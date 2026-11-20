"""
Aggiorna i dati di mercato del sito "Borse del Mondo".

Fonti (gratuite):
  - Yahoo Finance, tramite la libreria yfinance: prezzi, capitalizzazione, P/E, dividendi, volumi
  - vnstock (solo Vietnam, se Yahoo non restituisce dati)
  - Banca Centrale Europea: tassi di cambio ufficiali dell'euro

Uso:
    python scripts/update_data.py

Legge  data/companies.json
Scrive data/market.json

Nota: i dati di Yahoo Finance sono destinati a uso personale. Prima di aprire
il sito al pubblico o di guadagnarci, serve una fonte con licenza commerciale.
"""

from __future__ import annotations

import json
import math
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMPANIES_FILE = ROOT / "data" / "companies.json"
MARKET_FILE = ROOT / "data" / "market.json"

ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
PAUSE_SECONDS = 1.0  # pausa tra una richiesta e l'altra, per non sovraccaricare le fonti

# Soglie di capitalizzazione in euro
LARGE_CAP_EUR = 10_000_000_000
MID_CAP_EUR = 2_000_000_000

# Soglie di liquidità: controvalore medio scambiato al giorno, in euro
HIGH_LIQ_EUR = 10_000_000
MEDIUM_LIQ_EUR = 1_000_000


# ---------------------------------------------------------------- utilità

def clean(value):
    """Converte in float e scarta valori vuoti, infiniti o non numerici."""
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(v) or math.isinf(v):
        return None
    return v


def size_from_cap(cap_eur):
    if cap_eur is None:
        return None
    if cap_eur >= LARGE_CAP_EUR:
        return "Large cap"
    if cap_eur >= MID_CAP_EUR:
        return "Mid cap"
    return "Small cap"


def liquidity_from_value(value_eur):
    if value_eur is None:
        return None
    if value_eur >= HIGH_LIQ_EUR:
        return "Alta"
    if value_eur >= MEDIUM_LIQ_EUR:
        return "Media"
    return "Bassa"


# ---------------------------------------------------------------- cambi BCE

def fetch_ecb_rates():
    """Restituisce {codice valuta: unità per 1 euro} dai cambi ufficiali BCE."""
    with urllib.request.urlopen(ECB_URL, timeout=30) as resp:
        tree = ET.fromstring(resp.read())
    rates, ref_date = {}, None
    for cube in tree.iter():
        if cube.get("time"):
            ref_date = cube.get("time")
        if cube.get("currency") and cube.get("rate"):
            rates[cube.get("currency")] = float(cube.get("rate"))
    rates["EUR"] = 1.0
    return rates, ref_date


def fetch_yahoo_fx(code):
    """Cambio EUR/<code> da Yahoo, per le valute che la BCE non pubblica (es. VND)."""
    import yfinance as yf
    hist = yf.Ticker(f"EUR{code}=X").history(period="5d")
    if hist is None or hist.empty:
        return None
    return clean(hist["Close"].dropna().iloc[-1])


# ---------------------------------------------------------------- storico per i grafici

def weekly_history(closes):
    """Chiusure settimanali (venerdì) dell'ultimo anno, più l'ultima chiusura: [[data, prezzo], ...]."""
    try:
        weekly = closes.resample("W-FRI").last().dropna()
    except Exception:
        weekly = closes
    points = [[d.strftime("%Y-%m-%d"), round(float(v), 4)] for d, v in weekly.items()]
    last_date = closes.index[-1].strftime("%Y-%m-%d")
    last = [last_date, round(float(closes.iloc[-1]), 4)]
    if points and points[-1][0] >= last_date:
        points[-1] = last
    elif not points or points[-1] != last:
        points.append(last)
    return points


# ---------------------------------------------------------------- Yahoo Finance

