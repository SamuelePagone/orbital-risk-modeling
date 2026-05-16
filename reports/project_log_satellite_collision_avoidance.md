# Project Log - Satellite Collision Avoidance Recommendation System

## Informazioni generali

**Titolo del progetto:** Recommendation System for Satellite Collision Avoidance Decision Support

**Obiettivo generale:** costruire un sistema di raccomandazione capace di supportare la decisione operativa in caso di possibile collisione tra oggetti spaziali.

Il sistema deve ricevere in input i dati relativi a un evento di conjunction, cioè un possibile avvicinamento pericoloso tra due oggetti spaziali, e produrre in output una raccomandazione ordinata tra quattro possibili azioni:

- no action
- monitor
- small maneuver
- major maneuver

L'obiettivo non è semplicemente predire se una collisione avverrà oppure no. L'obiettivo è trasformare l'analisi del rischio in una decisione consigliata, considerando anche vincoli operativi come tempo disponibile, distanza, velocità relativa, costo della manovra e priorità della missione.

---

# Struttura iniziale del progetto

## Cosa abbiamo impostato

La struttura del progetto è stata organizzata così:

```text
orbital-risk-modeling/
├── dataset/
│   └── data/
│       ├── kelvins_competition_data/
│       │   ├── train_data.csv
│       │   ├── test_data.csv
│       │   ├── test_data_private.csv
│       │   └── train_data.zip
│       └── raw_data/
├── notebooks/
├── outputs/
│   ├── figures/
│   ├── recommendations/
│   └── tables/
├── project_docs/
├── reports/
├── src/
│   ├── __init__.py
│   ├── data_loading.py
│   ├── preprocessing.py
│   ├── recommender.py
│   └── evaluation.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Perché questa struttura è utile

Questa struttura separa chiaramente le varie parti del progetto:

- `dataset/` contiene i dati originali e non deve essere modificata direttamente.
- `notebooks/` contiene l'esplorazione dei dati.
- `src/` contiene il codice Python modulare.
- `outputs/` conterrà risultati, grafici, tabelle e raccomandazioni.
- `reports/` contiene i report tecnici e il project log.
- `project_docs/` contiene documentazione più descrittiva o PDF del progetto.
- `main.py` servirà per eseguire tutta la pipeline.
- `requirements.txt` elenca le librerie necessarie.

La separazione è importante perché rende il progetto più professionale, più leggibile e più facile da spiegare.

---

# Step 1 - Setup di `requirements.txt`

## Cosa abbiamo fatto

Abbiamo controllato e impostato il file `requirements.txt` con le librerie principali:

```text
pandas
numpy
scikit-learn
matplotlib
jupyter
notebook
```

## Perché lo abbiamo fatto

Questo file serve a rendere il progetto riproducibile.

Se un altro computer, un professore o un collaboratore apre il progetto, può installare tutte le dipendenze con:

```bash
pip install -r requirements.txt
```

Le librerie hanno questi ruoli:

- `pandas`: lettura e analisi dei CSV.
- `numpy`: calcoli numerici.
- `scikit-learn`: normalizzazione, preprocessing e possibili metriche.
- `matplotlib`: grafici.
- `jupyter` e `notebook`: esplorazione interattiva dei dati.

## Risultato ottenuto

Il progetto ha ora una base chiara per installare gli strumenti Python necessari.

---

# Step 2 - Prima ispezione del dataset con Codex

## Prompt dato a Codex

```text
Inspect the current repository structure and the dataset files.

Do not delete, move, rename, or modify any dataset file.

Focus only on:
dataset/data/kelvins_competition_data/train_data.csv

Create a markdown report at:
reports/data_inspection.md

The report must include:

1. Exact path of the dataset used.
2. Number of rows and columns.
3. Full list of column names.
4. Data types of each column.
5. Number of missing values per column.
6. Number of duplicated rows.
7. First 5 rows of the dataset.
8. Basic descriptive statistics for numerical columns.
9. A short explanation of which columns seem useful for a satellite collision avoidance decision-support system.
10. A short note about whether these variables are present or need to be created:
   - collision probability
   - miss distance
   - relative velocity
   - time to closest approach
   - fuel cost
   - mission priority

Do not train any model.
Do not create recommendations.
Do not create plots.
Do not modify the original dataset.

This step is only for dataset inspection.
```

## Perché abbiamo fatto questo step

Prima di costruire un modello o uno score, dobbiamo capire esattamente com'è fatto il dataset reale.

Non possiamo partire direttamente con formule o modelli, perché rischieremmo di usare colonne inventate o nomi sbagliati.

Questo step serve a rispondere a domande fondamentali:

- Quante righe ha il dataset?
- Quante colonne ha?
- Quali colonne sono presenti?
- Quali colonne mancano?
- Ci sono valori mancanti?
- Ci sono duplicati?
- Le colonne principali per il progetto esistono davvero?
- Il dataset è adatto a un sistema di collision avoidance?

## Risultati ottenuti

Codex ha creato il file:

```text
reports/data_inspection.md
```

Il dataset usato è:

```text
dataset/data/kelvins_competition_data/train_data.csv
```

Il dataset contiene:

```text
162634 righe
103 colonne
```

Non sono state trovate righe duplicate:

```text
duplicated rows = 0
```

## Colonne principali individuate

Le colonne più importanti per il nostro progetto sono:

```text
event_id
time_to_tca
mission_id
risk
max_risk_estimate
max_risk_scaling
miss_distance
relative_speed
relative_position_r
relative_position_t
relative_position_n
relative_velocity_r
relative_velocity_t
relative_velocity_n
mahalanobis_distance
c_object_type
```

## Variabili già presenti

Il dataset contiene già informazioni utili per:

- rischio di collisione
- distanza minima
- velocità relativa
- tempo al closest approach
- identificativo dell'evento
- identificativo della missione
- tipo di oggetto secondario
- incertezza tramite `mahalanobis_distance`

## Variabili mancanti

Il dataset non contiene direttamente:

```text
fuel_cost
mission_priority
```

Queste variabili dovranno essere create più avanti in modo sintetico e dichiarato nel report.

## Decisione presa

Il dataset è adatto al progetto.

Possiamo costruire un recommendation system usando le colonne reali:

```text
risk
max_risk_estimate
miss_distance
relative_speed
time_to_tca
mahalanobis_distance
mission_id
c_object_type
```

e aggiungendo successivamente variabili sintetiche per:

```text
fuel_cost
mission_priority
```

---

# Step 3 - Interpretazione della colonna `risk`

## Cosa abbiamo osservato

Dal report è emerso che la colonna `risk` non è una probabilità normale tra 0 e 1.

I suoi valori sono circa:

```text
min = -30
max = -1.44
mean = -19.34
```

Questo suggerisce che `risk` sia rappresentata in scala logaritmica, probabilmente come:

```text
risk = log10(collision probability)
```

## Spiegazione semplice

Se `risk` è in scala logaritmica:

```text
risk = -6  significa collision_probability = 10^-6
risk = -3  significa collision_probability = 10^-3
risk = -1  significa collision_probability = 10^-1
```

Quindi più `risk` è vicino a zero, più il rischio è alto.

Esempio:

```text
risk = -30  rischio estremamente basso
risk = -10  rischio basso
risk = -3   rischio molto più alto
risk = -1.4 rischio molto alto rispetto agli altri eventi
```

## Prompt dato a Codex

```text
Update the data inspection report at reports/data_inspection.md by adding a new section called "Risk Column Interpretation".

Do not modify any dataset file.

In the new section, explain that the column risk appears to be represented on a log10 scale because its values range approximately from -30 to -1.44. Explain that a derived collision probability can be computed as:

collision_probability = 10 ** risk

Also explain that max_risk_estimate appears to be a maximum estimated risk in the same log-scale convention, so a derived variable can be computed as:

max_collision_probability = 10 ** max_risk_estimate

Add a short example:
risk = -6 corresponds to collision_probability = 10^-6
risk = -3 corresponds to collision_probability = 10^-3

Finally, add a note that the project will use the original risk columns for traceability, but will create derived probability columns for interpretability and recommendation scoring.

Do not train any model.
Do not create recommendations.
Do not create plots.
Only update the markdown report.
```

## Perché abbiamo fatto questo step

Se usassimo direttamente `risk` nello score senza interpretarlo, potremmo sbagliare il significato.

La colonna `risk` è negativa e in log-scale, quindi per spiegare il progetto in modo intuitivo conviene creare anche una colonna derivata:

```text
collision_probability = 10 ** risk
```

e per `max_risk_estimate`:

```text
max_collision_probability = 10 ** max_risk_estimate
```

## Decisione presa

Nel progetto useremo entrambe le informazioni:

- le colonne originali `risk` e `max_risk_estimate` per tracciabilità;
- le colonne derivate `collision_probability` e `max_collision_probability` per interpretabilità e scoring.

---

# Step 4 - Creazione del notebook di esplorazione dati

## Prompt dato a Codex

```text
Create a Jupyter notebook named:
notebooks/01_data_exploration.ipynb

The notebook must load:
dataset/data/kelvins_competition_data/train_data.csv

The notebook must perform only exploratory data analysis.

Include these sections:

1. Load libraries
2. Load dataset
3. Show dataset shape
4. Show first rows
5. Show column names
6. Show data types
7. Show missing values summary
8. Show duplicated rows count
9. Show descriptive statistics for the key columns:
   - event_id
   - time_to_tca
   - risk
   - max_risk_estimate
   - miss_distance
   - relative_speed
   - mahalanobis_distance
10. Create derived columns only inside the notebook, without saving them to the original dataset:
   - collision_probability = 10 ** risk
   - max_collision_probability = 10 ** max_risk_estimate
11. Show descriptive statistics for:
   - collision_probability
   - max_collision_probability
12. Plot basic histograms for:
   - risk
   - max_risk_estimate
   - miss_distance
   - relative_speed
   - time_to_tca
   - collision_probability

