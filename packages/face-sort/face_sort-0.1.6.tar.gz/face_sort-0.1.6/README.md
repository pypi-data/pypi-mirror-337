
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
python -m face_sort /chemin/vers/le/dossier_a_traiter --seuil strict --modele ED
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
