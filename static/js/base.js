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

// FIXME: see https://github.com/timschlechter/bootstrap-tagsinput/issues/386
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
$('.delete-froze-status').on('click', function(e){
  if (!confirm("Вы хотите удалить статус?")) {
    return false;
  }
  var el = $(this);
  $.ajax({
    url: el.data("url"),
    method: "post",
    headers: {
      "X-CSRFToken": getCookie('csrftoken')
    }
  }).done(function(){
    el.css("display", "none");
    var parent = el.parent().parent().parent();
    parent.animate({
      opacity: 0.2
    }, {
      duration: 1000,
      complete:function() {
        parent.css("display", "none");
      }
    });
  });
  return false;
});
/* */
// Use froze/include/froze_detail.html

$('.inline-edit-form-show').on('click', function (e) {
  e.preventDefault();
  var el = $(this);
  el.css("display", "none");
  el.siblings('.inline-edit-form-value').css("display", "none");
  el.siblings(".inline-edit-form").css("display", "inline");
});
$('.inline-edit-form-hidden').on('click', function (e) {
  e.preventDefault();
  var form = $(this).parent();
  form.css("display", "none");
  form.siblings(".inline-edit-form-show").css("display", "inline");
  form.siblings(".inline-edit-form-value").css("display", "inline");
});
$('.inline-edit-form').on('submit', function (e) {
  e.preventDefault();
  var form = $(this);
  $.ajax({
    'url': form.attr("action"),
    'method': "post",
    'data': form.serialize()
  }).done(function () {
    form.children().removeClass("disabled");
    var input_name = form.find(".input-sm")[0];
    form.css("display", "none");
    form.next(".inline-edit-form-value")[0].innerText = input_name.value;
    form.siblings(".inline-edit-form-show").css("display", "inline");
    form.siblings(".inline-edit-form-value").css("display", "inline");
  }).fail(function () {
    form.children().removeClass("disabled");
  });
});
/* */
$(document).ready(function(){
      if (window.innerWidth <= 1024) {
          $('#calendar').addClass("table-responsive");
      }
});

$(document).ready(function () {
  $.each($(".hide_designer"), function(index, l){
    var designer_id = $(l).attr("data-froze-designer");
    if (localStorage["designer_pk_"+designer_id]) {
      $(l).parent().parent().css({"display": "none"});
      $(l).text("показать");
    } else {
      $(l).text("скрыть");
    }
  });

  $(".hide_designer").on("click", function (e) {
    e.preventDefault();
    var designer_pk = $(this).attr("data-froze-designer");
    var key = "designer_pk_" + designer_pk;

    if (localStorage.getItem(key)) {
      $(this).text("скрыть");
      localStorage.removeItem(key);
    } else {
      $(this).text("показать");
      localStorage.setItem(key, designer_pk);
      $(this).parent().parent().css({"display": "none"});
    }

  });

  $("#show_hide_designer").on("click", function (e) {
    var checked = $("#show_hide_designer").prop( "checked" );

    $.each($(".hide_designer"), function (index, l) {
      var elem = $(l);
      var designer_id = elem.attr("data-froze-designer");
      var key = "designer_pk_" + designer_id;

      if (checked && localStorage.getItem(key)) {
          elem.parent().parent().css({"display": "table-row"});
      } else if (!checked && localStorage.getItem(key)) {
          elem.parent().parent().css({"display": "none"});
      }

    });
  });

});
$(".froze_file_delete").on("submit", function(e){
  e.preventDefault();
  var form = $(this);

  if (!confirm("Удалить выбранный файл?")) {
    return false;
  }

  $.ajax({
    method: form.prop('method'),
    url: form.prop('action'),
    data: form.serialize()
  }).done(function(response){
    window.location = response["redirect_url"]
  })
});
/* */
(function(){
  $('a[href="'+window.location.href+'"]').addClass('active');
})()
/* */
$(function(){
  $(".action_send_inspection").submit(function(){
    $form = $(this);
    $btn = $(document.activeElement);

    $btn.button('loading');
    $form.prop('action', $btn.data('url'));
  });
});
/* */
$('.action__change_constructor').submit(function(event){
  event.preventDefault();
  $form = $(this);
  $.ajax({
    url: $form.prop('action'),
    method: $form.prop('method'),
    data: $form.serialize()
  }).success(function(){
    location.reload();
  })
})