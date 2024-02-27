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

Ce site est hébergé sur GitHub et généré automatiquement d'après les fichiers qui se trouvent dans le [dépôt du projet MDR :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR). 



Vous pouvez contribuer et apporter des modifications aux pages. Voici comment faire :

1. Allez sur notre dépôt GitHub à l'adresse [lien du dépôt].
2. Naviguez vers le fichier que vous souhaitez modifier. Les fichiers sont généralement dans le dossier `/docs`.
3. Cliquez sur l'icône du crayon pour commencer à modifier le fichier.
4. Après avoir apporté vos modifications, descendez vers le bas de la page et cliquez sur "Propose Changes". Donnez un titre et une description à vos modifications.
5. Vous serez redirigé vers une nouvelle page. Cliquez sur "Create Pull Request" et donnez un titre et une description à votre Pull Request.
6. Attendez que vos modifications soient approuvées par un administrateur.

Note : Vous aurez besoin d'un compte GitHub pour effectuer ces actions. Si vous n'en avez pas, vous pouvez en créer un gratuitement sur GitHub.

### Fonctionnement général de GitHub

### Syntaxe de base en Markdown (et/ou HTML)





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
3.  Ajouter l'icône "**:octicons-link-external-16:**" (`:octicons-link-external-16:`) dans le texte d'un lien permet d'indiqueraux utilisateurs qu'il s'agit d'un **lien externe**.

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
6.  `index.md` : La page `index.md` du dossier `biblio/` est la page qui regroupe la liste des ressources classées par ordre alphabétique (à updater lorsqu'une nouvelle ressource est ajoutée). Les autres pages sont **les ressources** elles-mêmes.
7.  `css-and-js/` : Dossier pour les fichiers CSS et JavaScript personnalisés du site.
8.  `help/` : Dossier qui contient les pages d'information et d'assistance, telles que ce guide.
9.  `apropos.md` : La page "À propos" du site 🙂
10.  `guide.md` : La présente page 🙂
11.  `index.md` : La page `index.md` du dossier `help/` correspond à la page "Contribuer/Discuter" du site.
12.  `categories.md` : Page listant les différentes catégories de ressources (updatée automatiquement si des "tags" sont présentes dans la page d'une ressource).
13.  `index.md` : La page d'accueil du site (appartient au dossier `docs/`, à ne pas confondre avec les pages `index` d'autres dossiers).
14.  `mkdocs.yml` : Fichier de configuration pour MkDocs, définissant la structure et les paramètres du site.
15.  `README.md` : Fichier contenant des informations générales sur le projet, visible sur la page principale du dépôt GitHub.

!!! failure "Modifications hors pages ressources"

    Pour assurer le bon fonctionnement du site, merci de ne pas modifier les fichiers hors du dossier `docs/biblio/`.<br>
    Si vous souhaitez proposer des changements non spécifiques aux ressources, ouvrez d'abord une [discussion :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR/discussions) pour en parler !

## Édition "avancée"

### Fonctionnalités de Material for MkDocs

Comme l'illustre cette page, il est possible d'ajouter divers éléments (encarts, annotations, tableaux, diagrammes, icônes, etc...) grâce à Material for MkDocs, le framework utilisé pour générer ce site. Consultez les pages de la [section "Reference" de Material for MkDocs :octicons-link-external-16:](https://squidfunk.github.io/mkdocs-material/reference/) pour en savoir plus et explorer les fonctionnalités à disposition.

### Pull, commit, push etc SANS GitHub

## Et après ? Tâches des administrateurs/responsables

La gestion et la révision des contributions reçues sur GitHub constituent une responsabilité clé des administrateurs et des responsables du projet MDR. Voici une vue d'ensemble des étapes et des meilleures pratiques pour examiner et intégrer efficacement les propositions de modifications soumises par la communauté.

### Validation des contributions

:material-numeric-0-circle: **Réception d'une Pull Request** : Lorsqu'une nouvelle contribution est soumise, elle apparaît dans la section [Pull Requests :octicons-link-external-16:](https://github.com/thomas-qwertz/MDR/pulls) du dépôt GitHub du projet. Les administrateurs sont notifiés et peuvent commencer le processus d'examen.

:material-numeric-1-circle: **Vérification du contenu** : Assurez-vous que le contenu proposé est pertinent, exact, et apporte une valeur ajoutée au projet. Cela peut nécessiter une lecture approfondie du contenu, une vérification des faits, ou une consultation avec d'autres membres de la communauté. Vérifiez également que la pull request respecte les directives de contribution du projet, notamment en ce qui concerne la structure attendue du contenu, l'utilisation correcte du Markdown et la catégorisation adéquate. Si besoin, vous pouvez discuter avec la personne ayant contribué et lui demander d'effectuer des corrections. (1)
{ .annotate }

1.  En cas de difficulté face à la complexité de l'interface, n'hésitez pas à consulter la [documentation GitHub :octicons-link-external-16:](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/reviewing-proposed-changes-in-a-pull-request) pour obtenir des explications détaillées.

:material-numeric-2-circle: **Nouveau fichier ?** Vérifiez qu'il est **placé dans le bon dossier** au sein de l'arborescence du projet, conformément aux conventions établies (`docs/biblio/` pour les ressources et `docs/assets/images/` pour les images). Pour toute nouvelle page ressource, vérifiez qu'elle contient les tags de **catégories** appropriées en haut du fichier, comme indiqué dans la [structure attendue](#structure-de-page-attendue).

:material-numeric-3-circle: **Merge de la Pull Request** : Une fois que la pull request a été soigneusement examinée et que tous les ajustements nécessaires ont été apportés, elle peut alors être **fusionnée** dans la branche principale ("main") du dépôt. Cela mettra à jour le projet avec les contributions acceptées. (1)
{ .annotate }

1.  :octicons-arrow-right-24: Onglet "Conversation" de la pull request ciblée :octicons-arrow-right-24: cliquez sur "**Squash and merge**".<br>
N'hésitez pas à consulter la [documentation GitHub :octicons-link-external-16:](https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request) pour obtenir des explications exhaustives sur cette procédure !

:material-numeric-4-circle: **Mise à jour des fichiers `biblio/index.md` et `mkdocs.yml`** : Pour les nouvelles pages de ressources, il est nécessaire d'ajouter manuellement leurs liens dans le fichier `biblio/index.md` (qui correspond à la [liste des ressources par ordre alphabétique](../biblio/index.md)) et dans le fichier de configuration `mkdocs.yml` (pour que les liens apparaissent dans le menu de navigation du site MDR). En revanche, les nouvelles pages incluant des "tags" de catégories seront automatiquement listées dans la page [Catégories](../categories.md).


 Pour finir, il est toujours bon de s'assurer que la fusion est effectuée correctement et que le site est mis à jour pour refléter les nouveaux changements (après environ 30 secondes). En suivant ces lignes directrices, les administrateurs et responsables peuvent efficacement gérer les contributions au projet MDR, garantissant que le contenu reste de haute qualité, organisé, et utile pour la communauté.

### Organiser les tâches à accomplir sur GitHub (issues et projects)








