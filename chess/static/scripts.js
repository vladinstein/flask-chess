const socket = io();
'use strict';

socket.on("connect", () => {
    var id = $('h4.game-id').attr('data-i')
        creator = $('h4.game-id').attr('data-creator')
    socket.emit('info', {'id': id}) 
});

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
    var id = $('h4.game-id').attr('data-i')
    socket.emit('take', {'x': x, 'y': y, 'id': id, 'figure': figure})     
});

$(document).on('click', '.square[data-a="1"]', function() {
    $('.square[data-m="2"]').attr('data-m', '1')
    $(this).attr('data-a', '0');  
    $('.square[data-go="1"]').attr('data-go', '0')
    $('.square[data-attack="1"]').attr('data-attack', '0')  
});

$(document).on('click', '.square[data-go="1"], .square[data-attack="1"]', function() {
    $('.your_move').addClass('hidden')
    $('.opp_move').removeClass('hidden')
    var text = $('.square[data-a="1"]').html()
        figure = $('.square[data-a="1"]').attr('data-square')
        text2 = $(this).html()
        figure2 = $(this).attr('data-square')
    $(this).attr('data-former', figure2)
    $(this).attr('data-oldhtml', text2)
    $('.square[data-a="1"]').html('')
    $(this).html(text)
    $(this).attr('data-square', figure)
    var i = $('.square[data-a="1"]').attr('data-x')
        j = $('.square[data-a="1"]').attr('data-y')
    $('.square[data-a="1"]').attr('data-square', '0')
    $('.square[data-a="1"]').attr('data-a', '0')  
    $('.square[data-go="1"]').attr('data-go', '0')  
    $('.square[data-attack="1"]').attr('data-attack', '0')
    var x = $(this).attr('data-x')
        y = $(this).attr('data-y')
        id = $('h4.game-id').attr('data-i')    
    socket.emit('go', {'i': i, 'j': j, 'x': x, 'y': y, 'id': id, 'figure': figure})
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
        $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html(text)
        $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').html('')
        $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').attr('data-square', '0')
        $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', figure)
        if ((data['check'] == 1 && $('.under_check').hasClass('hidden')) || (data['check'] == 0 && 
        !$('.under_check').hasClass('hidden'))) {
            $('.under_check').toggleClass('hidden')
        }
    })
    socket.on('remove_check', () => {
        if (!$('.under_check').hasClass('hidden')) {
            $('.under_check').toggleClass('hidden')
        }
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
        $('.opp_move').addClass('hidden')
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

