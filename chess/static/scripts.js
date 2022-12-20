const socket = io();
'use strict';

window.addEventListener('DOMContentLoaded', function addfigures() {
    var squares = document.querySelectorAll(".square");
    squares.forEach(function (square)
    {
        figure = square.getAttribute('data-square');
        moving = square.getAttribute('data-m');
        if (figure == 1) {
        square.innerHTML = '&#9817;'
        } else if (figure == 2) {
        square.innerHTML = '&#9816;'    
        } else if (figure == 3) {
        square.innerHTML = '&#9815;'
        } else if (figure == 4) {
        square.innerHTML = '&#9814;'
        } else if (figure == 5) {
        square.innerHTML = '&#9813;'
        } else if (figure == 6) {
        square.innerHTML = '&#9812;'
        } else if (figure == 7) {
        square.innerHTML = '&#9823;'
        } else if (figure == 8) {
        square.innerHTML = '&#9822;'
        } else if (figure == 9) {
        square.innerHTML = '&#9821;'
        } else if (figure == 10) {
        square.innerHTML = '&#9820;'
        } else if (figure == 11) {
        square.innerHTML = '&#9819;'
        } else if (figure == 12) {
        square.innerHTML = '&#9818;'
        } else if (figure == 0) {
        square.innerHTML = ''
        }  
    });
}
);

// Thank God! https://stackoverflow.com/questions/16893043/jquery-click-event-not-working-after-adding-class

$(document).on('click', '.square[data-m="1"]', function() {
    $('.square[data-m="1"]').attr('data-m', '2') 
    $(this).attr('data-a', '1');
    var x = $(this).attr('data-x')
    var y = $(this).attr('data-y')
    var figure = $(this).attr('data-square')
    socket.emit('touch', {'x': x, 'y': y, 'figure': figure})     
});

$(document).on('click', '.square[data-a="1"]', function() {
    $('.square[data-m="2"]').attr('data-m', '1')
    $(this).attr('data-a', '0');  
    $('.square[data-go="1"]').attr('data-go', '0')
    $('.square[data-attack="1"]').attr('data-attack', '0')  
});

