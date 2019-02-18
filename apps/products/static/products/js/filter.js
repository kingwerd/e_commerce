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
        success: function(serverResponse) {
            document.getElementById('products').innerHTML = serverResponse
        }
    })
})