# Regole di design — Borse del Mondo

Istruzioni per chiunque modifichi il sito (persone o assistenti AI).
Lo scopo è mantenere la grafica coerente, sobria ed elegante. In caso di dubbio: **meno effetti, più leggibilità**.

Ultimo aggiornamento: 25 novembre 2026 (schede, dividendi, confronti, screener, guide).

---

## 1. Principi

1. **Leggibilità prima di tutto.** Il sito spiega investimenti a risparmiatori italiani: ogni numero e ogni testo deve leggersi al primo colpo.
2. **Sobrio ed elegante, non "fatto con l'AI".** Niente effetti decorativi in più, niente gradienti arcobaleno, niente icone generiche. Ogni elemento deve avere uno scopo.
3. **Semplice da usare.** La struttura attuale (banner → paesi → pannello del paese + card delle società → scheda) non si cambia senza un motivo forte.
4. **Solo computer.** Il sito è pensato per schermi desktop (larghezza di riferimento 1366 px). Il telefono non è una priorità.
5. **Informazione, non consulenza.** Nessun elemento grafico deve suggerire di comprare o vendere (niente "consigliato", "da comprare", frecce che invitano all'azione).

---

## 2. Colori

### Colore del paese
Ogni paese ha un suo colore. Cambia il banner e lo sfondo della pagina quando si cambia paese.

| Paese | Colore |
|---|---|
| India | `#c27420` |
| Thailandia | `#334a8c` |
| Vietnam | `#a8301f` |
| Polonia | `#9a2236` |
| Brasile | `#23774a` |
| Singapore | `#b0303a` |
| Sudafrica | `#137059` |
| Australia | `#b5782c` |
| Preferiti / nessun paese | `#8a6332` (bronzo) |

Un paese nuovo riceve un colore scuro e caldo, distinguibile dagli altri, in genere ispirato alla bandiera.

### Sfondo della pagina
- Pagina dei mercati: tinta **chiara** del colore del paese (30% colore + 70% avorio `#efe7da`), con una leggera luce in alto. Nessuna immagine.
- Pagine Metodo e Chi siamo: avorio neutro `#e8dccb`.

### Banner del titolo (in alto)
- Fondo del colore del paese, coperto a sinistra da una sfumatura quasi nera per garantire il contrasto del testo bianco; leggere righe verticali "a vetro scanalato".
- A destra: **sagoma del paese** scura con contorno e alone crema; il **cambio con l'euro** in grande; la **variazione media** delle società in un anno; la miniatura **"Prossimo"**.
- Frecce ‹ › sopra il titolo per scorrere i paesi.
- Intestazione della scheda società e pagine secondarie: fondo scuro dorato con grafico a candele (`img/candele.svg`).

### Card, pannelli, scheda
- Fondo **bianco** `#ffffff`, bordo/ombra leggerissimi.
- Fondi secondari dentro le card (campi, tabelle): `#f4f5f1`.

### Testo
- Testo principale: quasi nero `#121410`.
- **Niente testo grigio chiaro su fondo chiaro.** Etichette, ticker, note, assi dei grafici: sempre scuri (`#121410` / `#23251f`).
- Sul banner scuro: testo bianco `#ffffff`.
- In fondo pagina (sopra lo sfondo caffellatte): bianco con leggera ombra.

### Colore d'accento: oro
| Uso | Colore |
|---|---|
| Oro principale (minigrafici, grafico prezzo, barre bilanci, stella attiva) | `#b8892f` |
| Oro chiaro (pallini nel banner, preferito attivo) | `#d9b25e` |
| Fondo etichetta settore | `#f6ecd6` |
| Testo etichetta settore | `#6b4c12` |

### Verde e rosso: solo per salite e discese
| Uso | Fondo | Testo |
|---|---|---|
| Variazione positiva | `#e6f2e8` | `#24633a` |
| Variazione negativa | `#f8e5e1` | `#93361f` |

Non usare verde o rosso per nient'altro (né decorazioni né etichette).

### Colori da non usare
Verde lime, viola, blu acceso, gradienti multicolore, grigio freddo come sfondo principale.

---

## 3. Caratteri

- **Source Sans 3** per tutto il testo, ospitato sul sito (`fonts/source-sans-3.woff`). Non caricare caratteri da Google Fonts o altri server esterni (privacy dei visitatori).
- Titolo del banner: due righe, la prima normale e la seconda **grassetto corsivo**, ~40 px, bianco.
- Numeri importanti (capitalizzazione): grandi (~24 px), semibold, quasi neri.
- Etichette piccole (CAPITALIZZAZIONE, COSA FA, ticker): maiuscoletto, ~11–12 px, spaziatura larga, scure.
- Testo normale: 15–16 px.

---

## 4. Forme e spaziature

- **Angoli vivi (0 px)** per: card delle società, pannello del paese, barra dei filtri (e i suoi campi), scheda della società e tutti i riquadri al suo interno, etichette dentro card/pannelli/scheda.
- Restano **arrotondati** solo il banner in alto (22 px) e gli elementi al suo interno (pillole, barra dei paesi, frecce).
- Card in griglia da 3 colonne, spazio tra card ~14 px.
- Ombre morbide e poco marcate. Niente bordi spessi.
- Bandiere: piccole bandiere disegnate (21×14 px, angoli 2,5 px), mai emoji (su Windows non si vedono).

---

## 5. Movimenti

- **Card delle società:** al passaggio del mouse si alzano di 3 px e si ingrandiscono del 3,5% con un'ombra più ampia (0,28 s). Tornano normali quando il mouse si sposta.
- **Paesi:** si ingrandiscono dell'8% al passaggio del mouse; il paese selezionato resta al 104%.
- **Stella preferiti:** si ingrandisce al passaggio.
- **Cambio di paese:** banner e sfondo sfumano nel nuovo colore (~0,8–0,9 s); la sagoma del paese entra da destra con leggera rotazione (0,7 s); i numeri compaiono con una breve dissolvenza; le card compaiono una dopo l'altra salendo di poco.
- **Scheda della società:** si apre con una breve dissolvenza dal basso.
- I movimenti sono **brevi e leggeri**: niente rimbalzi, rotazioni o effetti lunghi.
- Rispettare sempre l'impostazione "riduci animazioni" del computer (`prefers-reduced-motion`).

---

## 6. Immagini e grafiche

- **Solo immagini originali o con licenza d'uso libera.** Non usare foto, fermi immagine di film, meme o grafiche trovate su Pinterest o in rete senza permesso: niente volti di persone reali, niente marchi di altri.
- Le grafiche attuali (sagome dei paesi, candele, logo a globo) sono disegnate appositamente in SVG: leggere, nitide, libere da diritti. Le sagome sono semplificate; per renderle precise usare solo dati di confini a uso libero (es. Natural Earth).
- Foto vere solo se proprie o da siti con licenza libera (es. Unsplash, Pexels), da verificare prima della pubblicazione. Immagini generate con AI: controllare che il servizio permetta l'uso commerciale.
- Le immagini sullo sfondo devono restare **in secondo piano**: non devono competere con le card né ridurre la leggibilità.

---

## 7. Componenti principali

| Componente | Regole |
|---|---|
| Banner | Logo + nome a sinistra; link in pillole trasparenti a destra; frecce ‹ ›, data, titolo, tre pillole (paesi, società, data dati); a destra sagoma del paese, cambio, variazione media, "Prossimo"; barra dei paesi con ricerca e Preferiti |
| Barra dei paesi | Paese attivo in pillola bianca con testo scuro; ricerca paese a sinistra; Preferiti fissi a destra |
| Card società | Compatta: filo in alto (3 px) nel colore del paese; icona del settore in quadratino oro chiaro + nome (max 2 righe); capitalizzazione grande; etichette settore e dimensione. Niente altro: variazioni, dividendo, rischio, preferiti e confronto stanno nella scheda. Niente loghi delle aziende |
| Scheda società | Intestazione scura dorata come il banner; sezioni separate da linee sottili con titoli in maiuscoletto |
| Scheda società | Fascia fissa con prezzo, 1 anno locale, 1 anno in euro, dividendo, capitalizzazione; sezioni a schede: Panoramica · Dividendi · Bilanci · Rischio · Società simili · Come comprarla |
| Dividendi | Barre per anno: ordinario oro `#b8892f`, probabile straordinario viola `#7a4f9e`, anno in corso tratteggiato; avvisi con barra a sinistra (rosso riduzione/sospensione, verde aumento, ambra da verificare) |
| Barra del confronto | Fissa in basso, nera, fino a 4 società, pulsante oro "Confronta" |
| Screener e Paesi a confronto | Pannello filtri a sinistra, tabella bianca a destra ordinabile cliccando le intestazioni |
| Pagine Metodo, Guide e Chi siamo | Stessa striscia dorata in alto; testo dentro un riquadro bianco centrato |

---

### Etichette di stato
Ogni informazione mostra la sua natura con una piccola etichetta quadrata:

| Etichetta | Uso | Colori |
|---|---|---|
| ✓ Verificato | Dato controllato a mano con fonte e data | verde `#24633a` su `#eef7f0` |
| ⟳ Dati automatici | Numeri scaricati in automatico | grigio `#3d4652` su `#f4f6f8` |
| ? Da verificare | Stime automatiche, dati fiscali non ancora controllati da un professionista | ambra `#8a5a00` su `#fdf6e3` |
| ✎ Nostra sintesi | Descrizioni, punti di forza e rischi scritti da noi | viola `#5b3f8a` su `#f6f2fb` |
| § Fonte ufficiale | Riferimenti di legge | blu `#1d4f86` su `#eef4fb` |

### Confronti e classifiche
- Mostrare numeri ordinati, mai giudizi ("il migliore", "il più interessante").
- Medie per settore o paese: usare la **mediana**, mostrare sempre **quante società** ci sono dietro, nascondere i gruppi con meno di 3 società.
- Ogni confronto riporta: "Confronto tra dati, non una classifica: i risultati passati non indicano quelli futuri".

## 8. Prima di pubblicare una modifica grafica

1. Mostrare un'anteprima (immagini o video) prima di pubblicare, se la modifica è visibile.
2. Controllare che tutte le 160 schede si aprano senza errori.
3. Controllare la leggibilità: nessun testo chiaro su fondo chiaro, nessun testo sopra le parti luminose delle immagini.
4. Applicare la stessa modifica a tutte le pagine (`index.html`, `metodo.html`, `chi-siamo.html`).
5. Verificare che non vengano caricate risorse da server esterni.
