Simulation homme ivre
=====================

Introduction
------------

Le but de cette simulation est de simuler le trajet d'une personne ayant bu 
sur une rue de Paris. On va regarder la proportion de chemin qu'il va faire
sur la route, qui comme nous le savons est dangereuse, par rapport à celle 
qu'il ferra sur le trottoir.
On pourra ainsi déterminer la probabilité d'un individu saoul à marcher sur la
route et ainsi courir le risque de se faire percuter par une voiture.


Variables du systèmes
---------------------
Identification des paramètres de notre système.

Variables indépendantes :

* temps
* espace (notre rue, constitué de la chausée et du trottoir)

Variables d'état :

* Position de l'individu
* taux d'alcoolémie (en %, 0 : sobre 100 : dangereux pour la santé !)

Hypothèses
----------

Voici les principales hypothèse que j'ai dressées :

* Le taux d'alcoolémie est constant durant la simulation.
* L'individu doit arriver de l'autre coté de la rue pour terminer la 
simulation.
* L'individu ne peut pas sortir de notre environnement (rue) sauf par la 
sortie.
* On considère que l'individu fait un pas toutes les 10 secondes.
* La variation du mouvement dépend du taux d'alcoolémie de l'individu.
* Si le taux d'alcoolémie est nul l'individu doit aller droit.
* La moyenne de la variation du mouvement tend vers 0 pour l'angle et vers 
les 'y' croissant pour la position (sinon l'individu peut ne pas sortir)

Le modèle
---------
Fonction update :  
La fonction update est appelée à chaque itération de notre simulation, c'est 
le cœur calculatoire du programme.  
La fonction retourne Vrai si la simulation doit continuer et Faux si elle doit
s'arrêter. J'ai donc mis les conditions d'arrêt du programme à savoir si le 
temps imparti à la simulation est épuisé ou si l'individu sort de la route.  
Le deuxième point de la fonction est de calculer la position de notre individu
après un pas.  
La direction et la taille de ce pas dépendent de son taux d'alcoolémie. Il n'y
a pas d'étude mathématique sur la marche de personnes saoul et je n'ai pas les
résultats de tests réel, de plus le 'taux d'alcoolémie' n'a pas vraiment de
signification. Le modèle à donc été créé suivant le bon sens.  
Pour m'amuser j'ai décider que la perturbation de distance se fera de façon
continue avec le taux d'alcoolémie et que la perturbation évoluerait de façon
discrète avec le taux d'alcoolémie.

-Perturbation en direction :  
Si le taux d'alcoolémie est supérieur à 75% il y 1 chance sur 5 que l'individu 
aille droit et 1/5 chance qu'il aille à -90deg, +90deg, -45deg ou +45deg.  
Si le taux d'alcoolémie est entre 5 % et 75% inclus il y a 1 chance sur 3 que
l'individu aille droit et 1/3 chance qu'il aille à -45deg ou +45deg.  
Si le taux d'alcoolémie est entre 0 et 5% inclus l'individu va droit.

-Perturbation en distance :  
Cette fois si la relation est continue et suis la formule suivante :
distance parcourue : 1 – (1,2 * %alcool) + (%alcool * U(0,1))  
Si %alcool = 0 notre individu avance toujours de 1 m par pas.  
Sinon la variation augmente avec le taux d'alcoolémie et tends à ce ralentir.
Au maximum (%alcool = 100) l'individu peut faire entre -0,20 m (il recule) et 
0,80 m.

les nouvelles coordonnées sont stockées dans une liste pour un futur affichage

La vue
------
Fichier SimTxt.py
Permet de lancer une interface graphique pour lancer la simulation.  
Necessite `tkinter`.

>>> python3 SimTxt.py

La simulation sans vue
----------------------
Fichier SimTxtr.py

>>> python3 SimTxtr.py nb-iter

Cela fera nb-iter tests pour tous les taux d'alcoolémie de 0 à 100 avec un pas
de 10, 'X' étant donné en paramètre au lancement du script.   
Les résultats sont affiches dans le terminal, ils sont aussi stockés dans un 
fichier 'resultats.csv' avec les différents tests rangés en colonne par 
%alcool.  
(Mieux vaut rediriger la sortie standard vers un fichier)


Validation
----------
Pour la validation j'ai fait des test à différentes valeurs, n'yanat pas de va 
leur comparative je ne peux pas dire que le modèle est valide.
Cependant l'individu déambule plus ou moins vite en fonction de son taux 
d'alcoolémie et se dirige globalement vers la bonne destination. De plus il ne
semble pas faire deux fois la même trajectoire, démontrant bien l'état
probabiliste de notre système. On peut aussi noté que si son taux d'alcoolémie
est nul l'individu se déplace droit.

Analyse des résultats
---------------------
Deux tests on été fait sur 100 et 1000 valeurs puis des courbes de la moyenne
du temps passé sur la route en fonction du taux d'alcolemie sont utilisees
pour tirer les conclusions suivantes.

La première chose que l'on remarque en regardant la courbe est que nos
résultats ne semble pas suivre le principe "plus je suis saoul, plus j'ai de
chance de marcher sur la route". en effet de 10 à 70 % l'individu passe un
temps de plus en plus faible sur la route, phénomène que je n'avais pas
remarqué enfaisant des tests simples avec l'interface graphique.  
Cependant les effets de l'alcool ne sont pas rationel, j'ai donc décidé de
garder mon modèle tel quel.  
En regardant nos courbes de résultats on peut voir que l'individu passe un
temps plus important sur le trottoir plus il a bu et ce jusqu'à 70 de taux
d'alcoolémie, il passe d'un ratio d'environ 20% à 15%. Cependant après avoir
dépassé cette limite il passe à un ratio important d'environ 30 %.  
Ceci s'explique du au choix de perturbation que j'ai fait, de 5 à 75%
d'alcoolémie l'individu a les mêmes variation de direction, cependant sa
perturbation de distance est plus importante ce qui à tendance à la diminuer.
Notre individu fait donc de plus en plus petit mouvement. Un fois dépassé la
borne de 75% il commence a faire des variation de direction importantes ce
qui, même avec une distance moyenne faible, l'entraine souvent sur la route.  
Biologiquement, On pourrait interpréter ce phénomène par un engourdissement
progressif de l'humain proportionnel à son taux d'alcoolémie, ce qui le
ralentirai, cependant après avoir dépassé limite (75%) il se mettrait en sur
régime et déambulerait dans tous les sens. Pour conclure, il faut boire,
beaucoup, mais pas trop !