def fetch_yahoo(symbol):
    """Dati di mercato di un titolo da Yahoo Finance. Restituisce None se non trovato."""
    import yfinance as yf

    t = yf.Ticker(symbol)
    hist = t.history(period="1y", auto_adjust=False)
    if hist is None or hist.empty or hist["Close"].dropna().empty:
        return None

    closes = hist["Close"].dropna()
    price = clean(closes.iloc[-1])
    first = clean(closes.iloc[0])
    change_1y = (price / first - 1) if price and first else None

    dividends_12m = None
    if "Dividends" in hist.columns:
        dividends_12m = clean(hist["Dividends"].sum())

    avg_volume = None
    if "Volume" in hist.columns:
        avg_volume = clean(hist["Volume"].tail(60).mean())

    info = {}
    try:
        info = t.info or {}
    except Exception as exc:  # Yahoo a volte limita le richieste di "info"
        print(f"    info non disponibile per {symbol}: {exc}")

    currency = info.get("currency")
    market_cap = clean(info.get("marketCap"))
    shares = clean(info.get("sharesOutstanding"))
    pe = clean(info.get("trailingPE"))

    if market_cap is None:
        try:
            fi = t.fast_info
            market_cap = clean(fi.get("market_cap") or fi.get("marketCap"))
            currency = currency or fi.get("currency")
        except Exception:
            pass
    if market_cap is None and shares and price:
        market_cap = shares * price

    return {
        "history": weekly_history(closes),
        "source": "Yahoo Finance",
        "price": price,
        "currency": currency,
        "change_1y": change_1y,
        "market_cap": market_cap,
        "pe": pe,
        "dividends_12m": dividends_12m,
        "avg_volume": avg_volume,
        "last_trade_date": closes.index[-1].strftime("%Y-%m-%d"),
    }


# ---------------------------------------------------------------- vnstock (Vietnam)

def fetch_vnstock(ticker):
    """Riserva per il Vietnam. L'interfaccia di vnstock cambia spesso tra versioni."""
    try:
        from vnstock import Vnstock
    except ImportError:
        return None
    end = date.today()
    start = end - timedelta(days=370)
    df = None
    for source in ("VCI", "KBS", "TCBS"):
        try:
            stock = Vnstock().stock(symbol=ticker, source=source)
            df = stock.quote.history(start=start.isoformat(), end=end.isoformat(), interval="1D")
            if df is not None and not df.empty:
                break
        except Exception:
            df = None
    if df is None or df.empty:
        return None

    closes = df["close"].dropna()
    # Alcune fonti vietnamite esprimono i prezzi in migliaia di dong
    factor = 1000 if closes.median() < 1000 else 1
    price = clean(closes.iloc[-1] * factor)
    first = clean(closes.iloc[0] * factor)
    last_time = df["time"].iloc[-1] if "time" in df.columns else end
    hist_series = None
    try:
        import pandas as pd
        hist_series = pd.Series((df["close"] * factor).values, index=pd.to_datetime(df["time"])).dropna()
    except Exception:
        pass
    return {
        "history": weekly_history(hist_series) if hist_series is not None and not hist_series.empty else [],
        "source": "vnstock",
        "price": price,
        "currency": "VND",
        "change_1y": (price / first - 1) if price and first else None,
        "market_cap": None,
        "pe": None,
        "dividends_12m": None,
        "avg_volume": clean(df["volume"].tail(60).mean()) if "volume" in df.columns else None,
        "last_trade_date": str(last_time)[:10],
    }


# ---------------------------------------------------------------- calcoli

def enrich(raw, fx_rates, fallback_currency):
    """Aggiunge valori in euro, rendimento del dividendo, dimensione e liquidità."""
    currency = raw.get("currency") or fallback_currency
    rate = fx_rates.get(currency)  # unità di valuta per 1 euro
    price = raw.get("price")

    def to_eur(v):
        return v / rate if (v is not None and rate) else None

    div = raw.get("dividends_12m")
    dividend_yield = (div / price) if (div is not None and price) else None
    avg_value_eur = to_eur(raw["avg_volume"] * price) if (raw.get("avg_volume") and price) else None
    cap_eur = to_eur(raw.get("market_cap"))

    return {
        **raw,
        "currency": currency,
        "price_eur": to_eur(price),
        "market_cap_eur": cap_eur,
        "dividend_yield": dividend_yield,
        "avg_value_traded_eur": avg_value_eur,
        "size": size_from_cap(cap_eur),
        "liquidity": liquidity_from_value(avg_value_eur),
    }


