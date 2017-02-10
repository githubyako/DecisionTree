Auteurs : Mariam Bouzid, Nicolas Roux

Implémentation python d'un arbre de décision, avec élagage par réduction d'erreur.
Ne fonctionne que sur des valeurs discrètes. Jeux d'exemples inclus.

Ce projet nécessite Python3 et a été testé avec la version 3.5.2

Il nécessite d'avoir un fichier .arff.

Les instructions se veulent explicites, il suffit de lancer "python3.5 ./projetIA.py" et de répondre au questions,
cependant vous pouvez trouver ci-dessous deux exemples d'interactions avec ce programme.

A noter: Il vous sera proposé de couper en deux le jeu d'exemples pour validation, l'objectif de cette option est de permettre la validation et l'élagage sur un seul jeu d'exemples.
La séparation des exemples étant automatiquement précédée d'un mélange aléatoire des exemples, l'arbre issu du choix de cette option peut varier.


_______________________________

Exemple d'utilisation:
_______________________________
Entrez le path du fichier .arff d'apprentissage:
>> /home/etudiant/data/ML_data/arff/mushroom_train.arff

Voulez-vous utiliser la moitié de ce jeu d'exemple pour validation? (o/n)
>> n

Entrez le path du fichier .arff de validation:
>> /home/etudiant/data/ML_data/arff/mushroom_valid.arff

Souhaitez-vous afficher directement l'arbre? (o/n)

>> n

Stats de l'arbre:
Nombre de noeuds = 476, nombre de feuilles = 678
Précision de l'arbre sur le jeu de validation: 0.787359716479622

Voulez-vous élaguer l'arbre avec le jeu de validation fourni? (o/n)

>> o

Entrez une valeur V telle qu'un noeud devient une feuille si cette opération
	permet une précision d'au moins (précision initiale + V) 
	(ex:précision initiale = 0.78, V = 0.01  ==> précision d'au moins 0.79)

>> V=0.005

Précision objectif = 0.792359716479622

Stats de l'arbre élagué:
Nombre de noeuds = 2, nombre de feuilles = 7, précision = 0.8753691671588896

Voulez-vous afficher l'arbre élagué? (o/n)

>> o

odor = a: 0 (145,18)
odor = l: 0 (141,13)
odor = c: 1 (69,4)
odor = y: 1 (566,63)
odor = f: 1 (13,2)
odor = m: 0 (992,129)
odor = n: 1 (90,12)

_____________________________

Exemple d'utilisation 2:
_____________________________

python3.5 ./projetIA.py
Entrez le path du fichier .arff d'apprentissage:

>> /home/etudiant/data/ML_data/arff/nursery.arff

Voulez-vous utiliser la moitié de ce jeu d'exemple pour validation? (o/n)

>> o

Souhaitez-vous afficher directement l'arbre? (o/n)

>> n

Stats de l'arbre:
Nombre de noeuds = 253, nombre de feuilles = 579
Précision de l'arbre sur le jeu de validation: 0.9584876543209877

Voulez-vous élaguer l'arbre avec le jeu de validation fourni? (o/n)

>> o

Entrez une valeur V telle qu'un noeud devient une feuille si cette opération
	permet une précision d'au moins (précision initiale + V) 
	(ex:précision initiale = 0.78, V = 0.01  ==> précision d'au moins 0.79)

>> V=0.0001

Précision objectif = 0.9585876543209877

Stats de l'arbre élagué:
Nombre de noeuds = 133, nombre de feuilles = 306, précision = 0.9586419753086419

Voulez-vous afficher l'arbre élagué? (o/n)

>> n 
