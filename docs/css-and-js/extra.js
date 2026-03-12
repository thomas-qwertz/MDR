///////////////////////
// CONFIGURATION GÉNÉRALE
///////////////////////

/*
Clé utilisée pour stocker le numéro du background dans sessionStorage.
Cela permet de conserver la même image pendant toute la session
(navigation entre pages), au lieu de générer un nouveau fond à chaque page.
*/
const MDR_BACKGROUND_KEY = "mdr-bg-index";

/*
Nombre total d'images de fond disponibles.
Les fichiers sont supposés suivre la structure :

light-bg1.svg
light-bg2.svg
...
dark-bg1.svg
dark-bg2.svg
...
*/
const MDR_BACKGROUND_COUNT = 27;



///////////////////////
// GESTION DES BACKGROUNDS ALÉATOIRES
///////////////////////

/*
Cette fonction détermine le chemin vers le dossier contenant
les images de fond.

Pourquoi faire cela dynamiquement ?
Parce que le script peut être inclus depuis différents chemins
selon l'organisation du site. On calcule donc le chemin relatif
à partir de l'emplacement réel du script.
*/
function getExtraScriptBasePath() {

  // document.currentScript correspond au script actuellement exécuté
  const currentScript = document.currentScript;

  if (currentScript && currentScript.src) {
    // On construit le chemin vers ../assets/backgrounds/
    // relativement à l'emplacement du script.
    return new URL("../assets/backgrounds/", currentScript.src).toString();
  }

  /*
  Fallback : si document.currentScript n'est pas disponible
  (cas rare selon la manière dont le script est chargé),
  on cherche manuellement un script contenant "css-and-js/extra.js".
  */
  const fallbackScript = Array.from(document.scripts).find((script) =>
    script.src && script.src.includes("css-and-js/extra.js"),
  );

  return fallbackScript
    ? new URL("../assets/backgrounds/", fallbackScript.src).toString()
    : "../assets/backgrounds/";
}



/*
Détermine quel numéro d'image utiliser.

Logique :
1. Si un numéro existe déjà dans sessionStorage → on le réutilise.
2. Sinon → on génère un numéro aléatoire.
3. On sauvegarde ce numéro pour toute la session.
*/
function getBackgroundNumber() {

  try {

    const stored = Number.parseInt(
      sessionStorage.getItem(MDR_BACKGROUND_KEY) || "",
      10
    );

    // Vérifie que la valeur stockée est valide
    if (Number.isInteger(stored) && stored >= 1 && stored <= MDR_BACKGROUND_COUNT) {
      return stored;
    }

    // Génération d'un numéro aléatoire
    const generated = Math.floor(Math.random() * MDR_BACKGROUND_COUNT) + 1;

    // Stockage pour les pages suivantes
    sessionStorage.setItem(MDR_BACKGROUND_KEY, String(generated));

    return generated;

  } catch {

    /*
    Certains navigateurs peuvent bloquer sessionStorage
    (ex: navigation privée restrictive).
    Dans ce cas on génère simplement un nombre aléatoire.
    */
    return Math.floor(Math.random() * MDR_BACKGROUND_COUNT) + 1;

  }
}



/*
Met à jour l'image de fond du site.

Le script :
1. détecte le thème (clair ou sombre)
2. choisit l'image correspondante
3. applique l'image via une variable CSS globale
*/
function updateBackgroundImage() {

  // Si le body n'existe pas encore (chargement précoce), on abandonne
  if (!document.body) {
    return;
  }

  const basePath = getExtraScriptBasePath();
  const imageNumber = getBackgroundNumber();

  /*
  Material for MkDocs stocke le thème actuel
  dans l'attribut HTML : data-md-color-scheme
  */
  const isDarkMode =
    document.body.getAttribute("data-md-color-scheme") === "slate";

  const modePrefix = isDarkMode ? "dark-" : "light-";

  const imageUrl = `${basePath}${modePrefix}bg${imageNumber}.svg`;

  // Injection de l'image dans une variable CSS globale
  document.documentElement.style.setProperty(
    "--background-image",
    `url('${imageUrl}')`
  );

}



/*
Initialise un observateur qui surveille les changements de thème.

Quand l'utilisateur passe :
clair → sombre
ou
sombre → clair

l'image de fond correspondante est automatiquement remplacée.
*/
function initBackgroundObserver() {

  // Application initiale de l'image
  updateBackgroundImage();

  if (!document.body) {
    return;
  }

  /*
  MutationObserver est une API permettant d'observer
  les modifications du DOM (attributs, enfants, etc.).
  */
  const observer = new MutationObserver((mutations) => {

    for (const mutation of mutations) {

      if (mutation.attributeName === "data-md-color-scheme") {
        updateBackgroundImage();
      }

    }

  });

  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-md-color-scheme"],
  });

}



///////////////////////
// RETOUR HOMEPAGE EN CLIQUANT SUR LE TITRE
///////////////////////