$(document).on('click', '.square[data-go="1"], .square[data-attack="1"]', function() {
    if (!$('.under_check').hasClass('hidden')) {
        $('.under_check').toggleClass('hidden')
    }
    $('.your_move').addClass('hidden')
    var text = $('.square[data-a="1"]').html()
        figure = $('.square[data-a="1"]').attr('data-square')
        text2 = $(this).html()
        figure2 = $(this).attr('data-square')
    if (figure == 6 && figure2 == 4 && $(this).attr('data-y') == 8) {
        $('.square[data-x="1"][data-y="6"]').html(text2)
        $('.square[data-x="1"][data-y="6"]').attr('data-square', figure2)
        $('.square[data-x="1"][data-y="7"]').html(text)
        $('.square[data-x="1"][data-y="7"]').attr('data-square', figure)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if (figure == 6 && figure2 == 4 && $(this).attr('data-y') == 1) {
        $('.square[data-x="1"][data-y="4"]').html(text2)
        $('.square[data-x="1"][data-y="4"]').attr('data-square', figure2)
        $('.square[data-x="1"][data-y="3"]').html(text)
        $('.square[data-x="1"][data-y="3"]').attr('data-square', figure)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if (figure == 12 && figure2 == 10 && $(this).attr('data-y') == 8) {
        $('.square[data-x="8"][data-y="6"]').html(text2)
        $('.square[data-x="8"][data-y="6"]').attr('data-square', figure2)
        $('.square[data-x="8"][data-y="7"]').html(text)
        $('.square[data-x="8"][data-y="7"]').attr('data-square', figure)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if (figure == 12 && figure2 == 10 && $(this).attr('data-y') == 1) {
        $('.square[data-x="8"][data-y="4"]').html(text2)
        $('.square[data-x="8"][data-y="4"]').attr('data-square', figure2)
        $('.square[data-x="8"][data-y="3"]').html(text)
        $('.square[data-x="8"][data-y="3"]').attr('data-square', figure)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if ((figure == 1 || figure == 7) && figure2 == 0 && 
    Math.abs($(this).attr('data-y') - $('.square[data-a="1"]').attr('data-y')) == 1) {
        $(this).html(text)
        $(this).attr('data-square', figure)
        var x = $('.square[data-a="1"]').attr('data-x')
            y = $(this).attr('data-y')
        $('.square[data-x=' + x + '][data-y=' + y +']').attr('data-square', '0')
        $('.square[data-x=' + x + '][data-y=' + y +']').html('')
    } else {
        $(this).html(text)
        $(this).attr('data-square', figure)
    }
    $('.square[data-a="1"]').html('')
    $('.square[data-a="1"]').attr('data-square', '0')
    var i = $('.square[data-a="1"]').attr('data-x')
        j = $('.square[data-a="1"]').attr('data-y')
    $('.square[data-a="1"]').attr('data-a', '0')  
    $('.square[data-go="1"]').attr('data-go', '0')  
    $('.square[data-attack="1"]').attr('data-attack', '0')
    var x = $(this).attr('data-x')
        y = $(this).attr('data-y')  
    socket.emit('go', {'i': i, 'j': j, 'x': x, 'y': y, 'figure': figure, 'figure2': figure2})
});

// https://stackoverflow.com/questions/34913675/how-to-iterate-keys-values-in-javascript
$(document).ready(function(){
    socket.on('moves', (go, attack)=>{
    for (let obj of Object.values(go)) {
        $('.square[data-x=' + obj[0] + '][data-y=' + obj[1] + ']').attr('data-go', '1')
    } 
    for (let obj of Object.values(attack)) {
        $('.square[data-x=' + obj[0] + '][data-y=' + obj[1] + ']').attr('data-attack', '1')
    }     
    })
    socket.on('opp_move', (data) => {
        var text = $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').html()
            figure = $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').attr('data-square')
            figure2 = $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square')
        if (data['castling'] == true) {
            if (figure == 6 && figure2 == 4 && data['y'] == 8) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="1"][data-y="7"]').html('&#9812;')
                $('.square[data-x="1"][data-y="7"]').attr('data-square', '6')
                $('.square[data-x="1"][data-y="6"]').html('&#9814;')
                $('.square[data-x="1"][data-y="6"]').attr('data-square', '4')
            } else if (figure == 6 && figure2 == 4 && data['y'] == 1) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="1"][data-y="3"]').html('&#9812;')
                $('.square[data-x="1"][data-y="3"]').attr('data-square', '6')
                $('.square[data-x="1"][data-y="4"]').html('&#9814;')
                $('.square[data-x="1"][data-y="4"]').attr('data-square', '4')
            } else if (figure == 12 && figure2 == 10 && data['y'] == 8) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="8"][data-y="7"]').html('&#9818;')
                $('.square[data-x="8"][data-y="7"]').attr('data-square', '12')
                $('.square[data-x="8"][data-y="6"]').html('&#9820;')
                $('.square[data-x="8"][data-y="6"]').attr('data-square', '10')
            } else if (figure == 12 && figure2 == 10 && data['y'] == 1) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="8"][data-y="3"]').html('&#9818;')
                $('.square[data-x="8"][data-y="3"]').attr('data-square', '12')
                $('.square[data-x="8"][data-y="4"]').html('&#9820;')
                $('.square[data-x="8"][data-y="4"]').attr('data-square', '10')
            }
        } else {
            $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html(text)
            $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', figure)
            if (data['en_passant'] == true) {
                $('.square[data-x=' + data['i'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['i'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
            }
        }
        $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').html('')
        $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').attr('data-square', '0')
        if ((data['check'] == true && $('.under_check').hasClass('hidden')) || (data['check'] == false && 
        !$('.under_check').hasClass('hidden'))) {
            $('.under_check').toggleClass('hidden')
        }
    })
    socket.on('remove_check', () => {
        if (!$('.under_check').hasClass('hidden')) {
            $('.under_check').toggleClass('hidden')
        }
    })
    socket.on('switch_move', () => {
        $('.opp_move').removeClass('hidden')
    })
    socket.on('next_move', (moving)=>{
        $('.square[data-m="2"]').attr('data-m', '0')
        for (let obj of Object.values(moving)) {
            $('.square[data-x=' + obj[0] + '][data-y=' + obj[1] + ']').attr('data-m', '1')
            } 
        $('.your_move').removeClass('hidden')
        $('.opp_move').addClass('hidden')
    })
    socket.on('checkmate', ()=>{
        $('.square[data-m="2"]').attr('data-m', '0')
        $('.checkmate').removeClass('hidden')
        $('.opp_move').addClass('hidden')
    })
    socket.on('victory', ()=>{
        $('.square[data-m="2"]').attr('data-m', '0')
        $('.victory').removeClass('hidden')
    })
    socket.on('stalemate', ()=>{
        $('.square[data-m="2"]').attr('data-m', '0')
        $('.stalemate').removeClass('hidden')
        $('.opp_move').addClass('hidden')
    })
    socket.on('connected', (moving)=>{
        $('.waiting').addClass('hidden')
        $('.your_move').removeClass('hidden')
        for (let obj of Object.values(moving)) {
            $('.square[data-x=' + obj[0] + '][data-y=' + obj[1] + ']').attr('data-m', '1')
            } 
    })
    socket.on('wait_move_status', ()=>{
        $('.waiting').addClass('hidden') 
        $('.opp_move').removeClass('hidden')
    })

});

