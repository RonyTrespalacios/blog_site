document.addEventListener('DOMContentLoaded', function() {
    // Alerta de bienvenida cuando el usuario llega al sitio
    welcomeAlert();

    // Manejo del menú desplegable en la navegación
    setupDropdownMenu();

    // Función para mostrar una alerta de bienvenida
    function welcomeAlert() {
        alert('¡Bienvenido a Mi Blog!');
    }

    // Función para configurar el menú desplegable en la navegación
    function setupDropdownMenu() {
        const dropdown = document.querySelector('.dropdown');
        const dropdownToggle = document.querySelector('.dropdown-toggle');
        const dropdownMenu = document.querySelector('.dropdown-menu');

        // Verifica si los elementos necesarios existen antes de agregar eventos
        if (dropdown && dropdownToggle && dropdownMenu) {
            dropdownToggle.addEventListener('click', function(event) {
                event.preventDefault();
                dropdownMenu.classList.toggle('show');
            });

            // Cierra el menú si se hace clic fuera de él
            document.addEventListener('click', function(event) {
                if (!dropdown.contains(event.target)) {
                    dropdownMenu.classList.remove('show');
                }
            });
        }
    }
});