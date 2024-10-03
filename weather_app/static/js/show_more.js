/**
 * Muestra u oculta el contenido de un elemento HTML.
 * 
 * @param {string} elementId - El id del elemento HTML.
 */
function toggleDisplay(elementId) {
    const content = document.getElementById(elementId);
    content.style.display = content.style.display === 'none' ? 'block' : 'none';
}

document.getElementById('see_more_button').addEventListener('click', function() {
    toggleDisplay('see_more');
});

document.getElementById('see_more_button2').addEventListener('click', function() {
    toggleDisplay('see_more2');
});