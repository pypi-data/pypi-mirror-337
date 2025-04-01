
Acronyme: FS_01

Titre: **face_sort**

Client(s) :Jerome Fink

Etudiant: **Keunang Tchatchou Farida**

# **I-face_sort**

**Description :**

**face_sort** un outil en ligne de commande ergonomique 
permettant de trier des photos contenant des visages d'humains. Sur base d'un dossier 
contenant des photos, l'application sortira un dossier contenant N sous dossier chacun 
correspondant a un visage unique et contenant les photos sur lesquels ce visage apparait.


l'application permet notament de choisir le modele d'IA a utiliser : entre la distance euclidienne notee **ED**
et le cosinus note **COS** .

il est egalement possible de choisir le seuil type de modele de tri permettant de rendre la recherche plus ou moins concise .
les differentes valeurs du seuil sont :

    - "strict" : permettant une classification beaucoup plus pointue et meticuleuse.
    - "large" : permettant d'opter cette fois ci pour un tri plus souple .
    -  none ,valeur par defaut : lorsque pas precise , une valeur par defaut est attribuee au seuil pour le tri.
    

## **II- Installation**

### Prerequis
- Python 3.8+
- Dependances requises listees dans `requirements.txt`

**Etapes d'installation**

lancer la commande "pip install face_sort" dans le terminal.
installer les Dependances

´´´bash
pip install -r requirements.txt
´´´


## **III- Utilisation**
Apres installation , vous pouvez utiliser face_sort via le terminal avec la commande suivante :


```bash
python -m face_sort /chemin/vers/le/dossier_a_traiter --seuil strict --ia_modele ED
```

### **Explication des parametres**
- **`/chemin/vers/le/dossier_a_traiter`** : Chemin du dossier contenant les photos a trier.
- **`--seuil`** : Niveau de filtrage des visages (options : `strict`, `large`, none par defaut).
- **`--ia_model`** : Modele d'intelligence artificielle utilise pour la reconnaissance (`ED`, `COS`).


Exemple:
```bash
python -m face_sort.main --seuil_type strict --ia_model ED -- "C:\Users\X1 Yoga\Desktop\moi\photos_to_test"
´´´



## **VI- Technologies utilisees**
- Python 3.8+
- OpenCV
- TensorFlow / PyTorch (selon le modele IA utilise)


##**V- Licence**
Ce projet est sous licence **MIT**. 



face_sort

Acronyme : FS_01

Client(s) : Jerome Fink

Étudiant : Keunang Tchatchou Farida

I. Description

face_sort est un outil en ligne de commande permettant de trier des photos contenant des visages humains.

À partir d'un dossier contenant des photos, l'application génère un dossier avec N sous-dossiers, chacun correspondant à un visage unique et contenant les photos où ce visage apparaît.

L'application offre plusieurs options :

Choix du modèle d'IA :

ED : Distance euclidienne

COS : Distance cosinus

Sélection du seuil de tri :

strict : Classification plus précise et rigoureuse.

large : Classification plus souple.

none (par défaut) : Un seuil automatique est appliqué.

II. Installation

Prérequis

Python 3.8+

Dépendances listées dans requirements.txt

Étapes d'installation

Installez face_sort en exécutant :

pip install face_sort

Puis installez les dépendances nécessaires :

pip install -r requirements.txt

III. Utilisation

Une fois installé, exécutez face_sort depuis le terminal :

python -m face_sort /chemin/vers/le/dossier_a_traiter --seuil strict --ia_modele ED

Explication des paramètres

/chemin/vers/le/dossier_a_traiter : Chemin du dossier contenant les photos à trier.

--seuil : Niveau de filtrage des visages (strict, large, none par défaut).

--ia_model : Modèle d'IA utilisé pour la reconnaissance (ED, COS).

Exemple d'exécution

python -m face_sort.main --seuil_type strict --ia_model ED -- "C:\Users\X1 Yoga\Desktop\moi\photos_to_test"

IV. Technologies utilisées

Python 3.8+

OpenCV

TensorFlow / PyTorch (selon le modèle IA utilisé)

V. Licence

Ce projet est sous licence MIT.

