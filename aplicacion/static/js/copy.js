
// Espera a que el documento HTML esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtén una referencia al botón de copiar
    var copyButton = document.getElementById('copyButton');
    
    // Agrega un evento de clic al botón de copiar
    copyButton.addEventListener('click', function() {
      // Obtén una referencia al campo de texto
      var codigoInvitacion = document.getElementById('codigoInvitacion');
      
      // Copia el contenido al portapapeles utilizando la API Clipboard
      navigator.clipboard.writeText(codigoInvitacion.value)
        .then(function() {
          console.log('El texto se ha copiado correctamente al portapapeles');
        })
        .catch(function(error) {
          console.error('Error al copiar el texto al portapapeles:', error);
        });
    });
  });