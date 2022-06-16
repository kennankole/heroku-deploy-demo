// Highlights current page link in the navbar 

document.addEventListener('DOMContentLoaded', () => {
   const $navLinks = Array.prototype.slice.call(
       document.querySelectorAll('.nav-link'), 0
   ); 
   if ($navLinks.length > 0){
       $navLinks.forEach(el => {
           if(window.location.pathname == el.getAttribute("href")){
               el.className += " current";
           }
       })
   }
});