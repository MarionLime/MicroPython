
# MicroPython

____________________________________________________________________
 
## Présentation du projet :
 
Ce projet a été réalisé dans le cadre de notre validation de fin d’année du cours de MicroPython orchestré par Mr POULAILLEAU, intervenant auprès de notre classe de 3e année cycle dans la filière de Robotique de l’école Ynov de Bordeaux.

Il nous a été demandé de réaliser un jeu à l’image du célèbre Space Invaders. Qui consiste à éliminer des aliens grâce à notre petit vaisseau. Pour ce faire, nous avons eu comme « contrainte » d’utiliser comme manette, une carte STM32F407-DISC équipée d’un accéléromètre lis3dsh qui lorsque nous penchons la carte de la gauche vers la droite, déplace notre petit vaisseau spatial.

____________________________________________________________________

Ce projet a été réalisé sur l'OS Windows10.
Les instructions pour lancer le jeu sont donc adaptés à ce système d'exploitation.

La carte STM32F407G-DISC n'est pas prévu initialement pour recevoir un programme en python , c'est pourquoi lors de nos cours, nous avons dû au préalable faire quelques manipulation, qui vous seront également necessaires afin de faire fonctionner le jeu.

1 - Téléchargez dans un premier temps, le programme de flashage :
    https://github.com/micropython/micropython/blob/cdaec0dcaffbfcb58e190738cf6e9d34541464f0/tools/pydfu.py
2 - Créez un environnement virtuel, avec un shell
    cd  dossier_que_vous_voulez
    python3.8 -m venv venv  
3 - Activez l'environnement virtuel
    .\venv\scripts\activate.ps1 
(venv) est ajouté au début du promptpip  
    pip install pyusb==1.1.1  
4 - Sur STM32F4 Discovery télécharger la dernière version stable
      https://www.micropython.org/download#other
5 - Débranchez la STM32F4 Discovery et mettez un jumper(du TERM par exemple) entre VDD et BOOT0 (header de droite de la carte)
6 - Branchez un câble mini-USB en haut de la STM32F4-Discovery (alimentation electrique)
7 - Branchez un câble micro-USB en bas de la STM32F4-Discovery (pour le flashage)
8 - Rentrez les commandes suivantes dans le terminal powershell:
    python pydfu.py --list ( Affiche la liste des périphériques en mode DFU)
    python pydfu.py --upload STM32F4DISC-20210222-v1.14.dfu (télécharge le fichier que vous avez pris sur le site STM, a adapté)
9 - A la fin du flashage, ejectez la clé USB en passant par le clic droit et retirer le jumper avant de faire un reset (bouton noir)
10 - télécharger le dépôt et remplacer le main.py de la clé
11 - Ejectez a nouveau la clé, puis rappuyer sur reset.

Ces étapes fini, téléchargerPuTTy : https://www.putty.org/
Regarder dans votre gestionnaire de périphérique "USB Serial Port"
Lancer PuTTY et rentrer les paramètres suivant:
  Serial line : otre port COM)
  Speed : 115200
  Connection type : Serial 
  
Enregistrer , cliquer sur "Open" et....


Let's play !

______________________________________________________________________________________________
______________________________________________________________________________________________

## Difficultés rencontrées et retour d'expérience

Pour ce projet, ma plus grande difficulté a été matérielle, en effet, mon ordinateur avait énormément de mal a reconnaître ma carte, ce qui a fait que j'ai travaillé en majorité à l'aveugle. J'ai également encore beaucoup à apprendre et comprendre sur ce langage qui fait que ma logique est encore à travailler, et le fait que l'année, ce soit majoritairement déroulé à distance à ajouter quelques obstacles. Je n'ai pas réussi a afficher quoi que ce soit correctement lorsque ma connexion fonctionnait.

Malgré tout, même si je n'ai pas réussi à faire fonctionner mon projet à temps, il est tout de même très intéressant et je compte bien essayer de le faire marcher.
C'est, je pense un excellent entraînement pour apprendre à utiliser les classes, les clocks, comprendre le fonctionnement des protocoles de communication ou encore apprendre à se servir des registre d'une carte e, fonction de nos besoins. J'espère réussir à faire fonctionner le projet dans l'été voir l'améliorer. Ce qui serait parfait pour s'entraîner pour les années à venir.
_____________________________________________________________________________________________
_____________________________________________________________________________________________
