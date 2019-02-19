$(document).ready(function() {
    // 1. Visualizing things on hover
    $('#stars li').on('mouseover', function() {
        // the star currently mouse on
        var onStar = parseInt($(this).data('value'), 10);

        // highlight all the stars that's not after the current hovered star
        $(this).parent().children('li.star').each(function(e) {
            if (e < onStar) {
                $(this).addClass('hover');
            } else {
                $(this).removeClass('hover')
            }
        });
    }).on('mouseout', function() {
        $(this).parent().children('li.star').each(function(e) {
            $(this).removeClass('hover');
        });
    });

    // 2. Action to perform on click
    $('#stars li').on('click', function() {
        var onStar = parseInt($(this).data('value'), 10);
        var stars = $(this).parent().children('li.star')
        for (var i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }
        for (var i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }
    })
})