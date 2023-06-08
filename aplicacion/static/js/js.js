const sidebar = document.querySelector(".sidebar");
const sidebarClose = document.querySelector("#sidebar-close");
const menu = document.querySelector(".menu-content");
const menuItems = document.querySelectorAll(".submenu-item");
const subMenuTitles = document.querySelectorAll(".submenu .menu-title");

sidebarClose.addEventListener("click", () => sidebar.classList.toggle("close"));

menuItems.forEach((item, index) => {
  item.addEventListener("click", () => {
    menu.classList.add("submenu-active");
    item.classList.add("show-submenu");
    menuItems.forEach((item2, index2) => {
      if (index !== index2) {
        item2.classList.remove("show-submenu");
      }
    });
  });
});

subMenuTitles.forEach((title) => {
  title.addEventListener("click", () => {
    menu.classList.remove("submenu-active");
  });
});




// Espera a que el documento HTML esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
  // Obtén una referencia al botón de copiar
  var copyButton = document.getElementById('copyButton');
  
  // Agrega un evento de clic al botón de copiar
  copyButton.addEventListener('click', function() {
    // Obtén una referencia al campo de texto
    var codigoInvitacion = document.getElementById('codigoInvitacion');
    
    // Selecciona el texto en el campo de texto
    codigoInvitacion.select();
    
    // Copia el texto seleccionado al portapapeles utilizando la API Clipboard
    navigator.clipboard.writeText(codigoInvitacion.value)
      .then(function() {
        console.log('El texto se ha copiado correctamente al portapapeles');
      })
      .catch(function(error) {
        console.error('Error al copiar el texto al portapapeles:', error);
      });
    
    // Deselecciona el texto en el campo de texto
    codigoInvitacion.blur();
  });
});