# ---------------------------------------------------------------- controlli di qualità

VERIFY_FILE = ROOT / "data" / "verifiche.json"
REPORT_FILE = ROOT / "data" / "da-verificare.md"

HIGH_DIVIDEND = 0.09      # rendimento oltre il 9%
MAX_PE = 100
BIG_DROP_1Y = -0.60       # calo oltre il 60% in un anno
BIG_RISE_1Y = 1.50        # rialzo oltre il 150% in un anno
DAILY_JUMP = 0.30         # prezzo cambiato oltre il 30% dall'ultimo aggiornamento
MAX_AGE_DAYS = 7          # ultima seduta più vecchia di una settimana


def pct_it(v):
    return f"{v * 100:+.0f}%".replace("+-", "-")


def quality_checks(cur, prev, today):
    """Restituisce l'elenco dei problemi trovati: (codice, campo, titolo, dettaglio)."""
    out = []
    if cur.get("market_cap_eur") is None:
        out.append(("cap_mancante", "market_cap_eur", "Capitalizzazione non disponibile",
                    "La fonte non fornisce la capitalizzazione: la dimensione è quella indicata a mano."))
    dy = cur.get("dividend_yield")
    if dy is not None and dy > HIGH_DIVIDEND:
        out.append(("dividendo_alto", "dividend_yield", "Rendimento del dividendo insolitamente alto",
                    f"{dy * 100:.1f}%: può includere un dividendo straordinario o un errore della fonte."))
    pe = cur.get("pe")
    if pe is not None and (pe <= 0 or pe > MAX_PE):
        out.append(("pe_anomalo", "pe", "P/E fuori dal normale",
                    f"P/E di {pe:.1f}: utili negativi, molto bassi o dato errato."))
    ch = cur.get("change_1y")
    if ch is not None and (ch <= BIG_DROP_1Y or ch >= BIG_RISE_1Y):
        out.append(("variazione_estrema", "change_1y", "Variazione a un anno estrema",
                    f"{pct_it(ch)}: può essere un evento reale, un frazionamento o aumento di capitale, oppure un errore della fonte."))
    old_price = (prev or {}).get("price")
    if (old_price and cur.get("price") and prev.get("last_trade_date") != cur.get("last_trade_date")
            and abs(cur["price"] / old_price - 1) > DAILY_JUMP):
        out.append(("salto_prezzo", "price", "Salto di prezzo rispetto all'ultimo aggiornamento",
                    f"{pct_it(cur['price'] / old_price - 1)} dal {prev.get('last_trade_date')}."))
    ltd = cur.get("last_trade_date")
    if ltd:
        try:
            age = (today - date.fromisoformat(ltd[:10])).days
            if age > MAX_AGE_DAYS:
                out.append(("dato_vecchio", "price", "Dato non recente",
                            f"Ultima seduta disponibile: {ltd[:10]} ({age} giorni fa)."))
        except ValueError:
            pass
    return out


