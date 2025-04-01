# INFOB318-template

Acronyme: FS_01
Titre: sort_my_face
Client(s) :Jerome Fink
Étudiant: Keunang Tchatchou Farida

# 📌 sort_my_face

**Description :**

sort_my_face un outil en ligne de commande ergonomique 
permettant de trier des photos contenant des visages d'humains. Sur base d'un dossier 
contenant des photos, l'application sortira un dossier contenant N sous dossier chacun 
correspondant à un visage unique et contenant les photos sur lesquels ce visage apparait.


l'application permet notament de choisir le modèle d'IA a utiliser : entre la distance euclidienne notée ED
et le cosinus noté COS .

il est egalement possible de choisir le seuil type de modèle de tri permettant de rendre la recherche plus ou moins concise .
les differentes valeurs du seuil sont :
    - "strict" : permettant une classification beaucoup plus pointue et meticuleuse.
    - "large" : permettant d'opter cette fois ci pour un tri plus souple .
    -  none ,valeur par defaut : lorsque pas precisé , une valeur par defaut est attribuée au seuil pour le tri.
    

## 🚀 Installation

## Prérequis
- Python 3.8+
- Dépendances requises listées dans `requirements.txt`

## Étapes d'installation
lancer la commande "pip install sort_my_face" dans le terminal.
#installer les Dépendances
pip install -r requirements.txt


### 🎯 Utilisation
Apres installation , vous pouvez utiliser sort_my_face via le terminal avec la commande suivante :

bash
sort_my_face "C:\Users\X1 Yoga\Desktop\moi\photos_to_test" --seuil_type strict --ia_model ED
´´´´

### Explication des paramètres
- **`/chemin/vers/le/dossier_a_traiter`** : Chemin du dossier contenant les photos à trier.
- **`--seuil`** : Niveau de filtrage des visages (options : `strict`, `large`, none par defaut).
- **`--ia_model`** : Modèle d'intelligence artificielle utilisé pour la reconnaissance (`ED`, `COS`,  none par defaut).

Exemple :
```bash
python -m sort_my_face ~/Images/photos_to_test --seuil strict --modele ED
```

## 📌 Technologies utilisées
- Python 3.8+
- OpenCV
- TensorFlow / PyTorch (selon le modèle IA utilisé)


#### 📜 Licence
Ce projet est sous licence **MIT**. 
