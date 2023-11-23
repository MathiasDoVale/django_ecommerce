function changeImage(newImageUrl, defaultImageId, event) {
  // Cambia la imagen principal
  document.getElementById(defaultImageId).src = newImageUrl;

  // Elimina la clase 'thumbnail-selected' de todas las miniaturas
  var thumbnails = document.getElementsByClassName('thumbnail');
  for (var i = 0; i < thumbnails.length; i++) {
    thumbnails[i].classList.remove('thumbnail-selected');
  }

  // Agrega la clase 'thumbnail-selected' a la miniatura seleccionada
  event.target.classList.add('thumbnail-selected');
}


var selectedSize = null;
function selectSize(button, product_id) {
  selectedSize = button.value;
  var addToCartButton = document.getElementById('add-to-cart-button-'+ product_id);
  var urlBase = addToCartButton.getAttribute('data-url-base');
  addToCartButton.href = urlBase + "?product_id=" + product_id + "&size=" + selectedSize;
}