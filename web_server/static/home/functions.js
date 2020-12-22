function startStream(){
    console.log("Start stream button pressed");
}

function enterConfig(){
    console.log("Starting config menu");
}


function main(){

    function addButtonEvents(){
        var buttons = document.querySelectorAll('.animated-button');  // Select elements with animated button class


        function enterButton(button) {
            // This function defines the animation for when the cursor enters the button
            anime.remove(button);
            anime({
                targets: button,
                scale: 1.1,
                backgroundColor: '#7d0000',
                duration: 500,
                easing: "easeOutExpo"
            });

            anime({
                // Grow the title text as well
                targets: ".secondary-font",
                scale: 1.1,
                duration: 2000,
                easing: "easeOutExpo"
            });
        };

        function leaveButton(button) {
            // This function defines the animation for when the cursor leaves the button
            anime.remove(button);
            anime({
                targets: button,
                scale: 1,
                backgroundColor: '#FFF',
                duration: 500,
                easing: "easeOutExpo"
            });
            // Shrink back title text
            anime({
                targets: ".secondary-font",
                scale: 1,
                duration: 2000,
                easing: "easeInOutSine"
            });
        };

        for (var i = 0; i < buttons.length; i++) {
            // Loop through all the buttons on the web page and add their event listeners

            // Adding "mouse enter" event listener
            buttons[i].addEventListener('mouseenter', function(e) {
                enterButton(e.target);
            }, false);

            // Adding "mouse leave" event listener
            buttons[i].addEventListener('mouseleave', function(e) {
                leaveButton(e.target)
            }, false);
        }
    }

    anime({
        targets: '.is-pulsating',
        opacity: 0,
        easing: "easeInOutSine",  // See easing types here: https://easings.net/
        direction: 'alternate', // This means the direction switches each time the animation loops
        loop: true  // This animation will loop infinitely
    });

    // Create new animation timeline
    var t1 = anime.timeline();

    t1.add({
        // Animate first layer (red layer)
        targets: '.layer0',
        keyframes: [
            {height:500},
            {width: 360},
        ],
        easing: "easeOutExpo",
        duration: 1500
    })

    t1.add({
        // Animate second layer (white layer)
        targets: '.layer1',
        keyframes: [
            {height:500},
            {width: 350},
        ],
        easing: "easeOutExpo",
        duration: 1500
    }, 100)  // this starts 100ms into the timeline rather than after layer0 finishes, so they are offset by 100ms

    t1.add({
        targets: '.slide-fade-down',
        opacity: [0,1],
        translateY: [-200,0],
        easing: "easeOutExpo",
        delay: anime.stagger(200),  // Each element with the slide-fade-down class will animate 200ms after the last
        duration: 600,
        complete:addButtonEvents()
        // Not adding the button event listeners until after the entry animation has completed else it causes bugs
    })

}

// Don't run any of these animation functions until the document has fully loaded else some elements may be missing
// When I didn't have this none of the animations worked
document.addEventListener("DOMContentLoaded", main);


