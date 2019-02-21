// filter by search
$('#item_search').on('input', function() {
    $.ajax({
        url: 'products/search',
        method: 'get',
        data: this.value,
        success: function(res) {
            console.log(res)
        }
    })
})

// filter by category
$('#category_filter').change(function(e){
    $.ajax({
        url:'products/filter',
        method: 'get',
        data: $(this).serialize(),
        success: function(res) {
            document.getElementById('products').innerHTML = res
        }
    })
})

$('#min-price-slider').change(function(e) {
    filter_price()
})
$('#max-price-slider').change(function(e) {
    filter_price()
})
function filter_price() {
    $.ajax({
        url: 'products/filter/price',
        method: 'get',
        data: $('#price-slider-form').serialize(),
        success: function(res) {
            document.getElementById('products').innerHTML = res
        }
    })
}
