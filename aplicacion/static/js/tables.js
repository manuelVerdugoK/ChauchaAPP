$(document).ready(function() {
    // Configuración de Numeral.js
    numeral.register('locale', 'es', {
        delimiters: {
            thousands: '.',
            decimal: ','
        },
        abbreviations: {
            thousand: 'k',
            million: 'M',
            billion: 'B',
            trillion: 'T'
        },
        currency: {
            symbol: '$'
        }
    });
    numeral.locale('es');

    // Inicialización de la tabla DataTable de Ingresos
    $('#tabla-ingresos').DataTable({
        language: {
            // ... configuración del idioma ...
        },
        columnDefs: [
            {
                targets: 2, // Índice de la columna "Monto de Ingreso"
                render: function(data, type, row) {
                    return numeral(data).format('$0,0');
                }
            }
        ]
    });

    // Inicialización de la tabla DataTable de Egresos
    $('#tabla-egresos').DataTable({
        language: {
            // ... configuración del idioma ...
        },
        columnDefs: [
            {
                targets: 2, // Índice de la columna "Monto de Egreso"
                render: function(data, type, row) {
                    return numeral(data).format('$0,0');
                }
            }
        ]
    });
});

