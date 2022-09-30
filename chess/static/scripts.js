game = true
const socket = io();

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
    var id = $('h4.game-id').attr('data-i')
    socket.emit('take', {'x': x, 'y': y, 'id': id})       
});

$(document).on('click', '.square[data-a="1"]', function() {
    $('.square[data-m="2"]').attr('data-m', '1')
    $(this).attr('data-a', '0');       
});