Important constraints:
- Do not modify the original dataset.
- Do not save a processed dataset yet.
- Do not train any model.
- Do not create recommendations yet.
- This notebook is only for exploratory data analysis.
```

## Perché abbiamo fatto questo step

Il report `data_inspection.md` è utile per documentare il dataset, ma è statico.

Il notebook serve per esplorare i dati in modo pratico e visivo.

Con il notebook possiamo:

- caricare il dataset;
- controllare le colonne;
- vedere le prime righe;
- calcolare statistiche;
- creare colonne temporanee;
- generare istogrammi;
- capire meglio la distribuzione dei dati.

## Problema incontrato

Quando abbiamo provato a eseguire il notebook, Python ha dato questo errore:

```text
ModuleNotFoundError: No module named 'matplotlib'
```

## Perché è successo

Il notebook stava usando un ambiente Python che non aveva installato `matplotlib`.

Questo non era un errore del codice del progetto, ma un problema di dipendenze mancanti nell'ambiente Python selezionato.

## Soluzione applicata

Abbiamo installato le dipendenze con:

```bash
pip3 install -r requirements.txt
```

Poi abbiamo riavviato il notebook e rieseguito le celle.

## Risultato ottenuto

Il notebook ora sembra funzionare correttamente.

---

# Step 5 - Analisi delle prime righe del dataset

## Cosa abbiamo osservato

Dalle prime 5 righe del dataset abbiamo visto che:

```text
event_id = 0
```

compare in tutte le prime righe.

Allo stesso tempo, la colonna `time_to_tca` cambia:

```text
1.566798
1.207494
0.952193
0.579669
0.257806
```

## Interpretazione

Questo significa che il dataset probabilmente non ha una sola riga per ogni evento.

Più righe possono rappresentare aggiornamenti successivi dello stesso evento di conjunction.

In altre parole:

```text
più righe = più osservazioni temporali dello stesso evento
```

Esempio:

```text
event_id = 0
time_to_tca = 1.56
time_to_tca = 1.20
time_to_tca = 0.95
time_to_tca = 0.57
time_to_tca = 0.25
```

Queste non sono cinque collisioni diverse.

Sono cinque aggiornamenti dello stesso possibile evento di collisione.

## Perché è importante

Il nostro sistema deve rispondere alla domanda:

```text
Dato un evento di possibile collisione, quale azione conviene raccomandare?
```

Quindi vogliamo idealmente:

```text
1 event_id = 1 raccomandazione finale
```

Non vogliamo avere tante raccomandazioni confuse per lo stesso evento, almeno nella prima versione del progetto.

## Decisione concettuale

Per costruire un sistema più pulito e spiegabile, lavoreremo a livello evento.

Questo significa che, più avanti, creeremo un dataset event-level dove ogni `event_id` compare una sola volta.

---

# Step 6 - Statistiche descrittive delle colonne chiave

## Cosa abbiamo osservato

Dal notebook sono state ottenute le statistiche delle colonne chiave.

Le colonne analizzate sono:

```text
event_id
time_to_tca
risk
max_risk_estimate
miss_distance
relative_speed
mahalanobis_distance
```

## Risultati principali

### `event_id`

```text
count = 162634
min = 0
max = 13153
```

Questo indica che gli eventi hanno identificativi da 0 a 13153.

Quindi ci sono circa 13154 eventi possibili, anche se bisogna confermare il numero esatto con `nunique()`.

### `time_to_tca`

```text
min = -0.149808
mean = 3.350190
max = 6.993832
```

La maggior parte dei valori è positiva, ma esistono alcuni valori leggermente negativi.

### Interpretazione di `time_to_tca`

`time_to_tca` indica quanto tempo manca al closest approach, cioè al momento di massimo avvicinamento tra i due oggetti.

Se il valore è grande, c'è più tempo prima dell'evento.

Se il valore è piccolo, l'evento è vicino.

Se il valore è negativo, probabilmente il closest approach è già passato oppure la misura è stata registrata poco dopo.

### `risk`

```text
min = -30
mean = -19.340603
max = -1.442854
```

Questo conferma la natura logaritmica del rischio.

Più `risk` è vicino a zero, maggiore è il rischio.

### `max_risk_estimate`

```text
min = -9.814175
mean = -6.282332
max = -1.082442
```

Anche questa colonna sembra essere in scala logaritmica.

Rappresenta una stima massima del rischio.

### `miss_distance`

```text
min = 9
mean = 16531.662088
max = 67373
```

La distanza minima prevista tra gli oggetti è sempre positiva.

Ci sono eventi con distanza molto piccola, anche circa 9 metri, e altri con distanze molto grandi.

### Interpretazione di `miss_distance`

Più `miss_distance` è bassa, più l'evento è pericoloso.

Per il recommendation system, questa colonna sarà trasformata in una feature chiamata:

```text
distance_risk
```

dove:

```text
miss_distance bassa -> distance_risk alto
miss_distance alta -> distance_risk basso
```

### `relative_speed`

```text
min = 4
mean = 10655.819638
max = 17138
```

Questa colonna misura la velocità relativa tra gli oggetti.

È sempre positiva.

### Interpretazione di `relative_speed`

Maggiore è la velocità relativa, più grave può essere una collisione.

Questa feature sarà utile nello score finale.

### `mahalanobis_distance`

```text
min circa = 0
mean = 192.602768
max = 15427.160794
```

Questa misura tiene conto della distanza normalizzata rispetto all'incertezza.

È utile per valutare la separazione considerando anche la covarianza e l'incertezza orbitale.

## Decisione presa

Le feature principali per il primo modello saranno:

```text
risk
max_risk_estimate
miss_distance
relative_speed
time_to_tca
mahalanobis_distance
```

Inoltre useremo le derivate:

```text
collision_probability
max_collision_probability
```

---

# Step 7 - Decisione sul livello di analisi: row-level vs event-level

## Problema individuato

Il dataset contiene più righe per lo stesso `event_id`.

Questo significa che una riga rappresenta probabilmente un aggiornamento temporale dell'evento, non necessariamente un evento diverso.

## Possibili strategie

### Strategia 1 - Usare tutte le righe

In questo caso ogni osservazione temporale produrrebbe una raccomandazione.

Sarebbe un sistema dinamico, capace di aggiornare la raccomandazione man mano che arrivano nuovi dati.

### Vantaggi

- usa più dati;
- rappresenta l'evoluzione temporale;
- può essere più realistico in un sistema operativo avanzato.

### Svantaggi

- è più complesso;
- rischia di produrre più raccomandazioni per lo stesso evento;
- rende più difficile la valutazione;
- è troppo avanzato per una prima versione del progetto.

### Strategia 2 - Usare una sola riga per evento

In questo caso ogni `event_id` produce una sola raccomandazione finale.

La riga scelta è quella più vicina al TCA ma ancora prima del TCA.

Quindi, per ogni evento, scegliamo la riga con:

```text
time_to_tca >= 0
```

e con il valore più piccolo possibile di `time_to_tca`.

### Esempio

Per:

```text
event_id = 0

time_to_tca = 1.56
time_to_tca = 1.20
time_to_tca = 0.95
time_to_tca = 0.57
time_to_tca = 0.25
```

scegliamo:

```text
time_to_tca = 0.25
```

perché è l'osservazione più vicina al momento critico, ma ancora prima del closest approach.

## Decisione presa

Per la prima versione del progetto useremo la strategia event-level:

```text
1 event_id = 1 osservazione rappresentativa = 1 raccomandazione
```

## Perché questa scelta è professionale

Il progetto è un decision-support recommendation system.

La domanda principale è:

```text
Dato un evento di possibile collisione, quale azione conviene raccomandare?
```

Quindi la forma più chiara è:

```text
1 evento -> 1 ranking di azioni
```

Un sistema dinamico con più raccomandazioni per lo stesso evento sarebbe interessante, ma è più complesso e non necessario per la prima versione.

---

# Step 8 - Analisi event-level nel notebook

## Prompt dato a Codex

```text
Update notebooks/01_data_exploration.ipynb.

Add a new section after the descriptive statistics called:

"Event-level structure analysis"

In this section, add code that:
1. Counts the number of unique event_id values.
2. Computes how many rows each event_id has.
3. Shows descriptive statistics for the number of rows per event.
4. Shows the first 10 event_id values with the highest number of rows.
5. Creates a candidate event-level dataframe by keeping, for each event_id, the row with the smallest non-negative time_to_tca.
6. Shows the shape of this event-level dataframe.
7. Shows the first 5 rows of this event-level dataframe using only these columns:
   - event_id
   - time_to_tca
   - risk
   - max_risk_estimate
   - miss_distance
   - relative_speed
   - mahalanobis_distance
   - mission_id
   - c_object_type

Important constraints:
- Do not modify the original dataset.
- Do not save any processed dataset yet.
- Do not train any model.
- Do not create recommendations.
- This is only exploratory analysis.
```

## Perché abbiamo fatto questo step

Questo step serve a confermare la struttura temporale del dataset.

Vogliamo sapere:

- quanti `event_id` unici esistono;
- quante righe ci sono per ogni evento;
- se alcuni eventi hanno molte più osservazioni di altri;
- quante righe rimangono dopo aver creato un dataset event-level;
- se la scelta della riga più vicina al TCA produce una tabella sensata.

## Cosa deve produrre questo step

Il notebook deve produrre un dataframe temporaneo event-level, senza salvarlo ancora.

Questo dataframe deve contenere una sola riga per evento.

## Decisione non ancora finale

Questo dataset event-level è ancora una versione candidata.

Prima di salvarlo ufficialmente, dobbiamo controllare il risultato e verificare che abbia senso.

---

# Stato attuale del progetto

Finora abbiamo completato la fase iniziale di comprensione dei dati.

## Completato

- struttura progetto organizzata;
- `requirements.txt` impostato;
- report di ispezione dati creato;
- interpretazione della colonna `risk`;
- notebook di esplorazione creato;
- prime righe analizzate;
- statistiche delle colonne chiave lette;
- decisione concettuale verso analisi event-level;
- richiesta a Codex di aggiungere analisi event-level.

## Non ancora fatto

- preprocessing definitivo;
- salvataggio di un processed dataset;
- creazione di `fuel_cost`;
- creazione di `mission_priority`;
- normalizzazione delle feature;
- costruzione di `distance_risk`;
- costruzione di `urgency`;
- costruzione del `risk_score`;
- action scoring;
- ranking delle azioni;
- raccomandazioni finali;
- evaluation;
- grafici finali;
- final report.

---

# Prossimo step previsto

Il prossimo step sarà leggere l'output della sezione:

```text
Event-level structure analysis
```

nel notebook.

Dobbiamo controllare:

```text
numero di event_id unici
statistiche sul numero di righe per evento
shape del dataframe event-level
prime 5 righe del dataframe event-level
```

Solo dopo questa verifica potremo decidere se salvare ufficialmente un dataset processato event-level.

---

# Riassunto semplice

Finora non abbiamo ancora creato il modello.

Abbiamo fatto la cosa giusta prima del modello:

1. abbiamo capito il dataset;
2. abbiamo verificato le colonne;
3. abbiamo interpretato il rischio;
4. abbiamo capito che il dataset contiene più aggiornamenti per lo stesso evento;
5. abbiamo deciso che la prima versione del sistema lavorerà a livello evento.

Il progetto sta quindi passando da dati grezzi temporali a una struttura più adatta per un sistema di raccomandazione:

```text
più righe per evento
        ↓
una riga rappresentativa per evento
        ↓
