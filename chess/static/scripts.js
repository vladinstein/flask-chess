const socket = io();
'use strict';

window.addEventListener('DOMContentLoaded', function addpieces() {
    var y = $('.square[data-x="8"][data-square="1"]').attr("data-y")
    if (y == 1 || y == 5) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '32px'})
    } else if (y == 2 || y == 6) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '97px'})
    } else if (y == 3 || y == 7) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '162px'})
    } else if (y == 4 || y == 8) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '227px'})
    }
    var y = $('.square[data-x="1"][data-square="7"]').attr("data-y")
    if (y == 8 || y == 4) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '32px'})
    } else if (y == 7 || y == 3) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '97px'})
    } else if (y == 6 || y == 2) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '162px'})
    } else if (y == 5 || y == 1) {
        $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '227px'})
    }
    var squares = document.querySelectorAll(".square");
    squares.forEach(function (square)
    {
        piece = square.getAttribute('data-square');
        moving = square.getAttribute('data-m');
        if (piece == 1) {
        square.innerHTML = '&#9817;'
        } else if (piece == 2) {
        square.innerHTML = '&#9816;'    
        } else if (piece == 3) {
        square.innerHTML = '&#9815;'
        } else if (piece == 4) {
        square.innerHTML = '&#9814;'
        } else if (piece == 5) {
        square.innerHTML = '&#9813;'
        } else if (piece == 6) {
        square.innerHTML = '&#9812;'
        } else if (piece == 7) {
        square.innerHTML = '&#9823;'
        } else if (piece == 8) {
        square.innerHTML = '&#9822;'
        } else if (piece == 9) {
        square.innerHTML = '&#9821;'
        } else if (piece == 10) {
        square.innerHTML = '&#9820;'
        } else if (piece == 11) {
        square.innerHTML = '&#9819;'
        } else if (piece == 12) {
        square.innerHTML = '&#9818;'
        } else if (piece == 0) {
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
    var piece = $(this).attr('data-square')
    socket.emit('touch', {'x': x, 'y': y, 'piece': piece})     
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
    var text = $('.square[data-a="1"]').html()
        piece = $('.square[data-a="1"]').attr('data-square')
        text2 = $(this).html()
        piece2 = $(this).attr('data-square')
        x = $(this).attr('data-x')
        y = $(this).attr('data-y')
        i = $('.square[data-a="1"]').attr('data-x')
        j = $('.square[data-a="1"]').attr('data-y')
    if (piece == 6 && piece2 == 4 && $(this).attr('data-y') == 8) {
        $('.square[data-x="1"][data-y="6"]').html(text2)
        $('.square[data-x="1"][data-y="6"]').attr('data-square', piece2)
        $('.square[data-x="1"][data-y="7"]').html(text)
        $('.square[data-x="1"][data-y="7"]').attr('data-square', piece)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if (piece == 6 && piece2 == 4 && $(this).attr('data-y') == 1) {
        $('.square[data-x="1"][data-y="4"]').html(text2)
        $('.square[data-x="1"][data-y="4"]').attr('data-square', piece2)
        $('.square[data-x="1"][data-y="3"]').html(text)
        $('.square[data-x="1"][data-y="3"]').attr('data-square', piece)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if (piece == 12 && piece2 == 10 && $(this).attr('data-y') == 8) {
        $('.square[data-x="8"][data-y="6"]').html(text2)
        $('.square[data-x="8"][data-y="6"]').attr('data-square', piece2)
        $('.square[data-x="8"][data-y="7"]').html(text)
        $('.square[data-x="8"][data-y="7"]').attr('data-square', piece)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if (piece == 12 && piece2 == 10 && $(this).attr('data-y') == 1) {
        $('.square[data-x="8"][data-y="4"]').html(text2)
        $('.square[data-x="8"][data-y="4"]').attr('data-square', piece2)
        $('.square[data-x="8"][data-y="3"]').html(text)
        $('.square[data-x="8"][data-y="3"]').attr('data-square', piece)
        $(this).html('')
        $(this).attr('data-square', '0')
    } else if ((piece == 1 || piece == 7) && piece2 == 0 && 
    Math.abs($(this).attr('data-y') - $('.square[data-a="1"]').attr('data-y')) == 1) {
        $(this).html(text)
        $(this).attr('data-square', piece)
        $('.square[data-x=' + i + '][data-y=' + y +']').attr('data-square', '0')
        $('.square[data-x=' + i + '][data-y=' + y +']').html('')
    } else if (piece == 1 && x == 8 ) {
        $(this).html(text)
        $(this).attr('data-square', piece)
        $('.selection > .square').attr('data-i', i)
        $('.selection > .square').attr('data-j', j)
        if (y == 1 || y == 5) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '32px'})
        } else if (y == 2 || y == 6) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '97px'})
        } else if (y == 3 || y == 7) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '162px'})
        } else if (y == 4 || y == 8) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '227px'})
        }
    } else if (piece == 7 && x == 1) {
        $(this).html(text)
        $(this).attr('data-square', piece)
        $('.selection > .square').attr('data-i', i)
        $('.selection > .square').attr('data-j', j)
        if (y == 8 || y == 4) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '32px'})
        } else if (y == 7 || y == 3) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '97px'})
        } else if (y == 6 || y == 2) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '162px'})
        } else if (y == 5 || y == 1) {
            $('.selection').css({'visibility': 'visible', 'opacity': '1', 'margin-left': '227px'})
        }
    } else {
        $(this).html(text)
        $(this).attr('data-square', piece)
    }
    $('.square[data-a="1"]').html('')
    $('.square[data-a="1"]').attr('data-square', '0')
    $('.square[data-a="1"]').attr('data-a', '0')  
    $('.square[data-go="1"]').attr('data-go', '0')  
    $('.square[data-attack="1"]').attr('data-attack', '0')
    if (!(piece == 1 && x == 8 ) && !(piece == 7 && x == 1)) {
        $('.your_move').addClass('hidden')
        socket.emit('go', {'i': i, 'j': j, 'x': x, 'y': y, 'piece': piece, 'piece2': piece2})
    }
});

