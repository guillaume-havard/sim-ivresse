""" Modele pour simulation. """

from sbsim import *
from gen import *

class Modele(object):
    """ Modele pour simulation. """

    def __init__(self, duree, mes_params):
        self.iteration = 0
        self.duree = duree                     # nb de jours a simuler
        self.mom = Moment()                  # gestionnaire du temps
        self.mom.dt = 10   # pas de temps = 1 sec
        self.maxiter = 3600 * 24 * self.duree / self.mom.dt   # nb iterations a faire
        self.myGen = GenU01MRG()
        self.tAlcool = float(mes_params)/100.0 # Taux d'alcoolémie de l'individu
                
        # Pour le ration route/trotoire.
        self.tempsR = 0
        
        # Coodonnées du monde
        self.xMonde = 50
        self.yMonde = 50
        self.hauteur = 60
        self.largeur = 900
        self.xMondeMax = self.xMonde + self.largeur 
        self.yMondeMax = self.yMonde + self.hauteur
        self.yRoute = self.yMonde + 40
    
        # Coordonéées de l'individu.
        self.cooIndX = 50.0
        self.cooIndY = 100.0
        self.cooIndT = 0.0
        self.cheminInd = [self.cooIndX, self.cooIndY]
    
        # Pour le premier affichage on fait avancer l'individu d'un pixel.
        self.cooIndX +=1
        self.cheminInd.append(self.cooIndX)
        self.cheminInd.append(self.cooIndY)

    def update(self):
        """ Mise a jour du modele. """
        self.iteration += 1
        self.mom.update() # mise a jour du temps 
        ok = self.iteration < self.maxiter
        
        # Calcul des nouvelles coodonnées.
        # 10 secondes par pas.
        # Le taux d'alcool dans le sang de l'individu à un impact sur sa trajectoire.        
        """
            Effet de l'alcool sur notre individu :            
            ** direction             
                - tAlcool >= 75 %
                    1/5 - 90°
                    1/5 - 45°
                    1/5 droit
                    1/5 + 45°
                    1/5 + 90°
                - 5 % < tAlcool <= 75 %                    
                    1/6 -45°
                    4/6 droit
                    1/6 +45°
                - tAlcool <= 5%
                    va droit.
            ** distance
                - dst = 1 - 1.2 * tAlcool   +   tAlcool * U(0,1)
            L'individu peut aller à réculons s'il est vraiment saoul.
            Mais il tend en moyenne vers les x positifs. 
        """
        
        # Calcul de la direction.
        tmpR = self.myGen.suiv()
        angle = 0.0        
        if self.tAlcool > 0.75 :
            if tmpR < 1/5 : angle = math.radians(-90) 
            elif tmpR < 2/5 : angle = math.radians(-45)
            elif tmpR < 3/5 : angle = math.radians(45)
            elif tmpR < 4/5 : angle = math.radians(90)
        elif self.tAlcool > 0.05 :
            if tmpR < 1/3 : angle = math.radians(-45) 
            elif tmpR < 2/3 : angle = math.radians(45)         
        self.cooIndT = angle                
        
        # Calcul de la distance parcourue.
        tmpR = self.myGen.suiv()
        dst = 1 - (1.2 * self.tAlcool) + (self.tAlcool * tmpR)
                              
        # Calcul de la nouvelle position
        self.cooIndX += dst * math.cos(self.cooIndT)
        self.cooIndY += dst * math.sin(self.cooIndT) 
        
        # On vérifie si l'individu ne sort pas de l'environnement.
        if self.cooIndY < self.yMonde : 
            self.cooIndY = self.yMonde
        elif self.cooIndY > self.yMondeMax : 
            self.cooIndY = self.yMondeMax
      
        # Mise à jour des variables de temps.
        if self.cooIndY < self.yRoute : self.tempsR += self.mom.dt
      
        # Application sur le chemin.
        self.cheminInd.append(self.cooIndX)
        self.cheminInd.append(self.cooIndY)
      
        # On regarde si on n'est pas arrivé à la fin de la rue.
        if ok : ok = self.cooIndX <= self.xMondeMax
    
        if not ok:  # fin de la simulation
            pass
            #print("Fin de la simulation")
            
        return ok

    def renderNow(self, g):
        """ Rendering du modele. """        
        sfont = ('times', 9, 'normal')
        nfont = ('times', 12, 'normal')
        bfont = ('times', 14, 'bold')
        xTxt = 10; yTxt = 20   # position en x, y des lignes de textes
        dyTxt = 20  # interligne pour le texte 
        s = "Simulation (" + str(self.iteration) + ")  " + self.mom.strNow()
        x = xTxt; y = yTxt; 
        g.create_text(x, y, text = s, font = bfont, anchor = 'w')
        
        # Phrase pour le temps passé à tituber.
        s = "Temps passé sur la route :" + str(self.tempsR) + "\n"        
        s += "Temps total passé : " + str(self.mom.SECtot) + "\n"
        if self.mom.SECtot : 
            s += "Ratio : " + str(self.tempsR/self.mom.SECtot) + "\n" 
        s += "Temps en secondes"       
        g.create_text(xTxt, self.yMondeMax + 40, text=s, font=nfont, anchor="nw")        
           
        # Ajout d'un rectangle et d'un ligne pour former notre environnement.                       
        g.create_rectangle(self.xMonde, self.yMonde, self.xMondeMax, self.yMondeMax, outline="black",fill="white", width=2)
        g.create_line(self.xMonde, self.yRoute, self.xMondeMax, self.yRoute,fill="red", width=2)
        
        # Affichage du parcours de l'individu.
        g.create_line(self.cheminInd, fill="blue", arrow="last")
        
    def RAZ(self):
        """ Remet toutes les variables à 0 pour recommencer une autre simulation. """
        self.iteration = 0                   
        self.mom = Moment()                 # gestionnaire du temps 
           
        self.mom.dt = 10   # pas de temps = 1 sec
        self.maxiter = 3600 * 24 * self.duree / self.mom.dt   # nb iterations a faire
        self.myGen = GenU01MRG()   
        
        # Pour le ration route/trotoire.
        self.tempsR = 0
                   
        # Coordonéées de l'individu.
        self.cooIndX = 50.0
        self.cooIndY = 100.0
        self.cooIndT = 0.0
        self.cheminInd = [self.cooIndX, self.cooIndY]
    
        # Pour le premier affichage on fait avancer l'individu d'un pixel.
        self.cooIndX +=1
        self.cheminInd.append(self.cooIndX)
        self.cheminInd.append(self.cooIndY)
        
        
# fin de la classe Modele

