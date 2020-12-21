function main(){
    anime({
        targets: '.is-pulsating',
        opacity: 0,
        easing: "easeInOutSine",
        direction: 'alternate',
        loop: true
    });

    var t1 = anime.timeline();

    t1.add({
        targets: '.layer0',
        keyframes: [
            {height:500},
            {width: 360},
        ],
        easing: "easeOutExpo",
        duration: 1500
    })

    t1.add({
        targets: '.layer1',
        keyframes: [
            {height:500},
            {width: 350},
        ],
        easing: "easeOutExpo",
        duration: 1500
    }, 100)

    t1.add({
        targets: '.slide-fade-down',
        opacity: [0,1],
        translateY: [-200,0],
        easing: "easeOutExpo",
        delay: anime.stagger(200),
        duration: 600
    })
    /*

    */
}

document.addEventListener("DOMContentLoaded", main);