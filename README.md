## 🎄Christmas_Gift_Finder🎁
# A webapp that allows you to describe the gift you want or the person you want to gift it to and get some recommendations !

# Instructions pour faire fonctionner le programme :
- Télécharger le dataset suivant en CSV : https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset?resource=download&select=Amazon-Products.csv et le placer dans le même dossier que le reste des fichiers
- Modifier dans app et extract_criteres_2 le chemin vers le CSV
- Ajouter une clé APIKEY pour faire fonctionner le modèle Mistral.AI
- Dans le terminal (de l'IDE pour le faire fonctionner directement), lancer le fichier app.py : streamlit run app.py
- Vous avez désormais accès au site - ne pas hésiter à rafraîchir la page entre les requêtes pour libérer de la mémoire/rafraichir

## Approche 
- Nous utilisons un dataset de produits Amazon (un peu moins de 400k lignes), qui possède les colonnes 'name', 'ratings', 'actual_price', 'discount_price', 'main_category' et 'sub_category' qui nous intéressent
- 
# Fonction ec.categorie() :
- Dans un premier temps, le traitement d'un dataframe aussi grand est impossible via LLM directement : nous filtrons donc une première fois le dataframe en ne retenant que la catégorie les plus adaptées au prompt utilisateur qui nous est parvenu 
- Ensuite, nous effectuons un traitement similaire mais plus fin sur les sous-catégories -- à partir de la description de l'utilisateur, on extrait les sous-catégories (parmi celles disponibles) pour en extraire les trois les plus pertinentes ==> on obtient désormais *un dataframe filtré ne contenant que les objets pertinents à l'utilisateur, basé sur son prompt*

# Fonction ec.choix():
- Cette fonction nous permet de dégager le produit le plus pertinent pour l'utilisateur
- Elle parcourt l'ensemble des noms d'objets extraits par la fonction categorie, et garde les objets les plus pertinents en comparant le titre et ce que l'utilisateur a décrit pour savoir si cet objet peut correspondre à ses besoins (en générant une petite description à partir du nom de l'objet)
- A partir de l'output de Mistral, on filtre encore une fois le dataframe en ne gardant que l'objet le plus pertinent

## Résultat global de l’application :
# Étapes de traitement
# Saisie utilisateur :

L’utilisateur saisit une description libre, par exemple : "Un cadeau pour un amateur de technologie qui aime les gadgets."
Filtrage initial :

ec.categorie est utilisé pour réduire la taille du dataset en conservant uniquement les catégories et sous-catégories les plus pertinentes.
Sélection du produit principal :

ec.choix permet d’isoler le produit unique qui correspond le mieux à la description donnée.
Traitement des prix :

Les colonnes actual_price et discount_price sont nettoyées (suppression des symboles monétaires comme ₹, des virgules) et converties en format numérique pour faciliter les calculs et les comparaisons.
Présentation des résultats :

# Recommandation principale :
Le produit le plus pertinent est mis en avant avec une présentation complète :
Nom du produit, image, note des utilisateurs, prix réel, prix réduit, et un lien d’achat cliquable.
# Suggestions alternatives :
Les produits restants du dataframe filtré sont présentés en grille pour offrir des options supplémentaires à l’utilisateur.
Message de repli :
Si aucun produit clair ne peut être identifié, un produit par défaut du dataset est proposé.
