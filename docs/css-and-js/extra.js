///// SCRIPT POUR RANDOM BACKGROUNDS /////

// Initialisation du numéro d'image pour garantir la cohérence entre les thèmes
let currentImageNumber = Math.floor(Math.random() * 27) + 1;
//let currentImageNumber = 12;

function updateBackgroundImage() {
  const basePath = '../assets/backgrounds/'; // Assurez-vous que ce chemin est correct pour votre projet
  const isDarkMode = document.body.getAttribute('data-md-color-scheme') === 'slate';
  const modePrefix = isDarkMode ? 'dark-' : 'light-';
  const imageUrl = `${basePath}${modePrefix}bg${currentImageNumber}.svg`;
  
  document.documentElement.style.setProperty('--background-image', `url('${imageUrl}')`);

  console.log(`Background image set to: ${imageUrl}`);
}

// Application initiale de l'image de fond
updateBackgroundImage();

// Configuration de l'observateur pour détecter les changements de thème
const observer = new MutationObserver(mutations => {
  mutations.forEach(mutation => {
    if (mutation.attributeName === 'data-md-color-scheme') {
      updateBackgroundImage();
    }
  });
});

// Démarrage de l'observation
observer.observe(document.body, { attributes: true });


//////////////// SCRIPT POUR RETOUR HOMEPAGE /////////////////

document.addEventListener('DOMContentLoaded', function() {
    var element = document.querySelector('body > header > nav > div.md-header__title > div > div:nth-child(1) > span');
    
    // Vérifier si l'élément existe pour éviter les erreurs
    if (element) {
      element.style.cursor = 'pointer';
      // Ajouter un gestionnaire d'événement de clic à l'élément
      element.addEventListener('click', function() {
        // Rediriger l'utilisateur vers l'URL souhaitée
        window.location.href = "https://thomas-qwertz.github.io/MDR/";
        //if (window.location.href !== "https://thomas-qwertz.github.io/MDR/") {
        //  window.location.href = "../..";
        //}
      });
    }
  });