una raccomandazione finale per evento
```
 

---

---

# Step 9 - Verifica della struttura event-level

## Cosa abbiamo fatto

Abbiamo eseguito la sezione `Event-level structure analysis` nel notebook `notebooks/01_data_exploration.ipynb`.

Questa sezione serve a verificare se il dataset contiene più righe per lo stesso evento e a costruire una prima versione temporanea del dataset a livello evento.

## Risultati ottenuti

Il numero di eventi unici è:

    Number of unique event_id values: 13154

Le statistiche del numero di righe per evento sono:

    count = 13154
    mean = 12.36
    std = 7.51
    min = 1
    25% = 5
    50% = 13
    75% = 20
    max = 23

Questo significa che ogni evento ha in media circa 12 aggiornamenti temporali.

Alcuni eventi hanno una sola osservazione, mentre altri arrivano fino a 23 osservazioni.

## Interpretazione

Il dataset non è strutturato come `1 riga = 1 evento`, ma come `più righe = più aggiornamenti temporali dello stesso evento`.

Quindi un singolo `event_id` può comparire più volte con diversi valori di `time_to_tca`.

Questo conferma che il dataset originale è observation-level, cioè contiene più osservazioni temporali per ogni evento di conjunction.

## Creazione del dataframe event-level

Abbiamo creato temporaneamente un dataframe event-level scegliendo, per ogni `event_id`, la riga con il più piccolo valore non negativo di `time_to_tca`.

La forma ottenuta è:

    event_level_df shape = (13143, 103)

Quindi il dataset passa da:

    162634 osservazioni temporali

a:

    13143 eventi utilizzabili a livello evento

## Perché ci sono 13143 eventi e non 13154

Gli eventi unici totali sono 13154, ma il dataframe event-level contiene 13143 eventi.

La differenza è:

    13154 - 13143 = 11 eventi

Questi 11 eventi probabilmente non hanno osservazioni con `time_to_tca >= 0`.

Per il progetto questo è accettabile, perché vogliamo costruire raccomandazioni prima del closest approach, non dopo.

## Decisione presa

Per la prima versione del progetto useremo una struttura event-level:

`1 event_id = 1 osservazione rappresentativa = 1 raccomandazione`

La riga rappresentativa sarà quella più vicina al TCA ma ancora prima del TCA, quindi con:

`time_to_tca >= 0`

e con il valore minimo di `time_to_tca`.

## Perché questa scelta è corretta

Il progetto vuole costruire un decision-support recommendation system.

La domanda principale è:

`Dato un evento di possibile collisione, quale azione conviene raccomandare?`

Per questo è più chiaro lavorare con una sola riga per evento, invece che produrre più raccomandazioni per diversi aggiornamenti temporali dello stesso evento.

Questa scelta rende il progetto più semplice, più interpretabile e più adatto a una prima versione completa.

---

# Step 10 - Creazione della funzione di preprocessing event-level

## Cosa abbiamo fatto

Abbiamo creato nel file `src/preprocessing.py` la funzione `create_event_level_dataset`.

Questa funzione prende in input il dataset originale in formato pandas DataFrame e restituisce un nuovo DataFrame a livello evento.

## Codice creato

La funzione principale è:

`create_event_level_dataset(df: pd.DataFrame) -> pd.DataFrame`

Riceve una tabella chiamata `df` e produce una nuova tabella con una sola riga per ogni `event_id`.

## Logica della funzione

La funzione esegue questi passaggi:

1. controlla che nel dataset esistano le colonne `event_id` e `time_to_tca`;
2. mantiene solo le righe con `time_to_tca >= 0`;
3. ordina il dataset per `event_id` e `time_to_tca`;
4. per ogni `event_id`, prende la prima riga dopo l'ordinamento;
5. restituisce il dataset event-level.

## Perché questa funzione è importante

Il dataset originale contiene più osservazioni temporali per lo stesso evento di conjunction.

Quindi la struttura originale è:

`più righe per evento`

Per il nostro recommendation system vogliamo invece:

`1 evento = 1 raccomandazione`

Per questo motivo creiamo un dataset event-level, dove ogni evento compare una sola volta.

## Regola scelta

Per ogni `event_id`, scegliamo la riga con `time_to_tca` più piccolo ma maggiore o uguale a zero.

Questo significa che scegliamo l'osservazione più vicina al momento del closest approach, ma ancora prima che il closest approach sia passato.

## Perché usiamo `time_to_tca >= 0`

Se `time_to_tca` è negativo, significa che il momento di massimo avvicinamento è probabilmente già passato.

Per un sistema di decision support, vogliamo raccomandare un'azione prima dell'evento critico, non dopo.

## Controlli presenti nella funzione

La funzione controlla che esistano le colonne necessarie:

- `event_id`
- `time_to_tca`

Se una di queste colonne manca, la funzione genera un errore chiaro.

Questo rende il codice più robusto, perché evita di continuare con un dataset sbagliato o incompleto.

## Risultato dello step

Abbiamo spostato la logica dal notebook esplorativo al codice vero del progetto.

Il notebook serve per capire i dati.

Il file `src/preprocessing.py` serve per costruire la pipeline definitiva.

## Decisione presa

La funzione `create_event_level_dataset` sarà usata più avanti in `main.py` per creare ufficialmente il dataset event-level.

---

# Step 11 - Creazione e salvataggio del dataset event-level

## Cosa abbiamo fatto

Abbiamo aggiornato il file `main.py` in modo che esegua la prima pipeline reale del progetto.

Lo script ora:

1. carica il dataset originale;
2. usa la funzione `create_event_level_dataset`;
3. crea la cartella `outputs/tables` se non esiste;
4. salva il dataset event-level in formato CSV;
5. stampa un riepilogo delle dimensioni dei dati.

## File creato

Il file processato è stato salvato in:

`outputs/tables/event_level_data.csv`

## Output ottenuto dal terminale

    Original dataset shape: (162634, 103)
    Event-level dataset shape: (13143, 103)
    Output path: outputs/tables/event_level_data.csv

## Interpretazione

Il dataset originale contiene 162634 righe, dove più righe possono appartenere allo stesso evento di collisione.

Dopo il preprocessing event-level, il dataset contiene 13143 righe.

Questo significa che ora abbiamo una sola osservazione rappresentativa per ogni evento utilizzabile.

## Perché questo step è importante

Questo è il primo vero passaggio dalla fase esplorativa alla pipeline del progetto.

Prima avevamo verificato la logica nel notebook.

Ora abbiamo creato un file concreto che useremo nei prossimi step.

Il recommendation system non lavorerà direttamente sul dataset grezzo, ma su questo dataset event-level.

## Decisione confermata

Useremo `outputs/tables/event_level_data.csv` come base per le prossime fasi:

- feature engineering;
- creazione di `collision_probability`;
- creazione di `distance_risk`;
- creazione di `urgency`;
- creazione di `fuel_cost`;
- creazione di `mission_priority`;
- risk score;
- action scoring;
- ranking delle azioni.

## Prossimo step

Il prossimo step sarà controllare velocemente il file salvato, per verificare che esista davvero e che sia leggibile.

---

# Step 12 - Verifica del file event-level salvato

## Cosa abbiamo fatto

Abbiamo controllato nel terminale che il file event-level fosse stato creato correttamente.

Il comando usato è stato:

    ls outputs/tables

## Output ottenuto

    event_level_data.csv

## Interpretazione

Il file `event_level_data.csv` esiste nella cartella `outputs/tables`.

Questo conferma che lo script `main.py` ha eseguito correttamente la pipeline di preprocessing event-level.

## Perché questo step è importante

Prima di continuare con feature engineering e scoring, dobbiamo essere sicuri che il dataset processato esista davvero.

Ora abbiamo due livelli di dati:

- dataset originale: `dataset/data/kelvins_competition_data/train_data.csv`
- dataset processato event-level: `outputs/tables/event_level_data.csv`

Il dataset originale resta intatto.

Il dataset event-level sarà la base per le prossime fasi del recommendation system.

## Decisione confermata

Da ora in poi useremo `outputs/tables/event_level_data.csv` come dataset di lavoro principale per costruire:

- collision probability;
- distance risk;
- urgency;
- fuel cost;
- mission priority;
- risk score;
- recommendation ranking.

---

# Step 13 - Creazione delle feature di probabilità

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/preprocessing.py` aggiungendo la funzione:

`add_probability_features`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con due nuove colonne:

- `collision_probability`
- `max_collision_probability`

## Perché servono queste feature

Nel dataset originale le colonne `risk` e `max_risk_estimate` sono rappresentate in scala logaritmica base 10.

Questo significa che valori come `-6`, `-3` o `-1` non sono direttamente probabilità, ma rappresentano il logaritmo della probabilità.

Per rendere il rischio più interpretabile, convertiamo questi valori con:

`collision_probability = 10 ** risk`

e:

`max_collision_probability = 10 ** max_risk_estimate`

## Esempio

Se:

`risk = -6`

allora:

`collision_probability = 10^-6 = 0.000001`

Se:

`risk = -3`

allora:

`collision_probability = 10^-3 = 0.001`

## Logica della funzione

La funzione:

1. controlla che esistano le colonne `risk` e `max_risk_estimate`;
2. crea una copia del DataFrame;
3. aggiunge `collision_probability`;
4. aggiunge `max_collision_probability`;
5. restituisce il nuovo DataFrame.

## Perché non modifichiamo il DataFrame originale

La funzione usa una copia del dataset.

Questo è importante perché rende il preprocessing più sicuro: il dataset di input non viene modificato direttamente.

## Decisione presa

Useremo le colonne originali `risk` e `max_risk_estimate` per mantenere tracciabilità rispetto al dataset ESA.

Useremo invece `collision_probability` e `max_collision_probability` per rendere più chiara l'interpretazione del rischio e per costruire le feature successive del recommendation system.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_probability_features`, così il file `outputs/tables/event_level_data.csv` conterrà anche le nuove colonne di probabilità.

---

# Step 14 - Aggiornamento della pipeline con le probability features

## Cosa abbiamo fatto

Abbiamo aggiornato il file `main.py` in modo che la pipeline usi anche la funzione `add_probability_features`.

Prima `main.py` creava solo il dataset event-level.

Ora invece esegue questi passaggi:

1. carica il dataset originale;
2. crea il dataset event-level con `create_event_level_dataset`;
3. aggiunge le feature di probabilità con `add_probability_features`;
4. salva il dataset finale in `outputs/tables/event_level_data.csv`;
5. stampa un riepilogo delle dimensioni dei dati.

## Output ottenuto dal terminale

    Original dataset shape: (162634, 103)
    Event-level dataset shape before probability features: (13143, 103)
    Final dataset shape after probability features: (13143, 105)
    Output path: outputs/tables/event_level_data.csv
    Added probability columns: collision_probability, max_collision_probability

## Interpretazione

Il dataset originale contiene 162634 osservazioni e 103 colonne.

Dopo la trasformazione event-level, il dataset contiene 13143 eventi e 103 colonne.

Dopo l'aggiunta delle probability features, il dataset finale contiene 13143 eventi e 105 colonne.

Le due nuove colonne sono:

- `collision_probability`
- `max_collision_probability`

## Perché questo step è importante

Le colonne originali `risk` e `max_risk_estimate` sono in scala logaritmica.

Questo formato è utile dal punto di vista tecnico, ma è meno intuitivo da interpretare.

Le nuove colonne trasformano questi valori in probabilità derivate:

`collision_probability = 10 ** risk`

`max_collision_probability = 10 ** max_risk_estimate`

Questo rende il dataset più leggibile e più adatto alla costruzione dello scoring.

