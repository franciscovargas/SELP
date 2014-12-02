function showPassword() {

    var key_attr = $('#key').attr('type');
    var key_attr2 = $('#key2').attr('type');

    if(key_attr != 'text' && key_attr2 != 'text') {

        $('.checkbox').addClass('show');
        $('#key').attr('type', 'text');
        $('#key2').attr('type', 'text');

    } else {

        $('.checkbox').removeClass('show');
        $('#key').attr('type', 'password');
        $('#key2').attr('type', 'password');

    }

}
