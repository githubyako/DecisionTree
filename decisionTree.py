import math

class DecisionTree(): 
	# Classe quireprésente l'arbre de décision, 
	# sert en fait surtout de conteneur et d'appelant des méthodes récursives

	def __init__(self,_attNames,_attVals, _classes, _examples): # constructeur
		self.rootNode = None # init d'un conteneur de nodes à vide
		self.attNames = _attNames # stockage des noms d'attributs et de leurs valeurs possibles respectives
		self.attVals = _attVals # stockage des valeurs possibles attribut par attribut
		self.exs = _examples # stockage des exemples
		self.classes = _classes # stockage des noms de classe
		self.valSet = None # set de validation, stocké au moment de la validation
		
	def build(self): # méthode de construction du noeud : construction du noeud racine
		# qui contient donc tous les exemples d'entraînement, tous les attributs, toutes leurs valeurs
		self.rootNode = Node(_attNames=self.attNames, 
			_attVals=self.attVals, 
			_exs=self.exs, 
			_classes=self.classes, 
			_level=0, # ceci sert uniquement à l'affichage indenté de l'arbre
			_av=None) # valeur d'attribut associée à ce noeud, vide donc pour le noeud racine
		self.rootNode.expand() # appel de la méthode de construction récursive

	def print(self): # méthode d'affichage, 
		# ne fait qu'appeler l'affichage du noeud racine (et des autres récursivement)
		print()
		self.rootNode.print()
		print()

	def validate(self, _examples): # méthode de validation
		self.valSet = _examples # assignation du jeu de test
		oks = 0 # nombre d'exemples correctement prédits
		for ex in _examples: # pour chaque exemple du jeu de test
			if self.rootNode.testExample(_ex=ex, _attNames=self.attNames) == ex.getCateg():
				# si l'appel récursif renvoie la bonne classe
				oks +=1	# le compteur est augmenté
		return oks / len(_examples) # retour du ratio (prédictions correctes / taille du jeu de test)

	def getStats(self): # méthode qui renvoie la taille de l'arbre
		nc, lc = self.rootNode.getStats() # appel récursif à nouveau
		nc += 1 # ajout du noeud racine au compteur
		return nc, lc # "node count, leaf count"

	def pruneRate(self, _minNewPrec): # méthode d'élagage via augmentation de précision.
		self.rootNode.pruneRate(_dt=self, _minNewPrec=_minNewPrec) # appel récursif
		
