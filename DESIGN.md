# Regole di design — Borse del Mondo

Istruzioni per chiunque modifichi il sito (persone o assistenti AI).
Lo scopo è mantenere la grafica coerente, sobria ed elegante. In caso di dubbio: **meno effetti, più leggibilità**.

Ultimo aggiornamento: 24 novembre 2026.

---

## 1. Principi

1. **Leggibilità prima di tutto.** Il sito spiega investimenti a risparmiatori italiani: ogni numero e ogni testo deve leggersi al primo colpo.
2. **Sobrio ed elegante, non "fatto con l'AI".** Niente effetti decorativi in più, niente gradienti arcobaleno, niente icone generiche. Ogni elemento deve avere uno scopo.
3. **Semplice da usare.** La struttura attuale (banner → paesi → pannello del paese + card delle società → scheda) non si cambia senza un motivo forte.
4. **Solo computer.** Il sito è pensato per schermi desktop (larghezza di riferimento 1366 px). Il telefono non è una priorità.
5. **Informazione, non consulenza.** Nessun elemento grafico deve suggerire di comprare o vendere (niente "consigliato", "da comprare", frecce che invitano all'azione).

---

## 2. Colori

### Sfondo della pagina
- Caffellatte chiaro, sfumato: `#c9ad8f` al centro → `#b3967a` → `#9c7f65` ai bordi.
- Sopra: **mappa del mondo** marrone medio `#6b5240` con alone crema (file `img/mappa-latte.svg`), ferma mentre si scorre.

### Banner del titolo (in alto) e intestazione della scheda
- Fondo scuro caldo: `#1c130a` → `#3a2714` → `#6b4a24` → `#8a6332`, con una luce dorata in alto a destra.
- Grafico a candele dorato disegnato (`img/candele.svg`) sul lato destro, mai sotto il titolo.
- A sinistra, dietro il titolo, il fondo resta molto scuro per garantire il contrasto del testo bianco.
- Cornice: filo sottile semitrasparente (1 px bianco al 55%) + ombra morbida.

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

- Angoli arrotondati: banner e card **16–22 px**, pannelli **16 px**, campi e pulsanti a **pillola** (99 px), etichette 99 px.
- Card in griglia da 3 colonne, spazio tra card ~14 px.
- Ombre morbide e poco marcate. Niente bordi spessi.
- Bandiere: piccole bandiere disegnate (21×14 px, angoli 2,5 px), mai emoji (su Windows non si vedono).

---

## 5. Movimenti

- **Card delle società:** al passaggio del mouse si alzano di 3 px e si ingrandiscono del 3,5% con un'ombra più ampia (0,28 s). Tornano normali quando il mouse si sposta.
- **Paesi:** si ingrandiscono dell'8% al passaggio del mouse; il paese selezionato resta al 104%.
- **Stella preferiti:** si ingrandisce al passaggio.
- **Cambio di paese:** le card compaiono una dopo l'altra salendo di poco.
- **Scheda della società:** si apre con una breve dissolvenza dal basso.
- I movimenti sono **brevi e leggeri**: niente rimbalzi, rotazioni o effetti lunghi.
- Rispettare sempre l'impostazione "riduci animazioni" del computer (`prefers-reduced-motion`).

---

## 6. Immagini e grafiche

- **Solo immagini originali o con licenza d'uso libera.** Non usare foto, fermi immagine di film, meme o grafiche trovate su Pinterest o in rete senza permesso: niente volti di persone reali, niente marchi di altri.
- Le grafiche attuali (mappa, candele, logo a globo) sono disegnate appositamente in SVG: leggere, nitide, libere da diritti.
- Foto vere solo se proprie o da siti con licenza libera (es. Unsplash, Pexels), da verificare prima della pubblicazione. Immagini generate con AI: controllare che il servizio permetta l'uso commerciale.
- Le immagini sullo sfondo devono restare **in secondo piano**: non devono competere con le card né ridurre la leggibilità.

---

## 7. Componenti principali

| Componente | Regole |
|---|---|
| Banner | Logo + nome a sinistra; link in pillole trasparenti a destra; data, titolo, tre pillole (paesi, società, data dati); barra dei paesi con ricerca e Preferiti |
| Barra dei paesi | Paese attivo in pillola bianca con testo scuro; ricerca paese a sinistra; Preferiti fissi a destra |
| Card società | Nome, variazione 1 anno (pillola verde/rossa), ticker e indice, stella, capitalizzazione grande, minigrafico oro con "un anno fa … oggi", etichette settore/dimensione, rischio a pallini |
| Scheda società | Intestazione scura dorata come il banner; sezioni separate da linee sottili con titoli in maiuscoletto |
| Pagine Metodo e Chi siamo | Stessa striscia dorata in alto; testo dentro un riquadro bianco centrato |

---

## 8. Prima di pubblicare una modifica grafica

1. Mostrare un'anteprima (immagini o video) prima di pubblicare, se la modifica è visibile.
2. Controllare che tutte le 160 schede si aprano senza errori.
3. Controllare la leggibilità: nessun testo chiaro su fondo chiaro, nessun testo sopra le parti luminose delle immagini.
4. Applicare la stessa modifica a tutte le pagine (`index.html`, `metodo.html`, `chi-siamo.html`).
5. Verificare che non vengano caricate risorse da server esterni.
