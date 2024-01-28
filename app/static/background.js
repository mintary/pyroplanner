document.addEventListener('DOMContentLoaded', function () {
    var total_seconds = document.getElementById('data-container').getAttribute('total_seconds');
    var seconds_left = document.getElementById('data-container').getAttribute('seconds_left');

    console.log(total_seconds)
    console.log(seconds_left)

    percentage = (seconds_left / total_seconds)

    var backgroundContainer = document.getElementById('background-container');
    var images = [
        'static/pixil-frame-0.png',
        'static/pixil-frame-1.png',
        'static/pixil-frame-2.png',
        'static/pixil-frame-3.png',
        'static/pixil-frame-4.png',
        'static/pixil-frame-5.png',
        'static/pixil-frame-6.png',

    ]; 

    function changeBackground(currentIndex) {
        backgroundContainer.style.backgroundImage = 'url(' + images[currentIndex] + ')';
        currentIndex = (currentIndex + 1) % images.length;
    }

    if (seconds_left<0)
        changeBackground(6)
    else if (percentage > 0 && percentage < 14) 
        changeBackground(0)
    else if (percentage >= 14 && percentage < 28)
        changeBackground(1)
    else if (percentage >= 28 && percentage < 42)
        changeBackground(2)
    else if (percentage >= 42 && percentage < 56)
        changeBackground(3)
    else if (percentage >= 56 && percentage < 70)
        changeBackground(4)
    else if (percentage >= 70 && percentage < 84)
        changeBackground(5)
    else if (percentage >= 84 && percentage < 100)
        changeBackground(6)
    else
        changeBackground(0)
    
});