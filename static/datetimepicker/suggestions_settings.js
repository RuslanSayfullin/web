$("#address_client").suggestions({
    token: "3e7e6b4c7e08d5b71d314a106d4a5349a1277e80",
    type: "ADDRESS",
    /* Вызывается, когда пользователь выбирает одну из подсказок */
    onSelect: function (suggestion) {
        console.log(suggestion);
    }
});