var sliders = document.querySelectorAll(".price-slider input");
var min = document.getElementById('min-price')
var max = document.getElementById('max-price')
min.innerText = sliders[0].value
max.innerText = sliders[1].value
function updatePriceLabels() {
    sliders = document.querySelectorAll(".price-slider input");
    val1 = parseInt(sliders[0].value);
    val2 = parseInt(sliders[1].value);
    min.innerText = sliders[0].value
    max.innerText = sliders[1].value
    if (val1 >= val2) {
        sliders[0].value = val2 - 3;
        return;
    }
    if (val2 <= val1) {
        sliders[1].value = val1 + 3;
        return;
    }
    
    if (val1 > 0 || val2 < 99) {
        sliders[0].style.background = sliders[1].style.background = 'sliders[0].style.background = sliders[1].style.background = "-webkit-gradient(linear, 0 0,100% 0, color-stop(0, white), color-stop(" + (val1 / 100) + ", white),color-stop(" + (val1 / 100) + ", #f0f0f0), color-stop(" + (val2 / 100) + ", #f0f0f0), color-stop(" + (val2 / 100) + ", white))";'
    }
    else {
        sliders[0].style.background = sliders[1].style.background = '';
    }
}
