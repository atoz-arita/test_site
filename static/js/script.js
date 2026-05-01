$(function () {
    // TOPへ戻る
    var topBtn = $('#pagetop');
    topBtn.hide();

    //ボタンの表示設定
    $(window).scroll(function () {
        if ($(this).scrollTop() > 800) {
            //---- 画面を800pxスクロールしたら、ボタンを表示する
            topBtn.fadeIn();
        } else {
            //---- 画面が800pxより上なら、ボタンを表示しない
            topBtn.fadeOut();
        }
    });

    //ボタンをクリックしたら、スクロールして上に戻る
    topBtn.click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 500);
        return false;
    });
});
// ここまで

// ハンバーガー
var hamburger = document.querySelector('.hamburger-menu');
var navMenu = document.querySelector('.nav-menu');

hamburger.addEventListener('click', function () {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
    var isOpen = navMenu.classList.contains('active');
    var items = navMenu.querySelectorAll('a');

    if (isOpen) {
        items.forEach(function (item, idx) {
            setTimeout(function () {
                item.classList.add('show');
            }, 250 + idx * 150);
        });
    } else {
        items.forEach(function (item) {
            item.classList.remove('show');
        });
    }
});
// ここまで