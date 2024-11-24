## 🎄Christmas_Gift_Finder🎁
# A webapp that allows you to describe the gift you want or the person you want to gift it to and get some recommendations !

# Instructions pour faire fonctionner le programme :
- Télécharger le dataset suivant en CSV : https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset?resource=download&select=Amazon-Products.csv et le placer dans le même dossier que le reste des fichiers
- Modifier dans app et extract_criteres_2 le chemin vers le CSV
- Ajouter une clé APIKEY pour lancer l'application le modèle Mistral.AI
- Dans le terminal (de l'IDE pour le faire fonctionner directement), lancer le fichier app.py : streamlit run app.py
- Vous avez désormais accès au site - ne pas hésiter à rafraîchir la page entre les requêtes pour libérer de la mémoire/rafraichir

## Approche 
- Nous utilisons un dataset de produits Amazon contenant près de 400 000 lignes, avec des colonnes clés comme name (nom du produit), ratings (notes des utilisateurs), actual_price (prix réel), discount_price (prix avec réduction), main_category (catégorie principale) et sub_category (sous-catégorie).
- L’objectif principal est de permettre à l’utilisateur de décrire une personne ou un cadeau idéal, puis de filtrer les produits pour proposer une recommandation principale ainsi que des suggestions alternatives pertinentes.
- 
# Fonction ec.categorie() :
- Dans un premier temps, le traitement d'un dataframe aussi grand est impossible via LLM directement : nous filtrons donc une première fois le dataframe en ne retenant que la catégorie les plus adaptées au prompt utilisateur qui nous est parvenu 
- Ensuite, nous effectuons un traitement similaire mais plus fin sur les sous-catégories -- à partir de la description de l'utilisateur, on extrait les sous-catégories (parmi celles disponibles) pour en extraire les trois les plus pertinentes ==> on obtient désormais *un dataframe filtré ne contenant que les objets pertinents à l'utilisateur, basé sur son prompt*

# Fonction ec.choix():
- Cette fonction nous permet de dégager le produit le plus pertinent pour l'utilisateur
- Elle parcourt l'ensemble des noms d'objets extraits par la fonction categorie, et garde les objets les plus pertinents en comparant le titre et ce que l'utilisateur a décrit pour savoir si cet objet peut correspondre à ses besoins (en générant une petite description à partir du nom de l'objet)
- A partir de l'output de Mistral, on filtre encore une fois le dataframe en ne gardant que l'objet le plus pertinent

⚠️Il y plusieurs étaps de nettoyage de l'output de Mistral à chaque fois afin qu'il soit utilisable comme index

# app.py :
- Désormais, nous importons notre CSV de données, que nous traitons avec pandas. Nous le traitons ensuite avec les fonctions mentionnées plus haut et on obtient deux dataframes exploitables.
- On extrait alors LE produit le plus pertinent qui est mis en avant par notre application web
- On extrait, selon le nombre de produits à afficher que l'utilisateur a choisi, un certains nombres de produits pertinents de façon aléatoire, que l'on affiche avec le prix, la note des utilisateurs, une photo et le prix avec solde : le nom du produit est un lien clickable qui redirige vers la fiche produit Amazon.
- Nous mettons en place plusieurs vérifications d'erreurs, dans le cas où le dataframe est vide, avec des messages d'erreurs pour guider l'utilisateur vers une tentative fructueuse.






