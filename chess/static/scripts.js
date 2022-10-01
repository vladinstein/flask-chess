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
    var id = $('h4.game-id').attr('data-i')
    socket.emit('take', {'x': x, 'y': y, 'id': id, 'figure': figure})       
});

$(document).on('click', '.square[data-a="1"]', function() {
    $('.square[data-m="2"]').attr('data-m', '1')
    $(this).attr('data-a', '0');  
    $('.square[data-go="1"]').attr('data-go', '0')  
});

$(document).on('click', '.square[data-go="1"]', function() {
    var text = $('.square[data-a="1"]').html()
    $('.square[data-a="1"]').html($(this).html())
    $(this).html(text)
    var i = $('.square[data-a="1"]').attr('data-x')
        j = $('.square[data-a="1"]').attr('data-y')
    $('.square[data-a="1"]').attr('data-a', '0')  
    $('.square[data-go="1"]').attr('data-go', '0')  
    var x = $(this).attr('data-x')
        y = $(this).attr('data-y')
        id = $('h4.game-id').attr('data-i')
    socket.emit('go', {'i': i, 'j': j, 'x': x, 'y': y, 'id': id, 'figure': figure})
});

// https://stackoverflow.com/questions/34913675/how-to-iterate-keys-values-in-javascript
$(document).ready(function(){
    socket.on('moves', (go, attack)=>{
    for (const [key, value] of Object.entries(go)) {
    $('.square[data-x=' + key + '][data-y=' + value + ']').attr('data-go', '1')
    }    
    for (const [key, value] of Object.entries(attack)) {
    $('.square[data-x=' + key + '][data-y=' + value + ']').attr('data-attack', '1')
    }       
    })
})