## Decisione confermata

Il file `outputs/tables/event_level_data.csv` sarà il dataset principale per i prossimi step.

Da ora in poi contiene:

- una sola osservazione per evento;
- le colonne originali del dataset;
- le nuove colonne di probabilità.

## Prossimo step

Il prossimo step sarà verificare rapidamente che le nuove colonne siano effettivamente presenti nel CSV salvato.

---

# Step 15 - Verifica delle probability features nel file salvato

## Cosa abbiamo fatto

Abbiamo controllato che le nuove colonne di probabilità fossero effettivamente presenti nel file salvato:

`outputs/tables/event_level_data.csv`

Il comando usato nel terminale è stato:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df[['risk','collision_probability','max_risk_estimate','max_collision_probability']].head())"

## Output ottenuto

Il terminale ha mostrato le colonne:

- `risk`
- `collision_probability`
- `max_risk_estimate`
- `max_collision_probability`

Esempio di output:

    risk        collision_probability        max_risk_estimate        max_collision_probability
    -10.391260  ...                          ...                      1.403000e-08
    -9.248105   ...                          ...                      4.704000e-08
    -30.000000  ...                          ...                      3.554000e-08

## Interpretazione

Le nuove colonne sono presenti nel CSV salvato.

I valori di probabilità sono molto piccoli, e questo è coerente con il significato del rischio di collisione.

La notazione scientifica, ad esempio `1.403000e-08`, significa:

`0.00000001403`

Quindi il valore è una probabilità molto bassa.

## Perché questo step è importante

Questo controllo conferma che la pipeline non solo crea le nuove feature in memoria, ma le salva davvero nel file finale.

Il dataset `event_level_data.csv` ora contiene sia le colonne originali in scala logaritmica, sia le colonne derivate più interpretabili.

## Decisione confermata

Possiamo usare `outputs/tables/event_level_data.csv` come base per il prossimo step di feature engineering.

## Prossimo step

Il prossimo step sarà creare due nuove feature operative:

- `distance_risk`
- `urgency`

Queste serviranno a trasformare `miss_distance` e `time_to_tca` in variabili coerenti con il concetto di rischio.

---

# Step 16 - Creazione delle feature operative `distance_risk` e `urgency`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/preprocessing.py` aggiungendo la funzione:

`add_operational_risk_features`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con due nuove colonne:

- `distance_risk`
- `urgency`

## Perché servono queste feature

Nel dataset originale alcune variabili importanti funzionano in direzione opposta rispetto al concetto di rischio.

La colonna `miss_distance` indica la distanza minima prevista tra i due oggetti.

Una distanza più piccola indica una situazione più critica, mentre una distanza più grande indica una situazione meno critica.

Quindi trasformiamo `miss_distance` in `distance_risk`, dove:

`miss_distance bassa -> distance_risk alto`

`miss_distance alta -> distance_risk basso`

La colonna `time_to_tca` indica il tempo rimanente prima del closest approach.

Un valore più piccolo significa che c'è meno tempo per intervenire, quindi l'urgenza è maggiore.

Quindi trasformiamo `time_to_tca` in `urgency`, dove:

`time_to_tca basso -> urgency alta`

`time_to_tca alto -> urgency bassa`

## Logica della funzione

La funzione esegue questi passaggi:

1. controlla che esistano le colonne `miss_distance` e `time_to_tca`;
2. crea una copia del DataFrame;
3. calcola `distance_risk` tramite min-max normalization invertita;
4. calcola `urgency` tramite min-max normalization invertita;
5. gestisce il caso limite in cui massimo e minimo coincidono;
6. restituisce il nuovo DataFrame.

## Formula per `distance_risk`

`distance_risk = 1 - ((miss_distance - min_miss_distance) / (max_miss_distance - min_miss_distance))`

Questa formula assegna valori più alti agli eventi con distanza minima più bassa.

## Formula per `urgency`

`urgency = 1 - ((time_to_tca - min_time_to_tca) / (max_time_to_tca - min_time_to_tca))`

Questa formula assegna valori più alti agli eventi più vicini al TCA.

## Perché questo step è importante

Il futuro `risk_score` dovrà combinare più variabili.

Per farlo in modo semplice e coerente, vogliamo che tutte le feature abbiano la stessa interpretazione:

`valore alto = situazione più critica`

Con questo step, `miss_distance` e `time_to_tca` vengono trasformate in due feature coerenti con il concetto di rischio operativo.

## Decisione presa

Useremo `distance_risk` e `urgency` come feature principali per costruire il futuro score di rischio e per supportare il sistema di raccomandazione.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_operational_risk_features`, così il file `outputs/tables/event_level_data.csv` conterrà anche `distance_risk` e `urgency`.

---

# Step 17 - Aggiornamento della pipeline con `distance_risk` e `urgency`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `main.py` in modo che la pipeline usi anche la funzione `add_operational_risk_features`.

La pipeline ora esegue questi passaggi:

1. carica il dataset originale;
2. crea il dataset event-level con `create_event_level_dataset`;
3. aggiunge le probability features con `add_probability_features`;
4. aggiunge le operational risk features con `add_operational_risk_features`;
5. salva il risultato finale in `outputs/tables/event_level_data.csv`.

## Output ottenuto dal terminale

    Original dataset shape: (162634, 103)
    Event-level dataset shape: (13143, 103)
    Dataset shape after probability features: (13143, 105)
    Final dataset shape after operational risk features: (13143, 107)
    Output path: outputs/tables/event_level_data.csv
    Added columns: collision_probability, max_collision_probability, distance_risk, urgency

## Interpretazione

Il dataset originale contiene 162634 osservazioni e 103 colonne.

Dopo la trasformazione event-level, il dataset contiene 13143 eventi e 103 colonne.

Dopo l'aggiunta delle probability features, il dataset contiene 13143 eventi e 105 colonne.

Dopo l'aggiunta delle operational risk features, il dataset contiene 13143 eventi e 107 colonne.

Le nuove colonne aggiunte in questo step sono:

- `distance_risk`
- `urgency`

## Perché questo step è importante

`miss_distance` e `time_to_tca` sono due variabili fondamentali, ma funzionano in direzione opposta rispetto al rischio.

Una `miss_distance` più bassa indica una situazione più pericolosa.

Un `time_to_tca` più basso indica maggiore urgenza operativa.

Per costruire uno score chiaro, vogliamo invece che le nuove feature abbiano questa logica:

    valore alto = situazione più critica
    valore basso = situazione meno critica

Per questo abbiamo creato:

- `distance_risk`, dove valori alti indicano passaggi più ravvicinati;
- `urgency`, dove valori alti indicano meno tempo disponibile prima del TCA.

## Decisione confermata

Il file `outputs/tables/event_level_data.csv` ora contiene una sola riga per evento e le prime feature ingegnerizzate utili per il recommendation system.

Il dataset contiene ora:

- colonne originali ESA;
- `collision_probability`;
- `max_collision_probability`;
- `distance_risk`;
- `urgency`.

## Prossimo step

Il prossimo step sarà verificare rapidamente che `distance_risk` e `urgency` siano presenti nel CSV salvato e che i loro valori siano compresi tra 0 e 1.

---

# Step 18 - Verifica di `distance_risk` e `urgency`

## Cosa abbiamo fatto

Abbiamo verificato che le colonne `distance_risk` e `urgency` siano presenti nel file salvato:

`outputs/tables/event_level_data.csv`

Il comando usato nel terminale è stato:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df[['miss_distance','distance_risk','time_to_tca','urgency']].head()); print(df[['distance_risk','urgency']].describe())"

## Output ottenuto

Le statistiche principali sono:

    distance_risk:
    count = 13143
    mean = 0.718712
    std = 0.236015
    min = 0.000000
    max = 1.000000

    urgency:
    count = 13143
    mean = 0.817140
    std = 0.273093
    min = 0.000000
    max = 1.000000

## Interpretazione

Entrambe le colonne hanno 13143 valori, cioè un valore per ogni evento del dataset event-level.

Il valore minimo è 0 e il valore massimo è 1.

Questo conferma che la normalizzazione min-max invertita ha funzionato correttamente.

## Significato di `distance_risk`

`distance_risk` deriva da `miss_distance`.

Poiché una distanza minore indica un evento più pericoloso, la normalizzazione è stata invertita:

`miss_distance bassa -> distance_risk alto`

`miss_distance alta -> distance_risk basso`

## Significato di `urgency`

`urgency` deriva da `time_to_tca`.

Poiché un tempo minore indica meno tempo disponibile per agire, la normalizzazione è stata invertita:

`time_to_tca basso -> urgency alta`

`time_to_tca alto -> urgency bassa`

## Perché questo step è importante

Questo controllo conferma che le nuove feature operative sono presenti nel dataset finale e sono coerenti con la scala richiesta.

Da ora in poi possiamo usare queste feature per costruire il futuro `risk_score`.

## Decisione confermata

Le colonne `distance_risk` e `urgency` sono valide e possono essere usate nei prossimi step del recommendation system.

## Prossimo step

Il prossimo step sarà creare una feature normalizzata per `relative_speed`, così anche la velocità relativa sarà espressa su scala 0-1.

---

# Step 19 - Normalizzazione della velocità relativa

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/preprocessing.py` aggiungendo la funzione:

`add_normalized_velocity_feature`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con una nuova colonna:

`relative_speed_norm`

## Perché serve questa feature

Nel dataset originale la colonna `relative_speed` rappresenta la velocità relativa tra i due oggetti spaziali.

Questa variabile è importante perché una velocità relativa più alta rende un eventuale impatto più critico.

Il problema è che `relative_speed` ha valori molto più grandi rispetto alle altre feature già create.

Per esempio:

`relative_speed` può avere valori come 10000 o 17000.

Invece `distance_risk` e `urgency` sono già su scala 0-1.

Per poter combinare le variabili in uno score finale, dobbiamo portare anche la velocità relativa su scala 0-1.

## Logica della funzione

La funzione esegue questi passaggi:

1. controlla che esista la colonna `relative_speed`;
2. crea una copia del DataFrame;
3. calcola il valore minimo di `relative_speed`;
4. calcola il valore massimo di `relative_speed`;
5. applica una normalizzazione min-max;
6. gestisce il caso limite in cui massimo e minimo coincidono;
7. restituisce il nuovo DataFrame.

## Formula usata

`relative_speed_norm = (relative_speed - min_relative_speed) / (max_relative_speed - min_relative_speed)`

## Perché non invertiamo questa feature

Per `miss_distance` e `time_to_tca` abbiamo invertito la normalizzazione, perché valori più bassi indicano situazioni più critiche.

Per `relative_speed` invece non serve invertire.

Una velocità relativa più alta indica già una situazione più critica.

Quindi:

`relative_speed bassa -> relative_speed_norm basso`

`relative_speed alta -> relative_speed_norm alto`

## Perché questo step è importante

Il futuro `risk_score` dovrà combinare più feature.

