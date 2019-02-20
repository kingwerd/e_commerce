$(document).ready(function() {

    $('.product-add').click(function() {
        $.ajax({
            url:'products/cart/modal',
            method: 'get',
            data: {
                'product': this.value
            },
            success: function(serverResponse) {
                document.getElementById('cart-modal').innerHTML = serverResponse
                $('#cart-modal').modal()
            }
        })
    });

    $('#cart-modal').on('shown.bs.modal', function (e) {
        $('#quantity').on('input', function() {
            quantity = this.value
            product_id = $('#product_id').val()
            url = `http://localhost:8000/cart/add/${product_id}/${quantity}`
            $('#product-confirm').attr('href', url)
        })
    })

})