/**
 * Cambia la cantidad de un producto en el carrito
 * @param {int} id: PK del registro del produto en el carrito 
 */
function cambiarCantidad(id) {
    // Obtiene la cantidad actual del producto y su valor unitario
    let cantidad = document.getElementById('cantidad_'+id).value;
    let valorUnit = document.getElementById('cantidad_'+id).dataset.preciou;
    // URL del endpoint para cambiar la cantidad de un producto en el carrito
    let url = "http://localhost:8000/productos/cambiarCantidad/";
    // Datos a enviar al endpoint
    let datos = {
        'id': id,
        'cantidad': cantidad
    };
    // Calcula el nuevo total del producto y lo muestra en la tabla
    let total = parseFloat(cantidad) * parseFloat(valorUnit);
    document.getElementById('total_'+id).innerText = '$' + total;

    // Hace la petición AJAX al endpoint y espera la respuesta
    mensajeAjax(url, datos, cambiarCantidadResp)    
}
// Función que se ejecuta cuando se recibe la respuesta del endpoint cambiarCantidad
function cambiarCantidadResp(data) {
    // Actualiza los totales del carrito con los datos recibidos en la respuesta
    document.getElementById('subtotal').innerText = '$' + data['subtotal'];
    document.getElementById('iva').innerText = '$' + data['iva'];
    document.getElementById('envio').innerText = '$' + data['envio'];
    document.getElementById('total').innerText = '$' + data['total']; 
}

/**
 * Consulta AJAX al servidor por método POST
 * @param {*} urlserver :Direccion de envio
 * @param {*} datos     :Data en formato JavaScript object
 * @param {*} callBackFunction : Funcion de retorno
 */
const csrftoken = getCookie('csrftoken');
fetch(urlserver, {
    method: 'POST',
    credentials: 'same-origin',
    headers: { 
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify(datos) //JavaScript object of data to POST
})

/**
 * @param {*} name Nombre de la cookie
 * @returns el cvontenido de la cookie
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") { //Verifica si existe alguna cookie y no está vacía
        const cookies = document.cookie.split(";"); // Divide las cookies en un array
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim(); // Quita los espacios en blanco de cada cookie
            // ¿Empieza la cadena de la cookie con el nombre que queremos?
            if (cookie.substring(0, name.length + 1) === (name + "=")) { //Si la cookie empieza con el nombre de la cookie deseada
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1)); // Obtiene el valor de la cookie y decodifica los caracteres especiales
                break;
            }
        }
    }
    return cookieValue; // Devuelve el valor de la cookie, o null si no se encontró la cookie
} 
