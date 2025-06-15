(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
    
    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict
function buscarLibros(event) {
  event.preventDefault(); // Evita que el formulario haga submit normal

  const query = document.getElementById("inputBuscar").value.trim();
  if (!query) {
    document.getElementById("resultadosBusqueda").innerHTML = "<p>Ingrese un término para buscar.</p>";
    return;
  }

  fetch(`/buscar_ajax?query=${encodeURIComponent(query)}`)
    .then(response => {
      if (!response.ok) throw new Error("Error en la búsqueda");
      return response.json();
    })
    .then(data => {
      mostrarResultados(data);
    })
    .catch(error => {
      document.getElementById("resultadosBusqueda").innerHTML = `<p>Error: ${error.message}</p>`;
    });
}

function mostrarResultados(libros) {
  const contenedor = document.getElementById("resultadosBusqueda");

  if (libros.length === 0) {
    contenedor.innerHTML = "<p>No se encontraron libros.</p>";
    return;
  }

  let html = '<div class="row">';
  libros.forEach(libro => {
    html += `
      <div class="col-md-3 mb-4">
        <div class="card h-100">
          <img src="${libro.imagen_url}" class="card-img-top" alt="${libro.titulo}" />
          <div class="card-body">
            <h5 class="card-title">${libro.titulo}</h5>
            <p class="card-text">₲${libro.precio.toLocaleString()}</p>
            <button class="btn btn-primary" onclick="agregarAlCarritoPorId(${libro.id})">Agregar al carrito</button>
          </div>
        </div>
      </div>
    `;
  });
  html += '</div>';

  contenedor.innerHTML = html;
}

// Opcional: función para agregar al carrito usando el id (necesitarías ajustar tu carrito)
function agregarAlCarritoPorId(id) {
  alert("Agregar al carrito libro con id: " + id);
  // Aquí va la lógica para agregar al carrito según tu estructura real
}
