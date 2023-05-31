/* */
// use froze/include/field_froze_form.html
var items_source = ["Гардеробная комната", "Гостиная", "Двери-купе", "Дверь межкомнатная", "Детская комната", "Детская мягкая кровать", "Диван", "Зеркало", "Комод", "Корпусная Мебель", "Кухонный гарнитур", "Кухонный модуль", "Кровать корпусная", "Кровать мягкая", "Матрас", "Мебель в ванную комнату", "Мягкая мебель", "Офисная мебель", "Подключение техники клиента", "Полка", "Перегородка", "Прихожая", "Рабочая зона", "Ресепшн", "Свет", "Спальный гарнитур", "Стеллаж", "Стол обеденный", "Стол рабочий", "Стол журнальный", "Стол для макияжа", "Столешница", "Текстиль", "Торговое оборудование", "Тумба", "Фурнитура", "Фасад", "Шкаф-купе", "Шкаф распашной", "Шкаф-кровать", "Шкаф -перегородка", "Образец", "Техника", "Пуфик", "Прачечная", "Банкетка", "Кресло", "Панель мягкая", "Сиденье мягкое", "Кухонный остров", "Корпусный модуль", "Кухонная панель", "Панель мебельная", "Мебель для лоджий", "Подушки", "Барная стойка", "Дизайн интерьера", "Ковры и ковровые покрытия", "Декор", "Подарочный сертификат", "Сборка мебели", "ЭГО ПОДУШКИ мягкие", "Подоконники"];
$('.type_production').tagsinput({
  typeahead: {
    source: items_source
  },
  onTagExists: function(item, $tag) {
    $tag.hide.fadeIn();
  },
  freeInput: false
});


$('.bootstrap-tagsinput').change(function(){
  $(this).find('input').val('');
});
/* */
function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }