# Progetto Algoritmi

## PF4EA

< G, w, $ \{ \pi_i \}_{i=i..n} $ , $init$, $goal$, $max$ >

## Compito 1: 

### Generazione di griglie

- Parametri:
  - Dimensione griglia
  - % celle attraversabili
  - fattore di agglomerazione degli ostacoli (quante celle vicine occupa un ostacolo)
- Return:
  - G , w (Rappresentano il grafo pesato)

### Generatore di istanze

- Dato un generatore di griglie crea anche i percorsi degli agenti (In caso compito 3)

### Soluzione 

- un percorso $ \pi_{n+1} $ per un agente $ \alpha_{n+1} $ senza collisioni con gli altri $ n $ agenti
- gli altri percorsi rimangono invariati
- $w(\pi_{n+1})$ costo minimo tra i percorsi che iniziano in $init$ e finiscono in $goal$ e hanno lunghezza al più uguale a $\max$
- $\nexists$ soluzione se:
  - La cella init/goal coincide con la cella di partenza/arrivo di un altro agente
  - Le celle init e goal sono irraggiungibili tra loro
  - $ max < w(\pi_{n+1}) $
  - le celle degli altri agenti diventano una barriera  e quindi init e goal diventano irrangiugibili

## Algoritmo ReachGoal

- Input: problema PF4EA
- Ricerca A* nello spazio $V \times \mathbb{N}$ ( il tempo ha come dominio i numeri naturali )
- Due liste di stati, dove lo stato è < *vertice* , *istante temporale* >:
  - *Open*,  contiene gli stati da espandere
  - *Closed*, contiene gli stati già espansi
- Due strutture dati:
  - $g(<v,t>)$ il costo più basso per raggiungere il vertice $v$ all'instante $t$ partendo da $init$ all'istante zero
  - $P(<v,t>)$ lo stato genitore di $<v,t>$ nell'albero dei cammini minimi
- Funzioni:
  - **euristica** $h(v,goal)$: stima del costo da $v$ a $goal$, il valore di $h(v,goal)$, non cambia durante l'esecuzione
  - **score** $f(<v,t>)$: è la somma $g(<v,t>)$ + $h(v,goal)$ ed è la stima del costo del percorso minimo tra $init$ e $goal$ passando per il vertice $v$ all'istante $t$, questa funzione può decrescere se $g(<v,t>)$ decresce  
  - $\sum$ è l'insieme degli $n$ agenti il cui percorso è noto a priori
- Output: percorso di costo minimo conforme ai vincoli oppure 0

### Pseudocodice

```
ReachGoal(G, w, list_path , init, goal, max){
	# Setup senza controllo del init degli altri agenti
	Closed <- {};
	Open <- { < init, 0 > };
	for t=0 to max do
		foreach v in V[G] do
			g(<v,t>) <- INFINITY;
			P(<v,t>) <- nil;
		end
	end
	g(<init,0>) <- 0;
	f(<init,0>) <- h(init, goal);
	
	# Estazione dello stato open e controllo di goal
	while Open != {} do
		<v,t> <- lowest f-score in Open
		Open <- Open \ {<v,t>};
		Closed <- Close U {<v,t>};
		if v==goal then
			return RecostructPath(init, goal, P, t)
		end
		###
		###
			compute a relaxed path pi_R from v to goal;
			if pi_R is collision-free then
				return RecostructPath(init, v, P, t) + pi_R
			end
		###
		###
		if t < max then
			foreach n in Adj[v] do
				if <n,t+1> not in Closed then
					traversable <- true;
					foreach agent in \sum do
						# manca il controllo se si entri in collissione con un agente fermo nel suo goal
						if l_{t+1}(agent) == n || (l_{t+1}(agent) =) v && l_t(agent) == n) then
							traversable <- false
                        end
                    end
                    if traversable then
                    	if g(<v,t>) + w(v,n) < g(<n,t+1>) then
                    		P(<n,t+1>) <- <v,t>;
                    		g(<n,t+1>) <- g(<v,t>) + w(v,n);
                    		f(<n,t+1>)<- g(<n,t+1>) + h(n,goal);
                    	end
                    	if <n,t+1> not in Open then
                    		Open <- Open U {<n,t+1>};
                    	end
                    end
                end
            end
        end
    end
    return fail;	
}
```



## Compito 2

- Implementare ``` ReconstructPath(init, goal,P,t )```
- Implementare l'algoritmo, attenzione alla memoria di:
  - dimensione della griglia
  - orizzonte temporale $max$
  - lunghezza della soluzione
- $h$​ euristica ammissibile (percorso ottimo) e consistente (per vistitare ogni stato al più una volta)
  - Distanza diagonale
  - Lunghezza del cammino minimo (senza altri agenti)*
  - Costo del cammino minimo (cammino rilassato)*

*h(n, goal) si può calcolare prima su tutti i nodi

## Compito 3

- Implementare un algoritmo per il rilassato
- verificare se un cammino entra in conflitto 

## Consegne

- Prove di esecuzione dei 3 compiti con valutazione delle prestazioni temporali e spaziali
- Info aggiuntive 
  - cicli alla riga 12, ovvero la dimensione massima raggiunta dalla lista *Closed*
  - numero di stati inseriti nella lista open, il numero di nodi dell'albero dei cammini minimi
  - lunghezza e costo del percorso
  - mosse di wait
- Altri parametri interessanti
  - Dimensione della griglia
  - Densità del grafo
  - Numero di agenti
  - Lunghezza dei percorsi degli agenti preesistenti
  - Valore dell'orizzonte temporale $max$