class Node: # noeud, contient des exemples
	def __init__(self, _attNames, _attVals, _exs, _classes, _level, _av): # constructeur
		# rien de particulier ici, si ce n'est que chaque noeud possède ses propres jeux
		# d'exemples, d'attributs et de leurs valeurs correspondantes.
		self.att = None
		self.av = _av
		self.attNames = _attNames
		self.attVals = _attVals
		self.exs = _exs
		self.classes = _classes
		self.noeudsFils = []
		self.level = _level
		self.majClass = "[empty leaf]"
		self.majClassCount = 0
		
	def pruneRate(self,_dt, _minNewPrec): # méthode récursive d'élagage
		temp = list(self.noeudsFils) # stockage temporaire du sous-arbre issu de ce noeud
		self.noeudsFils = None # élagage temporaire de tout le sous-arbre: le noeud devient une feuille
		newprec = _dt.validate(_dt.valSet) # test de la nouvelle précision
		if newprec >= _minNewPrec: # si la nouvelle précision correspond aux exigences
			return # alors ce noeud reste en feuille
		else:
			self.noeudsFils = temp # sinon on récupère le sous-arbre
			for nf in self.noeudsFils: # et on effectue un appel récursif en profondeur d'abord
				nf.pruneRate(_dt=_dt,_minNewPrec=_minNewPrec) # sur les noeuds fils.

	def getStats(self): # méthode incrémentale de récupération du nombre de noeuds/feuilles, RAS
		nbc, nbl = 0, 0
		if self.noeudsFils:
			nbc += 1
			for nf in self.noeudsFils:
				nc, nl = nf.getStats()
				nbc += nc
				nbl += nl
		else:
			nbl = 1
		return nbc, nbl

	def testExample(self,_ex,_attNames): # méthode de validation récursive
		if self.noeudsFils: # si la liste de noeuds fils existe (==si le noeud n'est pas une feuille)
			for i, an in enumerate(_attNames): 
				# récupération de l'indice de la liste GLOBALE de noms d'attributs
				# associée à l'attribut choisi pour ce noeud par meilleur gain d'entropie (voir expand())
				if an == self.att:
					break
			eav = _ex.getAttVals()[i] 
			# récupération de la valeur d'attribut de l'exemple correspondant à l'attribut local
			for nf in self.noeudsFils:
				if nf.av == eav:
					return nf.testExample(_ex,_attNames) 
					# "envoi" de l'exemple au noeud fils associé à la valeur d'attribut qui est celle de l'exemple
		else:
			return self.majClass # si la liste de noeuds fils est vide, c'est une feuille, on renvoie la classe majoritaire

	def isPure(self): # méthode au nom explicite renvoyant un booléen, RAS
		c = self.exs[0].getCateg()
		for ex in self.exs:
			if ex.getCateg() != c:
				return 0
		return 1

	def UpdateMajClass(self): # méthode de calcul de la classe majoritaire (en nombre d'exemples) dans ce noeudet de sa cardinalité
		cc = {} # init du compteur de classes
		for categ in self.classes:
			cc[categ] = 0
		#remplissage du compteur en parsant les exemples
		for ex in self.exs:
			cc[ex.getCateg()] += 1	
		self.majClass = max(cc.keys(), key=(lambda k: cc[k]))
		self.majClassCount = cc[self.majClass]


	def expand(self): # méthode récursive de construction de l'arbre
		self.UpdateMajClass() # mise à jour de la classe majoritaire
		if self.attNames and not self.isPure():
			# s'il reste des attributs non utilisés ET que les exemples du noeud courant ne sont pas tous de la même classe
			attValCount = [] 
			# liste de dictionnaires de dictionnaires d'entiers.
			# compte combien d'exemples de chaque classe correspondent à chaque valeur d'attribut, pour chaque attribut

			#création & init du compteur de valeurs d'attributs
			for att in self.attNames:
				attValCount.append({}) # un dictionnaire par attribut
				for attvalList in self.attVals:
					for i,attval in enumerate(attvalList):
						attValCount[-1][attval] = {} # un dictionnaire par valeur d'attribut
						for categ in self.classes:
							attValCount[-1][attval][categ] = 0 # compteur de chaque classe initialisé à 0

			# init du compteur pour connaître la cardinalité de chaque classe parmis les exemples du noeud courant
			categCounts = {}
			for categ in self.classes:
				categCounts[categ] = 0
				
			#remplissage des 2 compteurs en parsant les exemples

			for ex in self.exs:
				categCounts[ex.getCateg()] += 1
				for i, attval in enumerate(ex.getAttVals()):
					attValCount[i][attval][ex.getCateg()] += 1
			
			#calcul de l'entropie "totale" du noeud courant
			totalent = 0.0
			for categ, count in categCounts.items():
				if count > 0:
					fs = (count / len(self.exs))
					totalent -= fs * math.log2(fs)

			#calcul du gain d'entropie associé à chaque attribut
			gains = []
			for i, att in enumerate(attValCount):# pour chaque attribut
				gains.append(totalent)
				attValTotalcount, ent = {}, {}
				for j, attVal in enumerate(att): # pour chaque valeur d'attribut
					fs = {}
					attValTotalcount[attVal] = 0
					ent[attVal] = 0
					for cat, catCount in attValCount[i][attVal].items(): # pour chaque catégorie
						attValTotalcount[attVal] += catCount
					for cat, catCount in attValCount[i][attVal].items(): # pour chaque catégorie
						if attValTotalcount[attVal] > 0 and catCount > 0:
							fs = catCount / attValTotalcount[attVal] # calcul de proportion
							ent[attVal] -= fs * math.log2(fs) # entropie de la "valeur d'attribut"
					gains[-1] -= (attValTotalcount[attVal] / len(self.exs)) * ent[attVal] # màj du gain de l'attribut

			#Récupération de l'attribut associé au meilleur gain d'entropie
			maxgain = max(gains)
			for i, g in enumerate(gains):
				if g == maxgain: # nous somme sur l'index du meilleur attribut
					break


			self.att = self.attNames[i] # stockage du nom du meilleur attribut
			
			newExs = {}
			# découpage du jeu d'exemples selon les valeurs de l'attribut choisi
			for j, attv in enumerate(self.attVals[i]):
				newExs[attv] = []
			for ex in self.exs:
				newExs[ex.getAttVals()[i]].append(ex)
				del ex.getAttVals()[i]

			# suppression de l'attribut choisi de la liste des attributs disponibles pour les noeuds fils
			newAttNames = list(self.attNames)
			del newAttNames[i]
			newAttVals = list(self.attVals)
			del newAttVals[i]

			# création des noeuds fils
			for j, attv in enumerate(self.attVals[i]):
				# pour chaque valeur de l'attribut choisi
				if len(newExs[attv]) > 0 and newAttNames and self.exs:
					# vérification qu'il y a des exemples à envoyer au noeud fils correspondant à cette valeur d'attribut
					# et qu'il reste un(des) attribut(s) sur le(s)quel(s) les noeuds fils pourront travailler
					newNode = Node( # création d'un nouveau noeud fils
							_attNames=newAttNames, 
							_attVals=newAttVals, 
							_exs=newExs[attv], 
							_classes=self.classes,
							_level=self.level + 1,
							_av=attv
							)
					self.noeudsFils.append(newNode) # ajout du nouveau noeud fils à la liste de noeuds fils
					newNode.expand() # appel de construction récursif de l'arbre sur le nouveau noeud fils

	def print(self): # méthode d'affichage
		self.UpdateMajClass()
		# màj de la classe majoritaire (au cas où il y aurait eu élagage)

		if self.noeudsFils:
			for i, an in enumerate(self.attNames):
				if an == self.att:
					break
			for j, av in enumerate(self.attVals[i]):
				if len(self.noeudsFils) >= j+1:
					nbtabs = 0
					while nbtabs < self.level:
						print("|\t", end = "")
						nbtabs += 1
					eol = "\n"
					if len(self.noeudsFils) >= j+1 and not self.noeudsFils[j].noeudsFils:
						eol = ": "
					print(self.att + " = " + av, end = eol)
					if len(self.noeudsFils) >= j+1:
						self.noeudsFils[j].print()
		else:
			print(self.majClass + " (" + str(self.majClassCount) + "," + str(len(self.exs) - self.majClassCount) + ")")
				
class Example(): # Classe exemple, rien de particulier ici
	def __init__(self,_attVals,_categ):
		self.attVals = _attVals # liste des valeurs d'attributs
		self.categ = _categ # classe de l'exemple

	def getAttVals(self):
		return self.attVals

	def getCateg(self):
		return self.categ