def apply_checks(results, previous, companies, today):
    """Aggiunge avvisi e verifiche manuali ai dati e scrive il rapporto per il controllo."""
    verified = {}
    if VERIFY_FILE.exists():
        verified = json.loads(VERIFY_FILE.read_text(encoding="utf-8"))
    names = {c["id"]: c["name"] for c in companies}
    report = []
    for cid, cur in results.items():
        v = verified.get(cid, {})
        accepted = set(v.get("accetta", []))
        hidden = set(v.get("nascondi", []))
        warnings, notes = [], []
        if cur.get("stale"):
            warnings.append({"code": "non_aggiornato", "field": None, "title": "Aggiornamento non riuscito",
                             "detail": "Mostriamo l'ultimo dato valido disponibile."})
        for code, field, title, detail in quality_checks(cur, previous.get(cid), today):
            if code in accepted or field in hidden:
                continue
            warnings.append({"code": code, "field": field, "title": title, "detail": detail})
        for field in hidden:  # campi giudicati errati dal controllo manuale
            cur[field] = None
        if v.get("nota"):
            notes.append(v["nota"])
        cur["warnings"] = warnings
        cur["verified_notes"] = notes
        cur["hidden_fields"] = sorted(hidden)
        for w in warnings:
            report.append((names.get(cid, cid), cid, w["code"], w["title"]))

    lines = ["# Dati da verificare", ""]
    if report:
        lines += ["Il controllo automatico ha trovato questi dati sospetti. Per ognuno: verificare su una fonte",
                  "indipendente e poi confermarlo, correggerlo o nasconderlo in `data/verifiche.json`.", "",
                  "| Società | Codice | Problema |", "|---|---|---|"]
        lines += [f"| {n} (`{cid}`) | `{code}` | {title} |" for n, cid, code, title in sorted(report)]
    else:
        lines.append("Nessun dato sospetto.")
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(report)


# ---------------------------------------------------------------- livello di rischio

COUNTRIES_FILE = ROOT / "data" / "countries.json"
RISK_LABELS = {1: "Contenuto", 2: "Moderato", 3: "Medio", 4: "Elevato", 5: "Molto elevato"}
RISK_WEIGHTS = {"volatilita": 0.30, "calo": 0.25, "liquidita": 0.15, "dimensione": 0.10, "paese": 0.20}
EVENT_ADJ = {"bassa": 0.25, "media": 0.5, "alta": 1.0}


def band(value, limits):
    """Restituisce 1..5 secondo le soglie crescenti indicate."""
    for i, lim in enumerate(limits, start=1):
        if value < lim:
            return i
    return 5


def history_stats(history):
    """Volatilità annua (da rendimenti settimanali) e calo massimo dall'ultimo picco."""
    prices = [p[1] for p in history or [] if p[1]]
    if len(prices) < 10:
        return None, None
    rets = [math.log(b / a) for a, b in zip(prices, prices[1:]) if a > 0 and b > 0]
    mean = sum(rets) / len(rets)
    vol = math.sqrt(sum((r - mean) ** 2 for r in rets) / (len(rets) - 1)) * math.sqrt(52)
    peak, mdd = prices[0], 0.0
    for p in prices:
        peak = max(peak, p)
        mdd = min(mdd, p / peak - 1)
    return vol, mdd


def compute_risk(cur, company, country):
    """Indicatore di rischio 1-5, con il dettaglio di ogni componente."""
    comps = []
    vol, mdd = history_stats(cur.get("history"))
    if vol is not None:
        comps.append(("volatilita", "Volatilità", f"{vol * 100:.0f}% annuo", band(vol, [0.20, 0.30, 0.40, 0.55])))
        comps.append(("calo", "Calo massimo in un anno", f"{mdd * 100:.0f}%", band(-mdd, [0.15, 0.25, 0.40, 0.60])))
    liq = cur.get("liquidity")
    if liq:
        comps.append(("liquidita", "Liquidità", liq, {"Alta": 1, "Media": 3, "Bassa": 5}[liq]))
    size = cur.get("size")
    if size:
        comps.append(("dimensione", "Dimensione", size, {"Large cap": 1, "Mid cap": 2, "Small cap": 4}[size]))
    if country.get("country_risk"):
        comps.append(("paese", "Paese e accesso", country.get("name", ""), country["country_risk"]))
    if not comps:
        return None
    wsum = sum(RISK_WEIGHTS[k] for k, *_ in comps)
    base = sum(RISK_WEIGHTS[k] * s for k, _, _, s in comps) / wsum
    events = company.get("events", [])
    adj = max((EVENT_ADJ.get(e.get("severity"), 0) for e in events), default=0)
    score = min(5.0, base + adj)
    level = max(1, min(5, int(score + 0.5)))
    return {
        "level": level,
        "label": RISK_LABELS[level],
        "score": round(score, 2),
        "components": [{"key": k, "name": n, "value": v, "score": s} for k, n, v, s in comps],
        "events_adjustment": adj,
    }


