$(document).ready(function(){
    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем id товара
        var id = $(this).prop("id");
        // Берем token корзины
        var carttoken  = $(this).children("input").prop("value");
        // Ищем ближайшеий .quantity с количеством 
        var $input = $(this).prev().text();
        // Берем значение количества товара
        var currentValue = parseInt($input);
        // Если количества больше одного, то только тогда делаем -1
        var newVal = (currentValue -1);

        $(this).prev().text(newVal);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            decreaset(-1, id, carttoken);
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем id товара
        var id = $(this).prop("id");
        // Берем token корзины
        var carttoken  = $(this).children("input").prop("value");
        // Ищем ближайшеий .quantity с количеством 
        var $input = $(this).prev().text();
        // Берем значение количества товара
        var currentValue = parseInt($input);
        // Если количества больше одного, то только тогда делаем -1
        var newVal = (currentValue + 1);

        $(this).prev().text(newVal);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(1, id, carttoken);
    });


function updateCart(newVal, id, carttoken) {

    $.ajax({
        method: "POST",
        url: "add/"+id,
        data: {
            csrfmiddlewaretoken :	carttoken,
            quantity:	newVal,
            update:	"False",
        },
        success: function (data) {
            location.reload();
            
            //  // Сообщение
            // successMessage.html(data.message);
            // successMessage.fadeIn(400);
            //  // Через 7сек убираем сообщение
            // setTimeout(function () {
            //      successMessage.fadeOut(400);
            // }, 7000);

            // Изменяем количество товаров в корзине
            // var goodsInCartCount = $(".total_price");
            // var cartCount = parseInt(goodsInCartCount.text() || 0);
            // alert(cartCount)
            // cartCount += change;
            // goodsInCartCount.text(cartCount);

            // // Меняем содержимое корзины
            // var cartItemsContainer = $("#cart-items-container");
            // cartItemsContainer.html(data.cart_items_html);

        },
        error: function (data) {
            console.log("Ошибка при добавлении товара в корзину");
        },
    });
}
function decreaset(newVal, id, carttoken) {

    $.ajax({
        method: "POST",
        url: "decrease_item_quantity/"+id,
        data: {
            csrfmiddlewaretoken :	carttoken,
            quantity:	newVal,
            update:	"False",
        },
        success: function (data) {
            location.reload();
        },
        error: function (data) {
            console.log("Ошибка при обнавлении корзины");
        },
    });
}
});

// Берем из разметки элемент по id - оповещения от django
var notification = $('.messages');
// И через 7 сек. убираем
if (notification.length > 0) {
    setTimeout(function () {
        notification.alert('close');
    }, 4500);
}

// Обработчик события радиокнопки выбора способа доставки
$("input[name='requires_delivery']").change(function () {
    var selectedValue = $(this).val();
    // Скрываем или отображаем input ввода адреса доставки
    if (selectedValue === "1") {
        $("#deliveryAddressField").show();
    } else {
        $("#deliveryAddressField").hide();
    }
});