Per evitare che `relative_speed` domini lo score solo perché ha numeri molto più grandi, la trasformiamo in una variabile normalizzata tra 0 e 1.

## Decisione presa

Useremo `relative_speed_norm` come feature di velocità nel futuro score di rischio.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_normalized_velocity_feature`, così il file `outputs/tables/event_level_data.csv` conterrà anche `relative_speed_norm`.

---

# Step 20 - Aggiornamento della pipeline con `relative_speed_norm`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `main.py` in modo che la pipeline usi anche la funzione:

`add_normalized_velocity_feature`

La pipeline ora esegue questi passaggi:

1. carica il dataset originale;
2. crea il dataset event-level con `create_event_level_dataset`;
3. aggiunge le probability features con `add_probability_features`;
4. aggiunge le operational risk features con `add_operational_risk_features`;
5. aggiunge la feature normalizzata di velocità con `add_normalized_velocity_feature`;
6. salva il risultato finale in `outputs/tables/event_level_data.csv`.

## Output ottenuto dal terminale

    Original dataset shape: (162634, 103)
    Event-level dataset shape: (13143, 103)
    Dataset shape after probability features: (13143, 105)
    Dataset shape after operational risk features: (13143, 107)
    Final dataset shape after normalized velocity feature: (13143, 108)
    Output path: outputs/tables/event_level_data.csv
    Added columns: collision_probability, max_collision_probability, distance_risk, urgency, relative_speed_norm

## Interpretazione

Il dataset originale contiene 162634 osservazioni e 103 colonne.

Dopo la trasformazione event-level, il dataset contiene 13143 eventi e 103 colonne.

Dopo l'aggiunta delle feature di probabilità, il dataset contiene 105 colonne.

Dopo l'aggiunta di `distance_risk` e `urgency`, il dataset contiene 107 colonne.

Dopo l'aggiunta di `relative_speed_norm`, il dataset finale contiene 108 colonne.

## Perché questo step è importante

La colonna originale `relative_speed` ha valori molto grandi rispetto alle altre feature.

Per esempio, può assumere valori nell'ordine di migliaia o decine di migliaia.

Invece feature come `distance_risk` e `urgency` sono su scala 0-1.

Per costruire uno score bilanciato, anche la velocità relativa deve essere portata su scala 0-1.

## Decisione confermata

Useremo `relative_speed_norm` come rappresentazione normalizzata della velocità relativa nel futuro `risk_score`.

## Stato attuale delle feature principali

Il dataset finale contiene ora:

- `collision_probability`
- `max_collision_probability`
- `distance_risk`
- `urgency`
- `relative_speed_norm`

Queste feature saranno la base per costruire il futuro score di rischio e il sistema di raccomandazione.

## Prossimo step

Il prossimo step sarà verificare rapidamente che `relative_speed_norm` sia presente nel CSV salvato e che i suoi valori siano compresi tra 0 e 1.

---

# Step 21 - Verifica di `relative_speed_norm`

## Cosa abbiamo fatto

Abbiamo verificato che la colonna `relative_speed_norm` sia presente nel file salvato:

`outputs/tables/event_level_data.csv`

Il comando usato nel terminale è stato:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df[['relative_speed','relative_speed_norm']].head()); print(df[['relative_speed_norm']].describe())"

## Output ottenuto

Le statistiche principali di `relative_speed_norm` sono:

    count = 13143
    mean = 0.606739
    std = 0.264132
    min = 0.000000
    25% = 0.410441
    50% = 0.699545
    75% = 0.841952
    max = 1.000000

## Interpretazione

La colonna `relative_speed_norm` contiene un valore per tutti i 13143 eventi del dataset event-level.

Il valore minimo è 0 e il valore massimo è 1.

Questo conferma che la normalizzazione min-max ha funzionato correttamente.

## Significato di `relative_speed_norm`

`relative_speed_norm` deriva dalla colonna originale `relative_speed`.

La velocità relativa viene trasformata su scala 0-1:

`relative_speed bassa -> relative_speed_norm basso`

`relative_speed alta -> relative_speed_norm alto`

A differenza di `distance_risk` e `urgency`, questa feature non viene invertita, perché una velocità più alta indica già una situazione più critica.

## Perché questo step è importante

Il futuro `risk_score` dovrà combinare più feature.

Per costruire uno score bilanciato, le variabili principali devono essere su scale comparabili.

Ora anche la velocità relativa è su scala 0-1, come `distance_risk` e `urgency`.

## Decisione confermata

La colonna `relative_speed_norm` è valida e sarà usata nel futuro `risk_score`.

## Stato attuale

Il dataset finale contiene ora le seguenti feature principali:

- `collision_probability`
- `max_collision_probability`
- `distance_risk`
- `urgency`
- `relative_speed_norm`

## Prossimo step

Il prossimo step sarà creare una versione normalizzata del rischio di collisione, perché `collision_probability` è molto piccola e difficile da combinare direttamente nello score.

---

# Step 22 - Creazione della feature normalizzata `risk_norm`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/preprocessing.py` aggiungendo la funzione:

`add_normalized_risk_feature`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con una nuova colonna:

`risk_norm`

## Perché serve questa feature

La colonna originale `risk` rappresenta il rischio di collisione in scala logaritmica base 10.

I valori sono negativi, ad esempio:

`-30`, `-10`, `-3`, `-1.4`

Più il valore è vicino a zero, maggiore è il rischio di collisione.

Questo succede perché `risk` rappresenta circa:

`log10(collision_probability)`

Quindi:

`risk = -6` corrisponde a `collision_probability = 10^-6`

`risk = -3` corrisponde a `collision_probability = 10^-3`

Tra questi, `-3` indica un rischio maggiore, perché corrisponde a una probabilità più alta.

## Logica della funzione

La funzione esegue questi passaggi:

1. controlla che esista la colonna `risk`;
2. crea una copia del DataFrame;
3. calcola il valore minimo di `risk`;
4. calcola il valore massimo di `risk`;
5. applica una normalizzazione min-max;
6. gestisce il caso limite in cui massimo e minimo coincidono;
7. restituisce il nuovo DataFrame.

## Formula usata

`risk_norm = (risk - min_risk) / (max_risk - min_risk)`

## Perché non invertiamo questa feature

Non invertiamo la formula perché `risk` funziona già nella direzione corretta.

Anche se i valori sono negativi, un valore più alto indica un rischio maggiore.

Esempio:

`-3 > -10`

e `-3` rappresenta una probabilità di collisione maggiore rispetto a `-10`.

Quindi:

`risk più alto -> risk_norm più alto`

`risk più basso -> risk_norm più basso`

## Perché questo step è importante

Il futuro `risk_score` dovrà combinare più feature.

Per farlo bene, è utile avere anche il rischio di collisione su scala 0-1, come:

- `distance_risk`
- `urgency`
- `relative_speed_norm`

Con `risk_norm`, anche il rischio principale diventa comparabile con le altre feature.

## Decisione presa

Useremo `risk_norm` come feature principale del rischio di collisione nel futuro `risk_score`.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_normalized_risk_feature`, così il file `outputs/tables/event_level_data.csv` conterrà anche `risk_norm`.

---

# Step 23 - Aggiornamento della pipeline con `risk_norm`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `main.py` in modo che la pipeline usi anche la funzione:

`add_normalized_risk_feature`

La pipeline ora esegue questi passaggi:

1. carica il dataset originale;
2. crea il dataset event-level con `create_event_level_dataset`;
3. aggiunge le probability features con `add_probability_features`;
4. aggiunge le operational risk features con `add_operational_risk_features`;
5. aggiunge la feature normalizzata di velocità con `add_normalized_velocity_feature`;
6. aggiunge la feature normalizzata di rischio con `add_normalized_risk_feature`;
7. salva il risultato finale in `outputs/tables/event_level_data.csv`.

## Output ottenuto dal terminale

    Original dataset shape: (162634, 103)
    Event-level dataset shape: (13143, 103)
    Dataset shape after probability features: (13143, 105)
    Dataset shape after operational risk features: (13143, 107)
    Dataset shape after normalized velocity feature: (13143, 108)
    Final dataset shape after normalized risk feature: (13143, 109)
    Output path: outputs/tables/event_level_data.csv
    Added columns: collision_probability, max_collision_probability, distance_risk, urgency, relative_speed_norm, risk_norm

## Interpretazione

Il dataset finale contiene ora 13143 eventi e 109 colonne.

La nuova colonna aggiunta è:

`risk_norm`

Questa colonna rappresenta il rischio di collisione originale su scala 0-1.

## Perché questo step è importante

La colonna `risk` originale è in scala logaritmica e contiene valori negativi.

Anche se è informativa, non è comoda da combinare direttamente con le altre feature.

Con `risk_norm`, il rischio viene trasformato in una scala più semplice:

    risk_norm vicino a 0 = rischio basso
    risk_norm vicino a 1 = rischio alto

## Decisione confermata

Useremo `risk_norm` come una delle feature principali del futuro `risk_score`.

## Stato attuale delle feature principali

Il dataset finale contiene ora:

- `collision_probability`
- `max_collision_probability`
- `distance_risk`
- `urgency`
- `relative_speed_norm`
- `risk_norm`

## Prossimo step

Il prossimo step sarà verificare che `risk_norm` sia presente nel CSV salvato e che i valori siano compresi tra 0 e 1.

---

# Step 25 - Creazione delle feature sintetiche `fuel_cost` e `mission_priority`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/preprocessing.py` aggiungendo la funzione:

`add_synthetic_decision_features`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con due nuove colonne:

- `fuel_cost`
- `mission_priority`

## Perché servono queste feature

Il dataset originale ESA non contiene direttamente:

- un costo di carburante;
- una priorità della missione.

Tuttavia, per costruire un sistema di raccomandazione realistico, non basta considerare solo il rischio fisico di collisione.

Una decisione operativa deve considerare anche:

- quanto può costare una manovra;
- quanto è importante la missione da proteggere.

Per questo motivo abbiamo creato due feature sintetiche di supporto decisionale.

## `fuel_cost`

`fuel_cost` rappresenta un costo operativo sintetico della manovra.

La formula usata è:

`fuel_cost = 0.6 * relative_speed_norm + 0.4 * urgency`

Questa formula significa che il costo sintetico aumenta quando:

- la velocità relativa è alta;
- l'evento è urgente;
- quindi la manovra può essere più complessa o costosa.

Il risultato viene limitato all'intervallo 0-1.

## `mission_priority`

`mission_priority` rappresenta una priorità sintetica della missione.

La formula usata è:

`mission_priority = 0.5 + 0.5 * ((mission_id % 5) / 4)`

Questa formula genera valori tra 0.5 e 1.0.

Un valore più alto indica una missione considerata più prioritaria.

## Perché sono feature sintetiche

Queste due variabili non sono misure reali presenti nel dataset.

Sono ipotesi progettuali introdotte per rendere il recommendation system più realistico.

Questa assunzione dovrà essere dichiarata chiaramente nel report finale.

## Logica della funzione

La funzione esegue questi passaggi:

