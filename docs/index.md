---
hide:
  - navigation
  - toc
---

<script src="https://esm.sh/css-doodle/css-doodle.min.js?raw"></script>
<style>
  @media screen and (max-width: 76.234375em) {
    css-doodle, #art-txt-svg {
    top: 48px !important;
   }
   .welcome-cards {  
    top: -22px !important;
   }
   .grid.cards {
    grid-template-columns: repeat(auto-fit,minmax(min(100%,1rem),351.8px)) !important;
   }
  }
  .md-main {
    background-repeat: no-repeat !important;
    background-size: 100% 100% !important;
    background-position: 50% 41.22vw !important;
  }
  .md-content__button {
    display: none;
  }
  .md-tabs {
    box-shadow: none !important;
  }
  .doodle-container {
    width: 100%;
    height: 29.6vw !important; /*28.29vw*/
    left: 0 !important; 
  }
  css-doodle {
    position: absolute;
    width: 100%;
    height: 41.39vw; /*44.58%*/ /*41.22vw*/
    left: 0;
    top: 4rem;
    margin-top: 0;
  }
  #art-txt-svg {
  position: absolute;
  width: 100%;
  /*height: 41.35vw; 41.22vw*/
  left: 0;
  top: 4rem;
  z-index: 0;
  overflow: hidden;
  mix-blend-mode: saturation;
  }
  .welcome-card {  
    position: relative;
    text-align: center;
    z-index: 1;
  }
  .welcome-card h2 {
    margin-top: 0;
    text-decoration: none;
    font-weight: bold;
    user-select: none;
    font-size: 1.52em !important;
    letter-spacing: 0 !important;
    font-variant: small-caps;
  }
  .welcome-card .md-button {
    margin-top: 0.35rem !important;
  }
  .grid.cards {
    justify-content: center !important;
    text-align: center !important;
    grid-template-columns: repeat(auto-fit,minmax(min(100%,16rem),373.8px));
  }
</style>

<div class="doodle-container">
  <css-doodle click-to-update>
    @grid: 36x15;
    opacity: calc(1.1 - 0.0712 * @y);
    background: var(--md-primary-fg-color);
    margin: 0px; /*-0.19px*/
    transition: @r(0.5s, 1.5s) ease-out;
    clip-path: polygon(@pick(
    '0 0, 100% 0, 100% 100%',
    '0 0, 100% 0, 0 100%',
    '0 0, 100% 100%, 0 100%',
    '100% 0, 100% 100%, 0 100%'
    ));
  </css-doodle>

<svg id="art-txt-svg" width="100%" height="100%" viewBox="0 0 360 150" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M40 10V110H60V50L80 70L100 50V110H120V10L80 50L40 10Z" fill="var(--md-default-bg-color)"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M140 110V10H200L220 30V90L200 110H140ZM160 30V90H190L200 80V40L190 30H160Z" fill="var(--md-default-bg-color)"/>
<path fill-rule="evenodd" clip-rule="evenodd" d="M240 10V110H260V70H280L300 110H320L300 70L320 50V30L300 10H240ZM260 30V50H290L300 40L290 30H260Z" fill="var(--md-default-bg-color)"/>
</svg>

</div>

<div class="welcome-card" markdown>
<h2>MDR, la plateforme dédiée à la Mutualisation&nbsp;Des&nbsp;Ressources<br>pour la Recherche Orientée par la Conception</h2>
[:octicons-arrow-right-24: Parcourir](biblio/index.md){ .md-button .md-button--primary }
</div>

<div class="grid cards" style="padding-top:0.4rem" markdown>
-   <span class="twemoji middle" style="font-size:2em">:material-test-tube:</span>__Une démarche scientifique__

    Des ressources sélectionnées par des<br>
    chercheurs en Sciences de l'Éducation,<br>
    dans un cadre théorique formel.

    [:octicons-arrow-right-24: En savoir plus](help/apropos.md){ .md-button }

-   :material-charity:{ .xl .middle }&nbsp; __Un projet collaboratif__

    Mutualiser, c'est partager et échanger.<br>
    Apportez votre expérience et interagissez avec la communauté !
    
    [:octicons-arrow-right-24: En savoir plus](help/index.md){ .md-button }

</div>

# <!-- "# " à conserver pour éviter le titre "Accueil" par défaut -->

<script>
  ///// script pour l'animation d'accueil /////
  function update () {
    document.querySelectorAll('css-doodle').forEach(function (o) {
      o.update();
    });
  }
  window.addEventListener('load', function() {
    //update();
    setTimeout(update, 5000);
  });
  var interval = setInterval(update, 15000)
  document.addEventListener('click', function() {
  // clearInterval(interval)
  update()
  // interval = setInterval(update, 30000)
  })

  // Redirection home pour header
  document.addEventListener('DOMContentLoaded', function() {
    var element = document.querySelector('body > header > nav > div.md-header__title > div > div:nth-child(1) > span');
    if (element) {
      element.style.cursor = 'pointer';
      element.addEventListener('click', function() {
        window.location.href = "https://thomas-qwertz.github.io/MDR/";
      });
    }
});

</script>