$(document).on('click', '.selection > .square', function() {
    $('.selection').css({'visibility': 'hidden', 'opacity': '0'})
    var text = $(this).html()
        piece = $(this).attr('data-square')
        i = $(this).attr('data-i')
        j = $(this).attr('data-j')
    if (piece > 6) {
        var x = $('.square[data-x="1"][data-square="7"]').attr('data-x')
            y = $('.square[data-x="1"][data-square="7"]').attr('data-y')
            piece2 = 7
        $('.square[data-x="1"][data-square="7"]').html(text)
        $('.square[data-x="1"][data-square="7"]').attr('data-square', piece)
    } else {
        var x = $('.square[data-x="8"][data-square="1"]').attr('data-x')
            y = $('.square[data-x="8"][data-square="1"]').attr('data-y')
            piece2 = 1
        $('.square[data-x="8"][data-square="1"]').html(text)
        $('.square[data-x="8"][data-square="1"]').attr('data-square', piece)
    }
    $('.your_move').addClass('hidden')
    socket.emit('go', {'i': i, 'j': j, 'x': x, 'y': y, 'piece': piece, 'piece2': piece2})
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
        piece = data['piece']
        piece2 = data['piece2']
        if (data['promotion'] == true) {
            if (piece == 2) {
                var text = '&#9817;'
            } else if (piece == 2) {
                var text = '&#9816;'    
            } else if (piece == 3) {
                var text = '&#9815;'
            } else if (piece == 4) {
                var text = '&#9814;'
            } else if (piece == 5) {
                var text = '&#9813;'
            } else if (piece == 8) {
                var text = '&#9822;'
            } else if (piece == 9) {
                var text = '&#9821;'
            } else if (piece == 10) {
                var text = '&#9820;'
            } else if (piece == 11) {
                var text = '&#9819;'
            } 
        } else {
            var text = $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').html()
        }
        if (data['castling'] == true) {
            if (piece == 6 && piece2 == 4 && data['y'] == 8) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="1"][data-y="7"]').html('&#9812;')
                $('.square[data-x="1"][data-y="7"]').attr('data-square', '6')
                $('.square[data-x="1"][data-y="6"]').html('&#9814;')
                $('.square[data-x="1"][data-y="6"]').attr('data-square', '4')
            } else if (piece == 6 && piece2 == 4 && data['y'] == 1) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="1"][data-y="3"]').html('&#9812;')
                $('.square[data-x="1"][data-y="3"]').attr('data-square', '6')
                $('.square[data-x="1"][data-y="4"]').html('&#9814;')
                $('.square[data-x="1"][data-y="4"]').attr('data-square', '4')
            } else if (piece == 12 && piece2 == 10 && data['y'] == 8) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="8"][data-y="7"]').html('&#9818;')
                $('.square[data-x="8"][data-y="7"]').attr('data-square', '12')
                $('.square[data-x="8"][data-y="6"]').html('&#9820;')
                $('.square[data-x="8"][data-y="6"]').attr('data-square', '10')
            } else if (piece == 12 && piece2 == 10 && data['y'] == 1) {
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
                $('.square[data-x="8"][data-y="3"]').html('&#9818;')
                $('.square[data-x="8"][data-y="3"]').attr('data-square', '12')
                $('.square[data-x="8"][data-y="4"]').html('&#9820;')
                $('.square[data-x="8"][data-y="4"]').attr('data-square', '10')
            }
        } else {
            $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').html(text)
            $('.square[data-x=' + data['x'] + '][data-y=' + data['y'] + ']').attr('data-square', piece)
            if (data['en_passant'] == true) {
                $('.square[data-x=' + data['i'] + '][data-y=' + data['y'] + ']').html('')
                $('.square[data-x=' + data['i'] + '][data-y=' + data['y'] + ']').attr('data-square', '0')
            }
        }
        $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').html('')
        $('.square[data-x=' + data['i'] + '][data-y=' + data['j'] + ']').attr('data-square', '0')
    })
    socket.on('remove_check', () => {
        if (!$('.under_check').hasClass('hidden')) {
            $('.under_check').toggleClass('hidden')
        }
    })
    socket.on('switch_move', () => {
        $('.opp_move').removeClass('hidden')
    })
    socket.on('next_move', (data)=>{
        $('.square[data-m="2"]').attr('data-m', '0')
        for (let obj of Object.values(data['moving'])) {
            $('.square[data-x=' + obj[0] + '][data-y=' + obj[1] + ']').attr('data-m', '1')
            }
        if ((data['check'] == true && $('.under_check').hasClass('hidden')) || (data['check'] == false && 
        !$('.under_check').hasClass('hidden'))) {
            $('.under_check').toggleClass('hidden')
        } else {
            $('.your_move').removeClass('hidden')
        }    
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
    socket.on('change_flash_first', ()=>{
        $(".alert-success").html('Your opponent has connected.')
        setTimeout(function() {
            $(".alert-success").hide()
        }, 5000);
    })
    socket.on('change_flash_second', ()=>{
        setTimeout(function() {
            $(".alert-success").hide()
        }, 5000);
    })
});