1. controlla che esistano le colonne `relative_speed_norm`, `urgency` e `mission_id`;
2. crea una copia del DataFrame;
3. calcola `fuel_cost`;
4. calcola `mission_priority`;
5. restituisce il nuovo DataFrame.

## Perché questo step è importante

Con questo step passiamo da feature solo fisiche a feature utili per la decisione.

Il sistema finale dovrà raccomandare un'azione, non solo stimare il rischio.

Quindi deve considerare anche il costo operativo e l'importanza della missione.

## Decisione presa

Useremo `fuel_cost` e `mission_priority` nel futuro recommendation system.

Queste feature saranno usate per bilanciare il rischio di collisione con i costi e le priorità operative.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_synthetic_decision_features`, così il file `outputs/tables/event_level_data.csv` conterrà anche `fuel_cost` e `mission_priority`.

---

# Step 26 - Aggiornamento della pipeline con `fuel_cost` e `mission_priority`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `main.py` in modo che la pipeline usi anche la funzione:

`add_synthetic_decision_features`

La pipeline ora esegue questi passaggi:

1. carica il dataset originale;
2. crea il dataset event-level con `create_event_level_dataset`;
3. aggiunge le probability features con `add_probability_features`;
4. aggiunge le operational risk features con `add_operational_risk_features`;
5. aggiunge la feature normalizzata di velocità con `add_normalized_velocity_feature`;
6. aggiunge la feature normalizzata di rischio con `add_normalized_risk_feature`;
7. aggiunge le feature sintetiche decisionali con `add_synthetic_decision_features`;
8. salva il risultato finale in `outputs/tables/event_level_data.csv`.

## Output ottenuto dal terminale

    Final dataset shape after synthetic decision features: (13143, 111)
    Output path: outputs/tables/event_level_data.csv
    Added columns: collision_probability, max_collision_probability, distance_risk, urgency, relative_speed_norm, risk_norm, fuel_cost, mission_priority

## Interpretazione

Il dataset finale contiene ora 13143 eventi e 111 colonne.

Le due nuove colonne aggiunte sono:

- `fuel_cost`
- `mission_priority`

## Perché questo step è importante

Il dataset originale ESA non contiene direttamente un costo di carburante o una priorità della missione.

Però il nostro progetto non vuole solo stimare il rischio fisico.

Vuole raccomandare un'azione.

Per raccomandare un'azione in modo più realistico, servono anche feature decisionali:

- `fuel_cost`, per rappresentare il costo operativo sintetico della manovra;
- `mission_priority`, per rappresentare quanto è importante proteggere la missione.

## Decisione confermata

Da ora in poi il dataset finale contiene sia feature fisiche sia feature decisionali.

Feature fisiche principali:

- `risk_norm`
- `distance_risk`
- `urgency`
- `relative_speed_norm`

Feature decisionali principali:

- `fuel_cost`
- `mission_priority`

## Prossimo step

Il prossimo step sarà verificare che `fuel_cost` e `mission_priority` siano presenti nel CSV salvato e che abbiano valori coerenti tra 0 e 1.

---

# Step 27 - Verifica di `fuel_cost` e `mission_priority`

## Cosa abbiamo fatto

Abbiamo verificato che le colonne `fuel_cost` e `mission_priority` siano presenti nel file salvato:

`outputs/tables/event_level_data.csv`

Il comando usato nel terminale è stato:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df[['relative_speed_norm','urgency','fuel_cost','mission_id','mission_priority']].head()); print(df[['fuel_cost','mission_priority']].describe())"

## Output ottenuto

Le statistiche principali sono:

    fuel_cost:
    count = 13143
    mean = 0.690900
    std = 0.197832
    min = 0.011893
    25% = 0.549822
    50% = 0.731737
    75% = 0.872052
    max = 0.987810

    mission_priority:
    count = 13143
    mean = 0.668226
    std = 0.158640
    min = 0.500000
    25% = 0.500000
    50% = 0.625000
    75% = 0.750000
    max = 1.000000

## Interpretazione

Entrambe le colonne sono presenti nel dataset finale e hanno un valore per tutti i 13143 eventi.

`fuel_cost` è compreso circa tra 0 e 1.

`mission_priority` è compreso tra 0.5 e 1.0, come previsto dalla formula sintetica.

## Significato di `fuel_cost`

`fuel_cost` rappresenta un costo operativo sintetico della manovra.

La formula usata è:

`fuel_cost = 0.6 * relative_speed_norm + 0.4 * urgency`

Questo significa che il costo sintetico aumenta quando:

- la velocità relativa è alta;
- l'urgenza è alta;
- quindi la manovra può essere più complessa o costosa.

## Significato di `mission_priority`

`mission_priority` rappresenta una priorità sintetica della missione.

La formula usata è:

`mission_priority = 0.5 + 0.5 * ((mission_id % 5) / 4)`

Questa formula genera valori tra 0.5 e 1.0.

Un valore più alto indica una missione considerata più prioritaria.

## Perché questo step è importante

Questo controllo conferma che il dataset finale contiene anche feature decisionali.

Il progetto non deve solo valutare il rischio fisico di collisione, ma deve raccomandare un'azione.

Per raccomandare un'azione in modo più realistico servono anche:

- costo operativo;
- priorità della missione.

## Decisione confermata

Le colonne `fuel_cost` e `mission_priority` sono valide e possono essere usate nei prossimi step.

## Stato attuale

Il dataset finale contiene ora feature fisiche e decisionali.

Feature fisiche principali:

- `risk_norm`
- `distance_risk`
- `urgency`
- `relative_speed_norm`

Feature decisionali principali:

- `fuel_cost`
- `mission_priority`

## Prossimo step

Il prossimo step sarà costruire il primo `risk_score`, combinando le feature principali in un punteggio unico di severità dell'evento.

---

# Step 28 - Creazione del `risk_score`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/preprocessing.py` aggiungendo la funzione:

`add_risk_score`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con una nuova colonna:

`risk_score`

## Cosa rappresenta `risk_score`

`risk_score` rappresenta la severità complessiva dell'evento di conjunction.

Non è ancora la raccomandazione finale.

Serve a rispondere alla domanda:

`Quanto è critico questo evento?`

## Feature usate

La funzione combina queste feature:

- `risk_norm`
- `distance_risk`
- `urgency`
- `relative_speed_norm`
- `mission_priority`

## Formula usata

    risk_score =
        0.35 * risk_norm
        + 0.25 * distance_risk
        + 0.20 * urgency
        + 0.10 * relative_speed_norm
        + 0.10 * mission_priority

## Perché questi pesi

`risk_norm` ha il peso maggiore perché rappresenta direttamente il rischio di collisione.

`distance_risk` ha un peso alto perché una distanza minima bassa è un segnale importante di criticità.

`urgency` ha un peso rilevante perché meno tempo disponibile significa maggiore pressione decisionale.

`relative_speed_norm` ha un peso minore ma utile, perché velocità relative più alte rendono l'evento più severo.

`mission_priority` ha un peso minore ma permette di considerare l'importanza operativa della missione.

## Perché `fuel_cost` non è incluso

`fuel_cost` non è incluso nel `risk_score` perché non rappresenta la severità fisica dell'evento.

Il costo del carburante influenza quanto una manovra è desiderabile o conveniente, ma non aumenta direttamente il rischio di collisione.

Per questo motivo `fuel_cost` sarà usato più avanti nello scoring delle azioni.

## Interpretazione

`risk_score` è compreso tra 0 e 1.

Un valore vicino a 0 indica un evento meno critico.

Un valore vicino a 1 indica un evento più critico.

## Decisione presa

Useremo `risk_score` come punteggio principale di severità dell'evento.

Questo punteggio sarà la base per costruire il sistema di raccomandazione.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_risk_score`, così il file `outputs/tables/event_level_data.csv` conterrà anche la colonna `risk_score`.

---

# Step 30 - Creazione dello scoring delle azioni

## Cosa abbiamo fatto

Abbiamo creato nel file `src/recommender.py` la funzione:

`add_action_scores`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con quattro nuove colonne:

- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`

## Perché serve questo step

Finora avevamo costruito il `risk_score`, cioè un punteggio unico che indica quanto è critico un evento.

Il passo successivo è valutare le possibili azioni operative.

Le azioni considerate sono:

- `no action`
- `monitor`
- `small maneuver`
- `major maneuver`

In questo step non scegliamo ancora l'azione finale.

Assegniamo soltanto un punteggio a ogni azione.

## Feature usate

La funzione usa queste colonne:

- `risk_score`
- `fuel_cost`
- `mission_priority`
- `urgency`

## Formula per `no_action_score`

`no_action_score = 1 - risk_score`

Questa formula favorisce `no action` quando il rischio è basso.

Se `risk_score` è alto, `no_action_score` diventa basso.

## Formula per `monitor_score`

`monitor_score = 1 - abs(risk_score - 0.45)`

Questa formula favorisce `monitor` quando il rischio è medio.

Il monitoraggio è una scelta intermedia: più adatta quando non è ancora necessario manovrare, ma l'evento non è completamente trascurabile.

## Formula per `small_maneuver_score`

`small_maneuver_score = 0.65 * risk_score + 0.20 * urgency - 0.25 * fuel_cost`

Questa formula favorisce una piccola manovra quando:

- il rischio è medio-alto;
- l'urgenza è alta;
- il costo operativo non è troppo elevato.

Il termine `fuel_cost` penalizza la manovra, perché una manovra più costosa è meno desiderabile.

## Formula per `major_maneuver_score`

`major_maneuver_score = 0.75 * risk_score + 0.15 * urgency + 0.20 * mission_priority - 0.10 * fuel_cost`

Questa formula favorisce una manovra importante quando:

- il rischio è alto;
- l'urgenza è alta;
- la missione è prioritaria.

Anche qui `fuel_cost` penalizza l'azione, ma meno rispetto alla small maneuver, perché se l'evento è molto critico può essere giustificata una manovra più costosa.

## Normalizzazione degli score

Tutti gli score vengono limitati all'intervallo 0-1.

Questo rende i punteggi confrontabili tra loro.

## Decisione presa

Useremo questi quattro action score per scegliere più avanti la raccomandazione finale.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare `add_action_scores`, così il file finale conterrà anche i punteggi delle quattro azioni.

---

# Step 31 - Aggiornamento della pipeline con gli action scores

## Cosa abbiamo fatto

Abbiamo aggiornato `main.py` in modo che la pipeline usi anche la funzione:

`add_action_scores`

La funzione si trova in:

`src/recommender.py`

## Risultato ottenuto

Il dataset finale è passato da:

`(13143, 112)`

a:

`(13143, 116)`

Questo significa che sono state aggiunte quattro nuove colonne:

- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`

## Interpretazione

Ora ogni evento ha un punteggio per ciascuna possibile azione:

- `no action`
- `monitor`
- `small maneuver`
- `major maneuver`

Questi punteggi non rappresentano ancora la raccomandazione finale.

Servono a confrontare le azioni tra loro.

## Perché questo step è importante

Prima avevamo solo `risk_score`, cioè un punteggio di severità dell'evento.

Adesso abbiamo anche uno score per ogni azione.

Questo è il primo vero passaggio verso il recommendation system finale.

## Decisione confermata

Useremo questi quattro action scores per scegliere la raccomandazione finale nello step successivo.

## Prossimo step

Il prossimo step sarà creare una funzione che sceglie automaticamente l'azione con lo score più alto e la salva in una nuova colonna:

`recommended_action`

---

# Step 32 - Creazione della raccomandazione finale `recommended_action`

## Cosa abbiamo fatto

Abbiamo aggiornato il file `src/recommender.py` aggiungendo la funzione:

`add_recommended_action`

Questa funzione prende in input un DataFrame e restituisce una copia del DataFrame con una nuova colonna:

`recommended_action`

## Perché serve questo step

Negli step precedenti abbiamo creato quattro punteggi, uno per ogni possibile azione:

- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`

Questi punteggi indicano quanto ogni azione è adatta a un certo evento.

Ora vogliamo trasformare questi punteggi in una decisione finale.

## Logica della funzione

Per ogni riga, la funzione confronta i quattro action scores e sceglie l'azione con il valore più alto.

Le etichette finali sono:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

## Gestione dei pareggi

Se due o più azioni hanno esattamente lo stesso punteggio massimo, la funzione sceglie l'azione meno aggressiva.

L'ordine di preferenza in caso di pareggio è:

1. `no_action`
2. `monitor`
3. `small_maneuver`
4. `major_maneuver`

Questa scelta è importante perché in un contesto operativo satellitare è preferibile evitare manovre inutili quando due azioni risultano equivalenti.

## Perché questo step è importante

Questo è il primo step in cui il sistema produce una vera uscita finale di raccomandazione.

Prima il sistema calcolava solo punteggi.

Ora invece può associare a ogni evento una raccomandazione operativa.

## Decisione presa

Useremo `recommended_action` come output finale principale del recommendation system.

## Prossimo step

Il prossimo step sarà aggiornare `main.py` per usare anche `add_recommended_action`, così il file finale conterrà la raccomandazione finale per ogni evento.

---

# Step 33 - Aggiornamento della pipeline con `recommended_action`

## Cosa abbiamo fatto

Abbiamo aggiornato `main.py` in modo che la pipeline usi anche la funzione:

`add_recommended_action`

La funzione si trova in:

`src/recommender.py`

## Risultato ottenuto

Il dataset finale è passato da:

`(13143, 116)`

a:

`(13143, 117)`

Questo significa che è stata aggiunta una nuova colonna:

`recommended_action`

## Interpretazione

Ora ogni evento del dataset event-level ha una raccomandazione finale.

La raccomandazione viene scelta confrontando i quattro action scores:

- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`

L'azione con lo score più alto diventa il valore di `recommended_action`.

## Gestione dei pareggi

In caso di pareggio tra due o più azioni, viene scelta l'azione meno aggressiva.

L'ordine usato è:

1. `no_action`
2. `monitor`
3. `small_maneuver`
4. `major_maneuver`

Questa scelta evita manovre inutili quando due azioni hanno la stessa convenienza.

## Perché questo step è importante

Questo è il primo momento in cui il progetto produce l'output finale del recommendation system.

Prima avevamo solo feature e punteggi.

Ora abbiamo una vera raccomandazione operativa per ogni evento.

## Stato attuale

Il file finale:

`outputs/tables/event_level_data.csv`

contiene ora:

- una riga per ogni evento;
- feature fisiche;
- feature decisionali;
- `risk_score`;
- action scores;
- `recommended_action`.

## Prossimo step

Il prossimo step sarà controllare la distribuzione delle raccomandazioni, cioè contare quanti eventi ricevono:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

,---

# Step 34 - Verifica della distribuzione delle raccomandazioni

## Cosa abbiamo fatto

Abbiamo verificato la distribuzione della colonna `recommended_action` nel file finale:

`outputs/tables/event_level_data.csv`

Il comando usato nel terminale è stato:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df['recommended_action'].value_counts()); print(df[['event_id','risk_score','fuel_cost','no_action_score','monitor_score','small_maneuver_score','major_maneuver_score','recommended_action']].head(10))"

## Output ottenuto

La distribuzione delle raccomandazioni è:

    monitor           11703
    major_maneuver     1388
    no_action            52

Il totale è:

    11703 + 1388 + 52 = 13143

Quindi ogni evento del dataset event-level ha ricevuto una raccomandazione finale.

## Interpretazione

La maggior parte degli eventi viene classificata come `monitor`.

Questo significa che, secondo le formule attuali, molti eventi sono abbastanza rilevanti da essere osservati, ma non abbastanza gravi da richiedere una manovra importante.

Una parte degli eventi viene classificata come `major_maneuver`.

Pochissimi eventi vengono classificati come `no_action`.

## Problema individuato

La raccomandazione `small_maneuver` non compare nella distribuzione.

Questo significa che, con le formule attuali, `small_maneuver_score` non risulta mai il punteggio più alto.

Il sistema funziona, ma gli action scores non sono ancora perfettamente bilanciati.

## Possibile causa

La formula di `small_maneuver_score` penalizza abbastanza il costo del carburante.

Invece `major_maneuver_score` riceve una spinta maggiore da `risk_score` e `mission_priority`, e viene penalizzata meno dal costo.

Di conseguenza, quando il rischio è alto vince spesso `major_maneuver`, mentre quando il rischio è medio vince spesso `monitor`.

La `small_maneuver` rimane schiacciata tra le due.

## Decisione presa

Prima di considerare il recommender finale completo, dobbiamo fare un tuning delle formule di action scoring.

L'obiettivo è ottenere una distribuzione più sensata, dove siano possibili tutte le azioni:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

## Prossimo step

Il prossimo step sarà modificare le formule in `add_action_scores` per rendere `small_maneuver` più competitiva negli eventi a rischio medio-alto.

---

# Step 35 - Primo tuning degli action scores

## Cosa abbiamo fatto

Abbiamo modificato le formule in `add_action_scores` dentro `src/recommender.py`.

L'obiettivo era correggere il problema osservato nello step precedente: `small_maneuver` non veniva mai selezionata come raccomandazione finale.

## Risultato ottenuto

Dopo aver rieseguito la pipeline con:

    python3 main.py

abbiamo controllato la distribuzione delle raccomandazioni con:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df['recommended_action'].value_counts())"

La nuova distribuzione è:

    monitor           10936
    small_maneuver     2145
    no_action            62

Il totale è:

    10936 + 2145 + 62 = 13143

Quindi ogni evento ha una raccomandazione finale.

## Interpretazione

Il tuning ha risolto il problema principale: `small_maneuver` ora viene selezionata.

Questo significa che il sistema riesce a distinguere eventi medi o medio-alti, per cui una piccola manovra può essere più appropriata del semplice monitoraggio.

## Nuovo problema individuato

Dopo il tuning, `major_maneuver` non compare più nella distribuzione.

Questo significa che la formula attuale rende la manovra maggiore troppo difficile da selezionare.

Prima `major_maneuver` veniva scelta troppo spesso.

Ora non viene scelta mai.

## Decisione presa

Serve un secondo tuning leggero.

L'obiettivo non è aumentare troppo `major_maneuver`, ma renderla possibile solo nei casi davvero più critici.

Una distribuzione più desiderabile dovrebbe contenere tutte le azioni:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

## Prossimo step

Il prossimo step sarà regolare leggermente la formula di `major_maneuver_score`, in modo che possa vincere solo negli eventi con rischio molto alto, urgenza alta e missione prioritaria.
---

# Step 36 - Secondo tuning degli action scores

## Cosa abbiamo fatto

Abbiamo modificato nuovamente le formule in `add_action_scores` dentro `src/recommender.py`.

L'obiettivo era rendere possibile anche la raccomandazione `major_maneuver`, che dopo il primo tuning non veniva mai selezionata.

## Modifica principale

Abbiamo aggiunto un termine extra a `major_maneuver_score` quando `risk_score` supera una certa soglia.

La logica è:

`major_maneuver` deve diventare competitiva solo negli eventi più critici.

## Risultato ottenuto

Dopo aver rieseguito:

    python3 main.py

abbiamo controllato la distribuzione delle raccomandazioni con:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df['recommended_action'].value_counts())"

La nuova distribuzione è:

    monitor           10927
    major_maneuver     2051
    small_maneuver      103
    no_action            62

Il totale è:

    10927 + 2051 + 103 + 62 = 13143

Quindi ogni evento ha una raccomandazione finale.

## Interpretazione

Ora tutte e quattro le azioni compaiono nella distribuzione:

- `monitor`
- `major_maneuver`
- `small_maneuver`
- `no_action`

Questo conferma che il sistema è in grado di selezionare tutte le possibili azioni.

## Nuovo problema individuato

La distribuzione è ancora sbilanciata.

`major_maneuver` ora compare, ma `small_maneuver` è diventata molto rara.

Questo suggerisce che il termine extra dato a `major_maneuver` è forse troppo forte oppure la soglia scelta è troppo permissiva.

## Decisione presa

Il sistema funziona, ma può essere migliorato con un ultimo tuning leggero.

L'obiettivo sarà:

- mantenere `monitor` come azione più comune;
- aumentare un po' `small_maneuver`;
- ridurre `major_maneuver` ai casi più critici;
- mantenere `no_action` per i casi meno critici.

## Prossimo step

Il prossimo step sarà fare un ultimo tuning delle formule degli action scores per ottenere una distribuzione più equilibrata.

---

# Step 37 - Ultimo tuning leggero degli action scores

## Cosa abbiamo fatto

Abbiamo modificato leggermente la formula di `major_maneuver_score` dentro `src/recommender.py`.

L'obiettivo era rendere `major_maneuver` più selettiva e aumentare leggermente la presenza di `small_maneuver`.

## Modifica applicata

Abbiamo cambiato il termine extra della major maneuver da:

`+ 0.25 * (risk_score > 0.75)`

a:

`+ 0.15 * (risk_score > 0.80)`

## Perché abbiamo fatto questa modifica

La versione precedente faceva comparire `major_maneuver`, ma riduceva troppo `small_maneuver`.

Con questa modifica, `major_maneuver` riceve una spinta extra solo quando `risk_score` è superiore a 0.80.

Questo rende la manovra maggiore più selettiva.

## Risultato ottenuto

Dopo aver rieseguito:

    python3 main.py

abbiamo controllato la distribuzione delle raccomandazioni con:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/tables/event_level_data.csv'); print(df['recommended_action'].value_counts())"

La distribuzione ottenuta è:

    monitor           10927
    major_maneuver     1945
    small_maneuver      209
    no_action            62

Il totale è:

    10927 + 1945 + 209 + 62 = 13143

Quindi ogni evento ha una raccomandazione finale.

## Interpretazione

Ora tutte e quattro le azioni sono presenti:

- `monitor`
- `major_maneuver`
- `small_maneuver`
- `no_action`

Rispetto allo step precedente:

- `major_maneuver` è diminuita;
- `small_maneuver` è aumentata;
- `monitor` rimane l'azione più frequente;
- `no_action` rimane limitata ai casi meno critici.

## Decisione presa

Questa distribuzione è accettabile per la prima versione del recommendation system.

Il sistema è ora in grado di produrre una raccomandazione finale per ogni evento e di usare tutte le possibili azioni.

## Stato attuale

Il progetto ora contiene una pipeline completa che:

1. carica il dataset originale;
2. crea il dataset event-level;
3. genera feature fisiche e decisionali;
4. calcola `risk_score`;
5. calcola gli action scores;
6. seleziona `recommended_action`;
7. salva il risultato finale in `outputs/tables/event_level_data.csv`.

## Prossimo step

Il prossimo step sarà creare un file di output più leggibile con solo le colonne principali della raccomandazione, ad esempio:

- `event_id`
- `risk_score`
- `fuel_cost`
- `mission_priority`
- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`
- `recommended_action`

