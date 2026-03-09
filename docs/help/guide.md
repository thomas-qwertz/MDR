<style>
  .md-content__button {
    display: none;
  }
  .inline {
    width:47% !important;
  }
</style>

# Guide de contribution

La collaboration est au cœur du projet MDR. Si vous disposez d'expérience dans le domaine de la recherche techno-pédagogique, nous vous encourageons vivement à participer. Cette page rassemble donc diverses informations et conventions destinées à guider les personnes qui souhaitent contribuer.

!!! info "Vous connaissez déjà GitHub ?"

    La première partie de ce guide présente les bases de fonctionnement d'un dépôt GitHub. Si vous déjà savez modifier les fichiers d'un dépôt, vous pouvez directement passer à la partie **[Conventions de contributions](#conventions-de-contributions)**.






## Modifier et ajouter des pages depuis GitHub

Ce site est hébergé sur GitHub et généré automatiquement d'après les fichiers qui se trouvent dans le [dépôt du projet MDR :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR). Vous pouvez contribuer et apporter des modifications aux pages. Voici comment faire :

1. Rendez-vous sur le dépôt GitHub du projet (lien ci-dessus).
2. Naviguez vers le fichier que vous souhaitez modifier. Les fichiers sont généralement dans le dossier `/docs`.
3. Cliquez sur l'icône du crayon pour commencer à modifier le fichier.
4. Après avoir apporté vos modifications, descendez vers le bas de la page et cliquez sur "Propose Changes". Donnez un titre et une description à vos modifications.
5. Vous serez redirigé vers une nouvelle page. Cliquez sur "Create Pull Request" et donnez un titre et une description à votre Pull Request.
6. Attendez que vos modifications soient approuvées par un administrateur.

Note : Vous aurez besoin d'un compte GitHub pour effectuer ces actions. Si vous n'en avez pas, vous pouvez en créer un gratuitement sur GitHub.

### Fonctionnement général de GitHub

GitHub est une plateforme qui héberge des dépôts Git et facilite la collaboration sur le code. Pour ce projet, chaque contributeur travaille en local sur une copie du dépôt (clonée depuis GitHub) et peut synchroniser ses modifications avec le dépôt distant. Cela permet de suivre les changements, proposer des ajouts via des pull requests, et s'assurer que tout le monde travaille sur une base de code à jour.

Pour en savoir plus, consultez les [guides de GitHub :octicons-link-external-16:](https://docs.github.com/en/get-started/start-your-journey/about-github-and-git).

### Syntaxe de base en Markdown (et/ou HTML)

Les pages du projet sont principalement écrites en Markdown, un langage léger et simple pour formater du texte. Voici quelques éléments courants :

**Titres :**<br>
`# Titre principal`, `## Sous-titre`, `### Titre de niveau 3`.

**Listes :**<br>
À puces : `- Élément X` ou `* Élément Y`<br>
Numérotées : `1. Élément 1`

**Liens :**<br>
`[Texte du lien](https://exemple.com)`

**Images :**<br>
`![Texte alternatif](chemin/vers/image.jpg)`

**Texte enrichi :**<br>
Gras : `**texte en gras**`<br>
Italique : `*texte en italique*`<br>
Code : ```` `exemple de code` ````<br>

Vous pouvez aussi intégrer du HTML directement dans une syntaxe Markdown (le retour à la ligne `<br>` est par exemple très utile).

Pour approfondir :<br>
[Guide Markdown officiel :octicons-link-external-16:](https://www.markdownguide.org/basic-syntax/)



## Conventions de contributions

Lorsque vous contribuez au projet MDR, il est important de suivre certaines règles et directives pour favoriser la cohérence et la qualité du contenu. Voici comment structurer vos contributions pour qu'elles s'intègrent harmonieusement au reste du projet.

### Structure de page attendue

<div class="annotate" style="margin-top:1.1rem" markdown>
```
---
tags:
  - Administratif (1)
  - Conception
  - Formation
  - Recherche
  - Usages multiples
---

![Titre image](https://dummyimage.com/300x300){ width=300, align=right } (2)

# Titre de la page (= nom de la ressource)

**Description :** Description brève et informative.

## Objectif

Description de l'objectif de la ressource.

## Durée/moment d'utilisation

Indication sur quand et combien de temps utiliser cette ressource.

## Limites

Discussion des limites ou des situations où la ressource n'est pas judicieuse.

## Remarques

Toutes autres remarques pertinentes.

## Personnes ressources

- Nom (et éventuellement fonction)
- Nom (et éventuellement fonction)

!!! quote "Retours d'expériences"
    === "Nom de la personne"
        *Retour d'expérience.*

    === "Nom d'une autre personne"
        *Autre retour d'expérience.*

## Liens vers la ressource

[Texte du lien :octicons-link-external-16:](https://exemple.com/) (3)

??? references "Références"
    - Référence X aux normes APA
    - Référence Y aux normes APA
```
</div>
1.  :fontawesome-solid-triangle-exclamation: Dans le code de votre nouvelle page, **supprimez les catégories qui ne correspondent pas à la ressource**.
2.  Une petite image placée avant le titre de la page s'alignera avec ce dernier. Exemple : page [Persona](../biblio/persona.md).
3.  Ajouter l'icône "**:octicons-link-external-16:**" (`:octicons-link-external-16:`) dans le texte d'un lien permet d'indiquer aux utilisateurs qu'il s'agit d'un **lien externe**.

!!! warning "Ne pas oublier les catégories !"

    Il est essentiel d'attribuer une ou plusieurs catégories à chaque nouvelle page créée pour aider à son organisation et à sa recherche dans le projet. Utilisez le bloc **tags** au début de votre page (avec les espaces et les tirets) pour indiquer les catégories pertinentes, en choisissant parmi celles définies par l'équipe.
    

### Arborescence du dépôt

<div style="margin-top:-0.8em;text-align:left" markdown>
!!! success inline end "Où placer/trouver les pages de ressources<br>et les images"
    - **Pages des ressources** :<br>dossier **`docs/biblio/`**<br>
    _Exemple de chemin pour lien interne depuis une page de ressource :_<br>
    **`[Persona](persona.md)`**
    - **Images** :<br>dossier **`docs/assets/images/`**<br>
        <li style="list-style-type: none">_Exemple de code à utiliser dans une page :_<br>
        **`![exemple](../assets/images/exemple.jpg){ width=300, align=right }`**</li>
</div>

<div class="annotate" style="margin-top:1.95rem" markdown>
``` 
MDR
├─ .github/
│  └─ workflows/
│     └─ ci.yml (1)
├─ docs/ (2)
│  ├─ assets/ (3)
│  │  └─ images/ (4)
│  ├─ biblio/ (5)
│  │  └─ index.md (et autres pages) (6)
│  ├─ css-and-js/ (7)
│  ├─ help/ (8)
│  │  ├─ apropos.md (9)
│  │  ├─ guide.md (10)
│  │  └─ index.md (11)
│  ├─ categories.md (12)
│  └─ index.md (13)
├─ mkdocs.yml (14)
└─ README.md (15)
```
</div>
1.  `ci.yml` : Fichier de configuration qui permet au site d'être actualisé automatiquement après un "merge" ou "push" dans le dépôt GitHub.<br>[En savoir plus :octicons-link-external-16:](https://squidfunk.github.io/mkdocs-material/publishing-your-site/)
2.  `docs/` : Dossier principal contenant le contenu du site.
3.  `assets/` : Dossier pour divers fichiers nécessaires au site (logo, backgrounds, etc).
4.  `images/` : Dossier où stocker **les images utilisées dans les documents.** :material-check-decagram:
5.  `biblio/` : **Dossier qui contient les pages de chaque ressource du projet MDR.** :material-check-decagram:
6.  `index.md` : La page `index.md` du dossier `biblio/` est la page qui regroupe la liste des ressources classées par ordre alphabétique (*updatée automatiquement* lorsqu'une nouvelle ressource est ajoutée). Les autres pages sont **les ressources** elles-mêmes.
7.  `css-and-js/` : Dossier pour les fichiers CSS et JavaScript personnalisés du site.
8.  `help/` : Dossier qui contient les pages d'information et d'assistance, telles que ce guide.
9.  `apropos.md` : La page "À propos" du site 🙂
10.  `guide.md` : La présente page 🙂
11.  `index.md` : La page `index.md` du dossier `help/` correspond à la page "Contribuer/Discuter" du site.
12.  `categories.md` : Page listant les différentes catégories de ressources (*updatée automatiquement* si des "tags" sont présentes dans la page d'une ressource).
13.  `index.md` : La page d'accueil du site (appartient au dossier `docs/`, à ne pas confondre avec les pages `index` d'autres dossiers).
14.  `mkdocs.yml` : Fichier de configuration pour MkDocs, définissant la structure et les paramètres du site.
15.  `README.md` : Fichier contenant des informations générales sur le projet, visible sur la page principale du dépôt GitHub.

!!! failure "Modifications hors pages ressources"

    Pour assurer le bon fonctionnement du site, merci de ne pas modifier les fichiers hors du dossier `docs/biblio/`.<br>
    Si vous souhaitez proposer des changements non spécifiques aux ressources, ouvrez d'abord une [discussion :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR/discussions) pour en parler !

### Autres conventions

* Ajouter l'icône "**:octicons-link-external-16:**" (`:octicons-link-external-16:`) dans le texte d'un lien permet d'indiquer aux utilisateurs qu'il s'agit d'un **lien externe**.

* Les contributions des personnes disposant des droits d'administration devraient **elles aussi** passer par des pull requests (et non pas "_Commit directly to the main branch_"), sauf s'il s'agit de modifications mineures (corrections orthographiques, mise à jour de lien...).

## Et après ? Tâches des administrateurs/responsables

La gestion et la révision des contributions reçues sur GitHub constituent une responsabilité clé des administrateurs et des responsables du projet MDR. Voici une vue d'ensemble des étapes et des meilleures pratiques pour examiner et intégrer efficacement les propositions de modifications soumises par la communauté.

### Validation des contributions

:octicons-git-pull-request-16: **Réception d'une pull request** : Lorsqu'une nouvelle contribution est soumise, elle apparaît dans la section [Pull requests :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR/pulls) du dépôt GitHub du projet. Les administrateurs sont notifiés et peuvent commencer le processus d'examen.

:material-numeric-1-circle: **Vérification du contenu** : Assurez-vous que le contenu proposé est pertinent, exact, et apporte une valeur ajoutée au projet. Cela peut nécessiter une lecture approfondie du contenu, une vérification des faits, ou une consultation avec d'autres membres de la communauté. Vérifiez également que la pull request respecte les directives de contribution du projet, notamment en ce qui concerne la structure attendue du contenu, l'utilisation correcte du Markdown et la catégorisation adéquate. Si besoin, vous pouvez discuter avec la personne ayant contribué et lui demander d'effectuer des corrections. (1)
{ .annotate }

1.  En cas de difficulté face à la complexité de l'interface, n'hésitez pas à consulter la [documentation GitHub :octicons-link-external-16:](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request) pour obtenir des explications détaillées.

!!! warning "Nouveaux fichiers"
    En cas de nouveau fichier ajouté au dépôt, vérifiez qu'il est **placé dans le bon dossier** au sein de l'arborescence du projet, conformément aux conventions établies (`docs/biblio/` pour les ressources et `docs/assets/images/` pour les images). Pour toute nouvelle page ressource, vérifiez qu'elle contient les tags de **catégories** appropriées en haut du fichier, comme indiqué dans la [structure attendue](#structure-de-page-attendue).

:material-numeric-2-circle: **Merge de la pull request** : Une fois que la pull request a été soigneusement examinée et que tous les ajustements nécessaires ont été apportés, elle peut alors être **fusionnée** dans la branche principale ("main") du dépôt. Cela mettra à jour le projet avec les contributions acceptées. (1)
{ .annotate }

1.  :octicons-arrow-right-24: Onglet "Conversation" de la pull request ciblée :octicons-arrow-right-24: cliquez sur "**Squash and merge**".<br>
N'hésitez pas à consulter la [documentation GitHub :octicons-link-external-16:](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request) pour obtenir des explications exhaustives sur cette procédure !


 Pour finir, il est toujours bon de s'assurer que la fusion est effectuée correctement et que le site est mis à jour pour refléter les nouveaux changements (après environ 30 secondes). En suivant ces lignes directrices, les administrateurs et responsables peuvent efficacement gérer les contributions au projet MDR, garantissant que le contenu reste de haute qualité, organisé, et utile pour la communauté.

??? question "Comment annuler la fusion avec une pull request ?"
    Pas de panique ! Le système Git est précisément conçu pour conserver un historique des modifications du dépôt. Dans le cas d'une pull request, un bouton "**Revert**" permet de créer une nouvelle pull request qui annulera les changements apportés par la pull request ciblée. Consultez la [documentation GitHub :octicons-link-external-16:](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/reverting-a-pull-request) qui vous guidera à travers cette procédure en quelques étapes simples.

    !!! warning "Annuler des modifications effectuées SANS pull requests / Revenir à une version antérieure du dépôt"
        En cas de changements directs sans pull requests (par exemple en choisissant l'option "_Commit directly to the main branch_" avant de valider un commit, ou lorsqu'on utilise la commande de terminal `push origin main`), il est toujours possible de revenir en arrière grâce à l'historique Git, mais cela nécessite d'utiliser des **commandes de terminal assez "risquées"** qui n'existent **pas** dans l'interface web de GitHub. En effet, **de telles manipulations peuvent aisément faire disparaître des mois de travail**, allant jusqu'à supprimer l'historique Git et même vos fichiers locaux synchronisés avec le dépôt !<br>
        Dans un tel cas, il est donc **fortement** recommandé de faire appel à une personne à l'aise avec Git afin de rétablir l'état souhaité du dépôt.

### Organiser les tâches à accomplir sur GitHub (Projects)

La gestion efficace des tâches et des idées est essentielle pour maintenir un projet structuré et favoriser une collaboration fluide.

Les [projects :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR/projects) offrent une vue d’ensemble des tâches sous différentes formes (tableaux, Kanbans, roadmaps, etc) permettant de visualiser le statut de chaque tâche. Ils sont parfaits pour organiser les contributions.

* Créer un project : Allez dans l'onglet "Projects" et cliquez sur "New Project".

* Colonnes typiques : Ajoutez des colonnes comme "À faire", "En cours", "Terminé".

* Cartes liées aux pull requests : Ajoutez les pull requests en tant que cartes dans les colonnes appropriées.

* Suivi de progression : Déplacez les cartes entre les colonnes pour refléter l’avancement des tâches.
Avec ces outils, l'équipe du projet MDR peut facilement prioriser les tâches, suivre les contributions et maintenir un workflow clair et efficace pour tous les membres.






## Édition "avancée"

### Fonctionnalités de Material for MkDocs

Comme l'illustre cette page, il est possible d'ajouter divers éléments (encarts, annotations, tableaux, diagrammes, icônes, etc...) grâce à Material for MkDocs, le framework utilisé pour générer ce site. Consultez les pages de la [section "Reference" de Material for MkDocs :octicons-link-external-16:](https://squidfunk.github.io/mkdocs-material/reference/) pour en savoir plus et explorer les fonctionnalités à disposition.

### Travailler en local / Prévisualiser le site

Lorsqu'on consulte une page directement depuis le dépôt GitHub, en mode de visualisation "Preview", seuls les éléments en Markdown et/ou HTML sont rendus correctement. En revanche, les éléments liés aux fonctionnalités spécifiques de Material for MkDocs restent à l'état de texte car GitHub ne peut pas interprêter de frameworks. Pour éditer et prévisualiser des pages sous leur forme "finale", telles qu'elles apparaissent sur le site MDR, vous pouvez facilement créer votre propre version locale sur laquelle travailler avec l'éditeur de code de votre choix.

Prérequis : Avoir installé [Python :octicons-link-external-16:](https://www.python.org/downloads/).

:material-numeric-1-circle: Télécharger une [copie du dépôt MDR au format .zip](https://github.com/thomas-qwertz/MDR/archive/refs/heads/main.zip) et extraire les fichiers.

:material-numeric-2-circle: Exécuter quelques commandes de terminal dans **la racine du dossier du projet local** (là où se trouve le dossier `/docs`) :

<div class="grid" style="text-align:left" markdown>
**a.** Installer Material for MkDocs en créant un environnement virtuel (à faire une seule fois) :<br>
`python -m venv venv`<br>
`pip install mkdocs-material`

**b.** Activer l'environnement virtuel et générer le site (à faire à chaque session de travail) :<br>
`.\venv\Scripts\activate`<br>
`mkdocs serve`
</div>

Le terminal affichera alors l'URL à partir duquel vous pouvez prévisualiser le site.

### Pull, commit, push etc SANS GitHub

Prérequis : Avoir installé [Git :octicons-link-external-16:](https://git-scm.com/book/fr/v2/D%C3%A9marrage-rapide-Installation-de-Git).

:material-numeric-1-circle: **Cloner le dépôt**<br>
Pour obtenir une copie locale du projet MDR, utilisez la commande git clone :<br>
`git clone https://github.com/thomas-qwertz/MDR.git`<br>
Cela crée un dossier nommé MDR contenant tous les fichiers du projet.

:material-numeric-2-circle: **Travailler sur une branche**<br>
Avant d'apporter des modifications, créez une nouvelle branche pour isoler votre travail :<br>
`git checkout -b nom-de-votre-branche`

:material-numeric-3-circle: **Effectuer des modifications**<br>
Modifiez les fichiers localement en utilisant l'éditeur de texte ou de code de votre choix.

:material-numeric-4-circle: **Stager les changements**<br>
Ajoutez les fichiers modifiés à l’index (staging area) avec la commande git add :<br>
`git add chemin/vers/fichier`<br>
Pour ajouter tous les fichiers modifiés :<br>
`git add .`

:material-numeric-5-circle: **Créer un commit**<br>
Enregistrez vos changements avec un message descriptif :<br>
`git commit -m "Description de vos modifications"`

:material-numeric-6-circle: **Pousser les changements vers GitHub**<br>
Envoyez vos modifications vers le dépôt distant (GitHub) sur votre branche :<br>
`git push origin nom-de-votre-branche`

:material-numeric-7-circle: **Créer une Pull Request**<br>
Allez sur le dépôt GitHub via votre navigateur.
Une notification apparaîtra pour créer une Pull Request à partir de votre branche récemment poussée.
Cliquez sur "Compare & Pull Request", ajoutez une description et soumettez la Pull Request.

**Autres commandes utiles**

* Mettre à jour votre copie locale (pull)<br>
Pour synchroniser votre copie locale avec les dernières modifications du dépôt distant :<br>
`git pull origin main`

* Voir le statut des fichiers<br>
Pour voir quels fichiers ont été modifiés ou ajoutés :<br>
`git status`

* Voir l'historique des commits<br>
Pour afficher les derniers commits du projet :<br>
`git log --oneline`

* Revenir à une version précédente<br>
Pour annuler des modifications non encore commit :<br>
`git checkout chemin/vers/fichier`
