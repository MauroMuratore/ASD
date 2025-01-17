# Progetto di Algoritmi e Strutture Dati

## Requisiti

Per l'esecuzione è necessario aver installato una versione di Python 3.10 o superiore. Per installare tutte le dipendenze necessarie si può fare eseguendo il comando:
```
pip install -r requirements.txt
```

## Esecuzione

Per eseguire il programma basta eseguire il comando:
```
python3 main.py
```

All'interno del programma si potrà selezionare tra diversi compiti:

1. Generare un problema
2. Risolvere un problema
3. Generare e risolvere un problema
4. Generare una lista di problemi
5. Risolvere tutti i problemi 

## Struttura della directory data

```
[data]
	|-[adj_list]
	|-[problem]
	|-[result]
	|-gg_result.csv
	|-result.csv
```

- Nella directory **adj_list** sono presenti le liste di adiacenza delle griglie generate sotto forma testuale
- Nella directory **problem** sono presenti i problemi generati, ogni file contiene le informazioni del problema corrispondente, come nodo iniziale e finale, il percorso degli altri agenti e il riferimento alla lista di adiacenza corrispondente. A una lista di adiacenza possono essere associati più problemi
- Nella directory **result** sono presenti i risultati delle risoluzioni dei problemi. In ogni file ci sono le informazioni sul problema e sulla soluzione, oltre che una rappresentazione visiva del grafo
- Il file **gg_result.csv** contiene le informazioni riguardo ai parametri e i tempi diversi tempi per la generazione di tutti problemi
- Il file **result.csv** contiene le informazioni relative alle soluzioni di tutti i problemi risolti

## Relazione

Il file **relazione.ipynb**, un Jupyter Notebook, contiene il codice sorgente utilizzato per la realizzazione della relazione e dell'elaborazione dei dati  