---

# Step 38 - Creazione del file pulito delle raccomandazioni

## Cosa abbiamo fatto

Abbiamo aggiornato `main.py` in modo che la pipeline salvi due file di output:

1. il dataset completo;
2. il file pulito delle raccomandazioni.

Il dataset completo viene salvato in:

`outputs/tables/event_level_data.csv`

Il file pulito delle raccomandazioni viene salvato in:

`outputs/recommendations/recommendations.csv`

## Risultato ottenuto

Dopo aver eseguito:

    python3 main.py

abbiamo ottenuto:

    Clean recommendations shape: (13143, 20)
    Full dataset output path: outputs/tables/event_level_data.csv
    Clean recommendations output path: outputs/recommendations/recommendations.csv

## Interpretazione

Il file `outputs/tables/event_level_data.csv` contiene tutte le colonne del dataset finale, incluse feature, score e raccomandazioni.

Il file `outputs/recommendations/recommendations.csv` contiene solo le colonne principali necessarie per leggere e presentare il risultato finale del recommendation system.

## Colonne incluse nel file pulito

Il file pulito contiene 20 colonne:

- `event_id`
- `mission_id`
- `c_object_type`
- `time_to_tca`
- `risk`
- `risk_norm`
- `collision_probability`
- `miss_distance`
- `distance_risk`
- `relative_speed`
- `relative_speed_norm`
- `urgency`
- `fuel_cost`
- `mission_priority`
- `risk_score`
- `no_action_score`
- `monitor_score`
- `small_maneuver_score`
- `major_maneuver_score`
- `recommended_action`

## Perché questo step è importante

Il dataset completo è utile per analisi e debugging, ma contiene troppe colonne per essere letto facilmente.

Il file `recommendations.csv` è invece pensato come output finale leggibile del progetto.

Questo file mostra chiaramente, per ogni evento:

- il rischio;
- la distanza;
- l'urgenza;
- il costo sintetico;
- la priorità sintetica;
- il punteggio finale di rischio;
- il punteggio di ogni azione;
- la raccomandazione finale.

## Stato attuale

Il progetto ora produce un output finale pulito e presentabile.

La pipeline completa:

1. legge il dataset originale;
2. crea il dataset event-level;
3. genera feature fisiche e decisionali;
4. calcola `risk_score`;
5. calcola gli action scores;
6. seleziona `recommended_action`;
7. salva il dataset completo;
8. salva il file pulito delle raccomandazioni.

## Prossimo step

Il prossimo step sarà controllare rapidamente il contenuto di `outputs/recommendations/recommendations.csv` per verificare che sia leggibile e ordinato.

---

# Step 39 - Verifica del file pulito delle raccomandazioni

## Cosa abbiamo fatto

Abbiamo verificato il contenuto del file pulito delle raccomandazioni:

`outputs/recommendations/recommendations.csv`

Il comando usato nel terminale è stato:

    python3 -c "import pandas as pd; df = pd.read_csv('outputs/recommendations/recommendations.csv'); print(df.head(10)); print(df['recommended_action'].value_counts())"

## Output ottenuto

Il file contiene:

    10 rows x 20 columns

nella visualizzazione delle prime righe.

La distribuzione delle raccomandazioni è:

    monitor           10927
    major_maneuver     1945
    small_maneuver      209
    no_action            62

## Interpretazione

Il file `recommendations.csv` è stato creato correttamente.

Contiene le colonne principali del sistema di raccomandazione e permette di leggere facilmente il risultato finale per ogni evento.

Ogni evento ha una raccomandazione nella colonna:

`recommended_action`

## Perché questo step è importante

Il file completo `event_level_data.csv` è utile per analisi tecniche e debugging, ma contiene molte colonne.

Il file `recommendations.csv` è invece più adatto per:

- report finale;
- presentazione;
- demo;
- controllo rapido delle raccomandazioni.

## Decisione confermata

Useremo `outputs/recommendations/recommendations.csv` come output finale leggibile del recommendation system.

## Stato attuale

Il progetto ora produce:

1. un dataset completo con tutte le feature e gli score;
2. un file pulito con le raccomandazioni finali.

## Prossimo step

Il prossimo step sarà creare un report riassuntivo automatico con statistiche principali del recommendation system.

---

# Step 41 - Generazione automatica del report riassuntivo

## Cosa abbiamo fatto

Abbiamo aggiornato `main.py` in modo che la pipeline generi automaticamente anche un report riassuntivo del recommendation system.

Il report viene creato usando la funzione:

`create_recommendation_summary_report`

definita in:

`src/reporting.py`

## File creato

Il report viene salvato in:

`reports/recommendation_summary.md`

## Output ottenuto

Dopo aver eseguito:

    python3 main.py

la pipeline ha prodotto tre output finali:

    Full dataset output path: outputs/tables/event_level_data.csv
    Clean recommendations output path: outputs/recommendations/recommendations.csv
    Recommendation summary report output path: reports/recommendation_summary.md

## Interpretazione

Il progetto ora salva:

1. un dataset completo con tutte le colonne originali, feature, score e raccomandazioni;
2. un CSV pulito con le colonne principali della raccomandazione;
3. un report markdown automatico con statistiche riassuntive del recommendation system.

## Perché questo step è importante

Il report automatico rende il progetto più professionale e più facile da presentare.

Invece di controllare manualmente il CSV, possiamo aprire `reports/recommendation_summary.md` e leggere subito:

- numero di eventi;
- distribuzione delle raccomandazioni;
- percentuali per azione;
- risk score medio per azione;
- fuel cost medio per azione;
- esempi di raccomandazioni.

## Stato attuale

Il progetto ora ha una pipeline completa e riproducibile.

Eseguendo:

    python3 main.py

vengono generati automaticamente tutti gli output principali del sistema.

## Prossimo step

Il prossimo step sarà aprire e controllare `reports/recommendation_summary.md`, per verificare che il report sia leggibile e coerente.

---

# Step 43 - Generazione automatica del validation report

## Cosa abbiamo fatto

Abbiamo aggiornato `main.py` in modo che la pipeline generi automaticamente anche il report di validazione descrittiva.

Il report viene creato usando la funzione:

`create_recommendation_validation_report`

definita in:

`src/reporting.py`

## File creato

Il report viene salvato in:

`reports/recommendation_validation.md`

## Output ottenuto

Dopo aver eseguito:

    python3 main.py

la pipeline ha prodotto questi output finali:

    Full dataset output path: outputs/tables/event_level_data.csv
    Clean recommendations output path: outputs/recommendations/recommendations.csv
    Recommendation summary report output path: reports/recommendation_summary.md
    Recommendation validation report output path: reports/recommendation_validation.md

## Interpretazione

Il progetto ora produce quattro file principali:

1. `outputs/tables/event_level_data.csv`
2. `outputs/recommendations/recommendations.csv`
3. `reports/recommendation_summary.md`
4. `reports/recommendation_validation.md`

Il primo file contiene il dataset completo.

Il secondo file contiene il CSV pulito con le raccomandazioni finali.

Il terzo file riassume i risultati del recommendation system.

Il quarto file controlla la coerenza delle raccomandazioni rispetto alle feature e agli action scores.

## Perché questo step è importante

Il validation report rende il progetto più solido.

Non basta generare raccomandazioni: bisogna anche verificare che abbiano senso.

Questo report aiuta a dimostrare che:

- le azioni meno aggressive sono associate a rischio più basso;
- le azioni di manovra sono associate a rischio più alto;
- gli action scores sono coerenti con la raccomandazione finale;
- le feature sintetiche devono essere interpretate come assunzioni progettuali.

## Stato attuale

La pipeline è ora completa e produce automaticamente dataset, raccomandazioni e report.

## Prossimo step

Il prossimo step sarà aprire e controllare `reports/recommendation_validation.md`, per verificare che le tabelle siano leggibili e che i risultati siano coerenti.

---

# Step 45 - Aggiornamento del README del progetto

## Cosa abbiamo fatto

Abbiamo aggiornato il file `README.md` per rendere il progetto più chiaro, professionale e comprensibile.

Il README ora descrive:

- obiettivo del progetto;
- dataset utilizzato;
- struttura generale della pipeline;
- feature ingegnerizzate;
- logica del recommendation system;
- output generati;
- istruzioni per eseguire il progetto;
- distribuzione attuale delle raccomandazioni;
- note e assunzioni principali.

## Perché questo step è importante

Il codice del progetto è ormai funzionante, ma un progetto non è completo se non è anche comprensibile.

Il README serve come pagina introduttiva per chi apre il repository.

Deve permettere di capire rapidamente:

- cosa fa il progetto;
- perché è stato costruito;
- come si esegue;
- dove si trovano i risultati;
- quali assunzioni sono state fatte.

## Contenuto principale del README

Il README spiega che il progetto costruisce un sistema di supporto decisionale per eventi di conjunction satellitare.

Il sistema raccomanda una tra quattro possibili azioni:

- `no_action`
- `monitor`
- `small_maneuver`
- `major_maneuver`

Il README chiarisce anche che l'obiettivo non è solo stimare il rischio di collisione, ma trasformare gli indicatori di rischio in una raccomandazione operativa.

## Output documentati nel README

Il README descrive questi output:

- `outputs/tables/event_level_data.csv`
- `outputs/recommendations/recommendations.csv`
- `reports/recommendation_summary.md`
- `reports/recommendation_validation.md`

## Assunzioni documentate

Il README specifica che:

- il sistema è rule-based;
- non è un modello di machine learning addestrato;
- `fuel_cost` e `mission_priority` sono feature sintetiche;
- il dataset originale non viene modificato;
- la logica del recommender è spiegabile e basata su score ingegnerizzati.

## Stato attuale

Il progetto ora ha:

- codice funzionante;
- pipeline completa;
- output finali;
- report automatici;
- README professionale;
- project log dettagliato.

## Prossimo step

Il prossimo step sarà creare un final report del progetto, cioè un documento più discorsivo che spiega il progetto dall'inizio alla fine in stile relazione universitaria/professionale.