// для увеличения фото/картинки на тёмном фоне
// Добавить в html
// <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
// <script type="text/javascript" src="{% static 'main/js/popup_img.js' %}"></script>

$(document).ready(function() { // Ждём загрузки страницы

	$(".image").click(function(){	// Событие клика на маленькое изображение
	  	var img = $(this);	// Получаем изображение, на которое кликнули
		var src = img.attr('src'); // Достаем из этого изображения путь до картинки
    console.log('src', src)
    let arr = src.split('/')
    if(arr.at(-1) === 'dvk.png') {
      arr[arr.length - 1] = 'dvk1.jpeg'
    } else if(arr.at(-1) === 'ES.png') {
      arr[arr.length - 1] = 'ES18411.jpeg'
    } else if(arr.at(-1) === 'Me.png') {
      arr[arr.length - 1] = 'me1.png'
    } else if(arr.at(-1) === 'pc_byte.png') {
      arr[arr.length - 1] = 'pc_byte1.jpg'
    }
    src = arr.join('/')
    console.log()

		$("body").append("<div class='popup_i'>"+ //Добавляем в тело документа разметку всплывающего окна
						 "<div class='popup_bg'></div>"+ // Блок, который будет служить фоном затемненным
						 "<img src='"+src+"' class='popup_img' />"+ // Само увеличенное фото
						 "</div>");
		console.log('Pressed')
		$(".popup_i").fadeIn(200); // Медленно выводим изображение
		$(".popup_bg").click(function(){	// Событие клика на затемненный фон
			$(".popup_i").fadeOut(200);	// Медленно убираем всплывающее окн
      setTimeout(function() {	// Выставляем таймер
			  $(".popup_i").remove(); // Удаляем разметку всплывающего окна
			}, 200);
		});
    $(".popup_img").click(function(){	// Событие клика на затемненный фон
			$(".popup_i").fadeOut(200);	// Медленно убираем всплывающее окн
      setTimeout(function() {	// Выставляем таймер
			  $(".popup_i").remove(); // Удаляем разметку всплывающего окна
			}, 200);
		});
	});

});

// для вывода модального окна
$(document).ready(function(){
            $("#staticBackdrop").modal('show');
        });
