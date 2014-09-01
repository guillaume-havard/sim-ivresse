import string, sys
from modele import *

class Sim:
    """ Interface de simulation en batch d'un modele. 
        On suppose que tous les parametres de simulation sont interne au modele. 
        Contraintes:
          * la classe Modele est dans modele.py 
          * les parametres de Modele.init sont un int de duree de la simulation 
            et une str pour les autres parametres propre au modele
          * la simulation se fait par une boucle sur Modele.update()
          * la boucle de simulation termine lorsque Modele.update() retourne false
    """

    def __init__(self):
        duree = 1 # Durée max de la simulation.
        if (len(sys.argv) == 2):
            self.iteration = int(sys.argv[1])
        else :
            # Erreur.
            print("Un seul parametre")
            pass
            
        self.modele = Modele(duree, 0.0) # initialisation (load) du modele
        self.resultats = Datastore(nom="resultats", entete="")
        self.valTest = ["0.0", "10.0", "20.0", "30.0", "40.0", "50.0", "60.0", "70.0", "80.0", "90.0", "100.0"]
       
    def run(self):
        
        # Écriture des valeurs d'alcolemie testees.
        self.resultats.add(" ".join(self.valTest))
        self.resultats.dump()
        
        for inutile in range(self.iteration) :  
            chaine =""          
            for tA in self.valTest :
                self.modele.tAlcool = float(tA)/100.0
                ok = True
                # boucle infinie de rendering
                while (ok):
                    ok = self.modele.update() # mise a jour du modele                       
                           
                chaine += str(self.modele.tempsR/self.modele.mom.SECtot)                
                chaine += " "
                self.modele.RAZ()
                
            self.resultats.add(chaine) 
            self.resultats.dump()
            print(chaine)
        
            

mySim = Sim()
mySim.run()



