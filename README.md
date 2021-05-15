# Intelligence Artificielle : Abalone avec l'algorithme minimax / alpha-beta pruning

```
    BINOME
        18332 - Maximilien Denis
        20324 - Nick Kuijpers
```

## Introduction 🤠

Dans le cadre du cours d'informatique de deuxième bac en ingénieur industriel, nous devions développer une intelligence artificielle pour le jeu de société **Abalone**.  

## TimeLine 🚀

Nous avons d'abord voulu nous inspirer de l'algorithme développé pour le projet *Alpha-Go Zero* (rendu populaire par Netflix). Une partie de cet algorithme se nomme *Monte-Carlo Tree Search*.  
Malheureusement, que ce soit par le temps ou par le manque de connaissance, nous n'avons pas réussi à aller au bout de nos idées, il a fallu adapter le travail.  
Un autre concept vu en cours nous a semblé plus réaliste. Il s'agit de l'algorithme *mini-max* que nous avons étoffé grâce à *alpha-beta pruning*.

## Minimax 🖱️

### Procédé

- Construction d'une arborescence qui représente l'ensemble des états possibles du jeu à partir du plateau de départ qu'on appelle *root*.
- C'est arbre possède plusieurs éléments :  
    - Les noeuds : ce sont les états du plateau de jeu qui illustrent l'avancement de la partie
    - Les ponts : représentent les interactions entre les noeuds, ici ce sont les **moves** 
    - Les terminaisons : l'état final de la partie (soit un gagnant et un perdant, soit une égalité = *Sumito*)
    - L'heuristique : pour chaque noeud, minimax tente à évaluer la position obtenue appelée heuristique. Elle est basée sur trois principes :
        1. Les pions doivent être le plus proche possible les uns des autres
        2. Ils doivent être proche du centre du plateau de jeu
        3. Récompense supplémentaire s'ils poussent un / des pion(s) adverse(s) en-dehors du plateau
- L'algorithme minimax tente à choisir l'état qui avantage le plus le joueur à partir d'un noeud défini. Nous optimisons cette recherche avec *alpha-beta pruning* qui permet de négliger la recherche dans certains noeuds car nous connaissons déjà la meilleure ou la pire heuristique existante pour le noeud *root* défini.
- Afin de réduire le temps de recherche, les moves qui possèdent les plus grandes chaînes sont prioritaires sur les autres. Leur heuristique est généralement meilleure.
 
![abalone](https://i2.cdscdn.com/pdt2/b/0/2/1/700x700/asab02/rw/asmodee-abalone-jeu-de-strategie.jpg)
