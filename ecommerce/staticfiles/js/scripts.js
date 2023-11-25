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

document.addEventListener('DOMContentLoaded', (event) => {
  function copyShippingToBilling() {
      document.getElementById('copyButton').addEventListener('click', function() {
          var shippingInputs = document.querySelectorAll('[name^="shipping-"]');
          shippingInputs.forEach(function(shippingInput) {
              var fieldName = shippingInput.name.replace('shipping-', '');
              var billingInput = document.querySelector('[name="billing-' + fieldName + '"]');
              if (billingInput) {
                  billingInput.value = shippingInput.value;
              }
          });
      });
  }
  copyShippingToBilling();
});