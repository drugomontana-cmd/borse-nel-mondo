# Borse del Mondo

Sito informativo sulle società quotate nei mercati meno conosciuti, pensato per chi investe dall'Italia.

## Com'è fatto

```
index.html                         il sito (una sola pagina)
data/countries.json                guide paese: borsa, accesso, tasse, liquidità, cambio
data/companies.json                società: descrizioni, punti di forza, rischi, ticker Yahoo
data/market.json                   dati di mercato, generato in automatico: non modificarlo a mano
scripts/update_data.py             script che scarica i dati
.github/workflows/update-data.yml  esegue lo script ogni giorno su GitHub
requirements.txt                   librerie Python necessarie
```

**Fonti:** Yahoo Finance (tramite yfinance), vnstock per il Vietnam se Yahoo non risponde, cambi ufficiali della Banca Centrale Europea.

> I dati di Yahoo Finance e vnstock sono per uso personale e non commerciale. Vanno bene per la demo.
> Prima di aprire il sito al pubblico o di guadagnarci, serve una fonte di dati con licenza commerciale.

## 1. Provare tutto sul tuo computer

Serve Python 3.10 o più recente (python.org).

```bash
cd borse-nel-mondo
pip install -r requirements.txt
python scripts/update_data.py
python -m http.server 8000
```

Poi apri http://localhost:8000 nel browser.

Il server locale serve perché i browser non permettono a una pagina aperta con doppio clic di leggere i file di dati.

## 2. Metterlo online gratis con GitHub

1. Crea un account su github.com e un nuovo repository, per esempio `borse-nel-mondo`.
2. Carica tutti i file della cartella, compresa la cartella nascosta `.github`. Il modo più semplice è GitHub Desktop.
3. **Settings → Actions → General → Workflow permissions:** scegli "Read and write permissions".
4. **Actions → "Aggiorna dati di mercato" → Run workflow:** il primo aggiornamento parte subito. Poi si ripete in automatico dal lunedì al venerdì.
5. **Settings → Pages:** come sorgente scegli il branch `main` e la cartella `/ (root)`. Dopo un paio di minuti il sito è online su `https://TUONOME.github.io/borse-nel-mondo/`.

## Aggiungere una società

Aggiungi un blocco in `data/companies.json` copiando uno esistente. Il campo `yahoo` è il simbolo usato da Yahoo Finance, con il suffisso del paese:

| Paese | Suffisso | Esempio |
|---|---|---|
| India (NSE) | `.NS` | `RELIANCE.NS` |
| Thailandia | `.BK` | `PTT.BK` |
| Vietnam (HOSE) | `.VN` | `VNM.VN` |
| Polonia | `.WA` | `PKO.WA` |

Per controllare il simbolo, cercalo su finance.yahoo.com. Al prossimo aggiornamento compariranno anche i suoi dati.

## Aggiungere un paese

Aggiungi un blocco in `data/countries.json` con il suffisso Yahoo e il codice valuta. Poi aggiungi la valuta del paese nella riga `country_currency` dentro `scripts/update_data.py`.

## Come vengono calcolati i dati

- **Dimensione:** capitalizzazione in euro. Large cap da 10 miliardi, Mid cap da 2 a 10 miliardi, Small cap sotto i 2 miliardi.
- **Liquidità:** media degli ultimi 60 giorni di scambi, in euro. Alta sopra i 10 milioni al giorno, Media da 1 a 10 milioni, Bassa sotto 1 milione.
- **Rendimento del dividendo:** dividendi degli ultimi 12 mesi divisi per il prezzo, al lordo delle tasse.
- **Se una fonte non risponde:** il sito mostra l'ultimo dato valido con un avviso.

## Controllo automatico dei dati

A ogni aggiornamento lo script segnala i dati sospetti:

- rendimento del dividendo oltre il 9%;
- P/E negativo o oltre 100;
- variazione a un anno sotto il -60% o sopra il +150%;
- prezzo cambiato di oltre il 30% dall'ultimo aggiornamento;
- ultima seduta più vecchia di 7 giorni;
- capitalizzazione mancante.

L'elenco finisce in `data/da-verificare.md`. Quando cambia, GitHub apre (o aggiorna) una segnalazione "Dati da verificare" nella scheda **Issues** e ti avvisa via email. Sul sito i dati sospetti compaiono con il simbolo ⚠.

Dopo il controllo manuale, l'esito va scritto in `data/verifiche.json`:

```json
"thailandia-advanc": { "accetta": ["dividendo_alto"], "nota": "Include un dividendo straordinario." },
"vietnam-pnj": { "nascondi": ["price", "market_cap_eur"] }
```

- `accetta`: l'avviso era un falso allarme e sparisce;
- `nascondi`: il dato è sbagliato e non viene mostrato;
- `nota`: spiegazione mostrata sul sito come "✓ Verificato".
