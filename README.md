# PyGario 3D

Une copie du fameux jeu `Agario` recréé de A à Z en Python, le tout **en 3D**!
Ce projet a été fondé dans le but d'un concours (`Les trophees NSI, édition 2023`) dans lequel il a remporté le prix de l'ingénierie dans la région Auvergne Rhône-Alpes

Pour voir la présentation détaillée du projet: https://d1t9mwb4xrtjag.cloudfront.net/archives2023/WgrjYjICoGdOQgpO4XBcPywXr1qX3JRDvqBCt1Ny.pdf

## Guide d’installation

Le jeu Pygario est écrit en Python, et utilise le module Ursina. Pour le lancer, il 	faudra premièrement installer Python, puis Ursina.

Installer Python:

Windows :

Si Python est déjà installé sur votre ordinateur, vous pouvez sauter cette étape.

Sinon, téléchargez la dernière version de Python à cette adresse: https://www.python.org/downloads/windows/
Ensuite, ouvrez le fichier python-{version}.exe que vous venez de télécharger sur votre ordinateur.

Puis suivez les intructions d'installation.



Linux :
	
La plupart des distributions Linux ont déjà Python installé, mais si la vôtre 	ne l’a pas, il vous suffit d’ouvrir votre invite de commande et de taper :
		
		Ubuntu/Debian/Fedora → sudo apt install python3
		Arch Linux 		    → sudo pacman -Sy python-pip




Installer Ursina:

	Une fois que Python est installé, vous pouvez lancer cette commande dans votre invite de commande :

		pip install ursina   	OU  	py -m pip install ursina


Enfin executez le script qui permet de lancer le jeu:

 	bash run.sh

Amusez vous bien !!!
	

## Dépendances

- `ursina` - **5.2.0+** - *Moteur de jeu 3D*