/*
Cette fonction rend tout le bloc du titre du header
cliquable pour retourner à la page d'accueil.

Objectif :
améliorer l'ergonomie : cliquer sur le titre
agit comme cliquer sur le logo.
*/
function initHeaderHomeLink() {

  const title = document.querySelector(".md-header__title");
  const logoLink = document.querySelector(".md-header__button.md-logo");

  // Vérification de sécurité
  if (!(title instanceof HTMLElement) || !(logoLink instanceof HTMLAnchorElement)) {
    return;
  }

  /*
  Empêche d'attacher plusieurs fois les événements
  si le script est exécuté plusieurs fois.
  */
  if (title.dataset.mdrHomeBound === "true") {
    return;
  }

  const navigateHome = () => window.location.assign(logoLink.href);

  // Marqueur interne
  title.dataset.mdrHomeBound = "true";

  // Classe CSS utile pour styliser l'élément si besoin
  title.classList.add("mdr-home-link");

  // Accessibilité clavier
  title.tabIndex = 0;
  title.setAttribute("role", "link");
  title.setAttribute("aria-label", "Retour à l’accueil");



  /*
  Gestion du clic souris
  */
  title.addEventListener("click", (event) => {

    /*
    Si l'utilisateur clique sur un lien ou un bouton
    déjà présent dans le header, on laisse le comportement normal.
    */
    if (event.target instanceof Element &&
        event.target.closest("a, button, input, label")) {
      return;
    }

    navigateHome();

  });



  /*
  Gestion clavier (accessibilité)
  Permet d'utiliser :
  - Entrée
  - Espace
  */
  title.addEventListener("keydown", (event) => {

    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      navigateHome();
    }

  });

}



///////////////////////
// RAFRAÎCHISSEMENT DES CSS-DOODLE
///////////////////////

/*
Certains éléments <css-doodle> nécessitent un rafraîchissement
pour générer de nouveaux motifs.

Ce script force périodiquement leur mise à jour.
*/
function initHomeDoodle() {

  const doodles = Array.from(document.querySelectorAll("css-doodle"));

  if (!doodles.length) {
    return;
  }

  const update = () => {

    doodles.forEach((doodle) => {

      if (typeof doodle.update === "function") {
        doodle.update();
      }

    });

  };

  /*
  Mise à jour après chargement complet de la page
  */
  window.addEventListener(
    "load",
    () => {
      window.setTimeout(update, 5000);
    },
    { once: true },
  );

  // Mise à jour périodique
  window.setInterval(update, 15000);

  // Mise à jour lors d'un clic utilisateur
  document.addEventListener("click", update);

}



///////////////////////
// NORMALISATION DU TEXTE DE RECHERCHE
///////////////////////

/*
Cette fonction simplifie le texte afin de rendre
la recherche plus tolérante.

Exemples :
"énergie" → "energie"
"Énergie" → "energie"
*/
function normalizeSearchText(value) {

  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();

}



///////////////////////
// FILTRAGE DE LA BIBLIOTHÈQUE
///////////////////////

/*
Implémente un système combiné :

- recherche texte
- filtres par tags
*/
function initLibraryFilters() {

  const root = document.querySelector(".mdr-library-index");

  if (!(root instanceof HTMLElement)) {
    return;
  }

  const searchInput = root.querySelector(".mdr-library-search__input");
  const status = root.querySelector(".mdr-library-status");
  const emptyState = root.querySelector(".mdr-library-empty");

  const groups = Array.from(root.querySelectorAll(".mdr-library-group"));
  const items = Array.from(root.querySelectorAll(".mdr-library-item"));
  const filterButtons = Array.from(root.querySelectorAll(".mdr-chip[data-filter]"));

  let activeFilter = "*";



  /*
  Petite fonction pour afficher :
  "1 ressource affichée"
  "5 ressources affichées"
  */
  const pluralize = (count) =>
    `${count} ressource${count > 1 ? "s" : ""} affichée${count > 1 ? "s" : ""}`;



  /*
  Recalcule quels éléments doivent être visibles.
  */
  const refresh = () => {

    const query =
      searchInput instanceof HTMLInputElement
        ? normalizeSearchText(searchInput.value)
        : "";

    let visibleItems = 0;

    items.forEach((item) => {

      if (!(item instanceof HTMLElement)) {
        return;
      }

      const haystack = item.dataset.search || "";
      const tags = (item.dataset.tags || "").split("|").filter(Boolean);

      const matchesFilter =
        activeFilter === "*" || tags.includes(activeFilter);

      const matchesQuery =
        !query || haystack.includes(query);

      const isVisible = matchesFilter && matchesQuery;

      item.hidden = !isVisible;

      if (isVisible) {
        visibleItems += 1;
      }

    });



    /*
    Cache les groupes vides
    */
    groups.forEach((group) => {

      if (!(group instanceof HTMLElement)) {
        return;
      }

      const hasVisibleChild =
        group.querySelector(".mdr-library-item:not([hidden])");

      group.hidden = !hasVisibleChild;

    });



    /*
    Mise à jour du compteur
    */
    if (status instanceof HTMLElement) {
      status.textContent = pluralize(visibleItems);
    }



    /*
    Message "aucun résultat"
    */
    if (emptyState instanceof HTMLElement) {
      emptyState.hidden = visibleItems !== 0;
    }

  };



  /*
  Gestion des boutons de filtre
  */
  filterButtons.forEach((button) => {

    if (!(button instanceof HTMLButtonElement)) {
      return;
    }

    button.addEventListener("click", () => {

      activeFilter = button.dataset.filter || "*";

      filterButtons.forEach((candidate) => {

        if (candidate instanceof HTMLElement) {
          candidate.classList.toggle(
            "is-active",
            candidate === button
          );
        }

      });

      refresh();

    });

  });



  if (searchInput instanceof HTMLInputElement) {
    searchInput.addEventListener("input", refresh);
  }

  refresh();

}



// INITIALISATION GLOBALE
/*
Quand le DOM est prêt, on initialise toutes
les fonctionnalités du script.
*/
document.addEventListener("DOMContentLoaded", () => {

  initBackgroundObserver();
  initHeaderHomeLink();
  initHomeDoodle();
  initLibraryFilters();

});
