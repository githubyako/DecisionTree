import decisionTree as dt
import sys
import csv
import re
import random

def readArff(_fname): # fonction de parsing pour extraire les données du fichier .arff
	try: 
		f = open(_fname, "r") # ouverture fichier
		attNames, attVals, classes, examples = [], [], [], []
		# atts = tableau associatif de {[nom_attribut], ['valeur 1', ..., 'valeur n']}
		# classes = ['valeur possible 1', ..., 'valeur possible n'}
		# examples = liste de {[valeur attribut 1], ... , [valeur attribut n], [classe]}
		rows = f.read().splitlines()
		for i, row in enumerate(rows): # pour chaque ligne
			if row and row[0] == '%': # si ligne non vide && commentaire, on ignore
				continue
			elif row and row[0] == '@': # sinon si ligne non vide && commence par @
				l2 = row.lower()
				l2 = re.sub('\s+', ' ', l2)
				l2 = re.sub(',', ' ', l2)
				l2 = re.sub(' +', ' ', l2)
				l2 = re.sub('\'', '', l2)
				l = l2.split(' ') # on split la ligne
				#print(l2)
				if l[0] == '@attribute' and rows[i+1] != "": #on vérifie que c'est bien une description d'attribut
					attVals.append((re.sub('[{},]', '', l2)).split(' ')[2:]) # récupère les valeurs possibles de l'attribut
					attNames.append(l[1])
				elif l[0] == '@attribute' and rows[i+1] == "":
					classes = (re.sub('[{},]', '', l2)).split(' ')[2:]
			elif row: # dans ce cas, c'est un exemple
				l = re.sub('\'', '', row)
				l = l.lower()
				l = l.split(',') # on split by ','
				c = l.pop() # récupération de la classe de l'exemple dans c
				e = dt.Example(l,c) # création d'un objet Exemple (voir classe dans decisionTree.py) avec les valeurs d'attributs et la classe
				examples.append(e) # ajout de cette exemple à la liste d'exemples
			prevrow = row
		f.close()
		return attNames, attVals, classes, examples

	except ValueError:
		print ("Impossible d'ouvrir/lire ce fichier. Vérifiez qu'il existe et vos droits d'accès dessus.")

print ("Entrez le path du fichier .arff d'apprentissage:")
trainset = input(">> ")

answ=None
while answ != "o" and answ != "n":
	print("Voulez-vous utiliser la moitié de ce jeu d'exemple pour validation? (o/n)")
	answ = input(">> ")
splitexs = (answ == "o")

attNames, attVals, classes, examples = readArff(trainset)

examples2 = None
if splitexs:
	random.shuffle(examples)
	examples2 = examples[:int(len(examples)/2)]
	examples = examples[int(len(examples)/2):]
else:
	print ("Entrez le path du fichier .arff de validation:")
	valset = input(">> ")
	attNames2, attVals2, classes2, examples2 = readArff(valset)

dt1 = dt.DecisionTree(_attNames=attNames, _attVals=attVals, _classes=classes, _examples=examples)
dt1.build()
print()
of = None
print("Souhaitez-vous afficher directement l'arbre? (o/n)")
while of != "o" and of != "n":
	of = input(">> ")
if of == "o":
	print("Arbre de décision non élagué:")
	dt1.print()

nbnodes, nbleaves = dt1.getStats()
print("\nStats de l'arbre:\nNombre de noeuds = " + str(nbnodes) + ", nombre de feuilles = " + str(nbleaves))
	

precision = dt1.validate(examples2)

print("Précision de l'arbre sur le jeu de validation: " + str(precision))
print()
inp=None
while inp != "o" and inp != "n":
	print("Voulez-vous élaguer l'arbre avec le jeu de validation fourni? (o/n)")
	inp = input(">> ")
prune = (inp == "o")
if prune:
	print("Entrez une valeur V telle qu'un noeud devient une feuille si cette opération\n\t"+
		"permet une précision d'au moins (précision initiale + V) \n\t"+
		"(ex:précision initiale = 0.78, V = 0.01  ==> précision d'au moins 0.79)")
	v = float(input(">> V="))
	print("\nPrécision objectif = " + str(precision + v))
	dt1.pruneRate(_minNewPrec=(precision + v))
	nbnodes, nbleaves = dt1.getStats()
	print("\nStats de l'arbre élagué:\nNombre de noeuds = " + 
		str(nbnodes) + ", nombre de feuilles = " + str(nbleaves) + 
		", précision = " + str(dt1.validate(examples2)))
	inp=None
	while inp != "o" and inp != "n":
		print("\nVoulez-vous afficher l'arbre élagué? (o/n)")
		inp = input(">> ")
	if inp == "o":
		dt1.print()

"""
/home/etudiant/data/ML_data/arff/weather.nominal.arff
/home/etudiant/data/ML_data/arff/tic-tac-toe.arff
/home/etudiant/data/ML_data/arff/coup_de_soleil.arff
/home/etudiant/data/ML_data/arff/contact-lenses.arff
/home/etudiant/data/ML_data/arff/nursery.arff
/home/etudiant/data/ML_data/arff/mushroom_train.arff
/home/etudiant/data/ML_data/arff/mushroom_valid.arff
"""