# ---------------------------------------------------------------- principale

def run(fetch_yahoo=fetch_yahoo, fetch_vnstock=fetch_vnstock,
        fetch_ecb=fetch_ecb_rates, fetch_fx=fetch_yahoo_fx, pause=PAUSE_SECONDS):
    companies = json.loads(COMPANIES_FILE.read_text(encoding="utf-8"))
    previous, previous_fx = {}, {}
    if MARKET_FILE.exists():
        old = json.loads(MARKET_FILE.read_text(encoding="utf-8"))
        previous = old.get("companies", {})
        previous_fx = old.get("fx", {}) or {}

    # Cambi: BCE, poi Yahoo per le valute mancanti, poi l'ultimo cambio salvato
    country_currency = {k: v["currency_code"] for k, v in json.loads(COUNTRIES_FILE.read_text(encoding="utf-8")).get("countries", {}).items()}
    try:
        fx_rates, fx_date = fetch_ecb()
    except Exception as exc:
        print(f"Cambi BCE non disponibili: {exc}")
        fx_rates, fx_date = {"EUR": 1.0}, previous_fx.get("date")
    fx_sources = {code: "BCE" for code in fx_rates}
    for code in set(country_currency.values()):
        if code not in fx_rates:
            try:
                rate = fetch_fx(code)
            except Exception as exc:
                print(f"Cambio {code} non disponibile: {exc}")
                rate = None
            if rate:
                fx_rates[code] = rate
                fx_sources[code] = "Yahoo Finance"
            elif code in previous_fx.get("per_eur", {}):
                fx_rates[code] = previous_fx["per_eur"][code]
                fx_sources[code] = (previous_fx.get("sources", {}).get(code) or "") + " (ultimo disponibile)"

    results, ok, failed = {}, 0, []
    for c in companies:
        print(f"- {c['name']} ({c['yahoo']})")
        raw = None
        try:
            raw = fetch_yahoo(c["yahoo"])
        except Exception as exc:
            print(f"    Yahoo errore: {exc}")
        if (raw is None or raw.get("price") is None) and c["country"] == "vietnam":
            try:
                raw = fetch_vnstock(c["ticker"])
            except Exception as exc:
                print(f"    vnstock errore: {exc}")

        if raw and raw.get("price") is not None:
            results[c["id"]] = {**enrich(raw, fx_rates, country_currency[c["country"]]), "stale": False}
            ok += 1
        elif c["id"] in previous:
            # Teniamo l'ultimo dato valido, segnalandolo come non aggiornato
            results[c["id"]] = {**previous[c["id"]], "stale": True}
            failed.append(c["id"])
        else:
            failed.append(c["id"])
        time.sleep(pause)

    countries = json.loads(COUNTRIES_FILE.read_text(encoding="utf-8")).get("countries", {})
    by_id = {c["id"]: c for c in companies}
    for cid, cur in results.items():
        try:
            cur["risk"] = compute_risk(cur, by_id[cid], countries.get(by_id[cid]["country"], {}))
        except Exception as exc:
            print(f"    rischio non calcolato per {cid}: {exc}")
            cur["risk"] = None

    n_warnings = apply_checks(results, previous, companies, date.today())
    print(f"Dati da verificare: {n_warnings}")

    output = {
        "updated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "fx": {
            "date": fx_date,
            "per_eur": {k: fx_rates[k] for k in sorted(set(country_currency.values())) if k in fx_rates},
            "sources": {k: fx_sources.get(k) for k in sorted(set(country_currency.values()))},
        },
        "thresholds_eur": {"large_cap": LARGE_CAP_EUR, "mid_cap": MID_CAP_EUR,
                           "high_liquidity": HIGH_LIQ_EUR, "medium_liquidity": MEDIUM_LIQ_EUR},
        "companies": results,
    }
    MARKET_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nAggiornate {ok} società su {len(companies)}.")
    if failed:
        print("Senza dati nuovi:", ", ".join(failed))
    return output


if __name__ == "__main__":
    out = run()
    sys.exit(0 if out["companies"] else 1)
