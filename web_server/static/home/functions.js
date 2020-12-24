function startStream(){
    console.log("Start stream button pressed");
}

function changeHotkey(key){
    var button = document.getElementById(key);
    var button_prev_text = button.innerText;
    button.innerText = "[editing]";
    anime({
        targets: button,
        scale: 0.8,
        backgroundColor: '#7d0000',
        color: '#FFF',
        duration: 500,
        easing: "easeOutExpo"
    });
    var url = config_update_hotkey_route + "?hotkey_name=" + key;
    $.get(url, function(data, status){
        if ( data["success"] == "true" ){
            button.innerText = data["hotkey_string"];
            var t3 = anime.timeline();
            t3.add({
                targets: button,
                scale: 1,
                backgroundColor: '#8aff70',
                color: '#000000',
                duration: 500,
                easing: "easeOutExpo"
            })
            t3.add({
                targets: button,
                scale: 1,
                backgroundColor: '#FFF',
                duration: 500,
                easing: "easeOutExpo"
            })
        } else {
            alert(data["error"]);
            anime({
                targets: button,
                scale: 1,
                backgroundColor: '#FFF',
                color: '#000000',
                duration: 500,
                easing: "easeOutExpo"
            });
            console.log(button_prev_text);
            button.innerHTML = button_prev_text;
        }
    });
}

function enterConfig(){
    console.log("Starting config menu");

    // Create new animation timeline
    var t2 = anime.timeline();

    $('#title-text').text("Config");



    t2.add({
        // Animate first layer (red layer)
        targets: '.layer0',
        height: 800,
        width: 600,
        easing: "easeOutExpo",
        duration: 1500
    })

    t2.add({
        // Animate second layer (white layer)
        targets: '.layer1',
        height: 790,
        width: 590,
        easing: "easeOutExpo",
        duration: 1500,
        complete: function(){
            $('#config-container').show();
        }

    }, '-=1500')

    t2.add({
        targets: '#home-contents',
        opacity: 0,
        easing: 'easeOutExpo',
        duration: 1000,
        complete: function(){
            $('#home-contents').hide();
        }
    }, 0)

    t2.add({
    targets: '#config-container',
        opacity: [0,1],
        translateY: [-200,0],
        easing: "easeOutExpo",
        delay: anime.stagger(200),  // Each element with the slide-fade-down class will animate 200ms after the last
        duration: 600,
    })
}

function saveConfig(){
    /*
    TODO: Add error handling
    Use jQuery.AJAX instead of .getJSON to include a timeout in case the web server is not online
    */
    $.getJSON(route, function(data, status){  // Get existing JSON config data
        if (status == "success"){
            console.log("Successfully retrieved current config data")
            console.log(data);
            console.log(status);
            var config_dict = data;
            // Select options box (which contains the config fields)
            var optionsBox = document.getElementById('config-options-box');
            // Get a list of all input fields
            var inputs = document.getElementsByTagName('input');
            // Get a list of all select fields
            var selects = document.getElementsByTagName('select');

            // For both of these lists, loop through them and replace the values in the existing
            // config dict with the new values
            for (var i = 0; i < inputs.length; i++) {
                config_dict[inputs[i].id]["value"] = inputs[i].value
            }
            for (var i = 0; i < selects.length; i++) {
                config_dict[selects[i].id]["value"] = selects[i].value
            }

            // Send POST request to server containing new config data
            $.ajax({
                type: "POST",
                url: config_submit_route,
                data: JSON.stringify(config_dict),
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function(data){
                    // If everything is successful, make the button shrink and turn green.
                    anime({
                        targets: '#saveConfigButton',
                        backgroundColor: '#8aff70',
                        scale: 0.8,
                        color: '#131313',
                        duration: 1000
                    })
                },
                error: function(jqXHR, exception){
                    console.log("Failure");
                    alert(exception);
                    location.reload();
                    return false;
                }
            });
        }
    });
}

function enterButton(button) {
            // This function defines the animation for when the cursor enters the button
            anime.remove(button);
            anime({
                targets: button,
                scale: 1.1,
                backgroundColor: '#7d0000',
                color: '#FFF',
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
        color: '#131313',
        duration: 500,
        easing: "easeOutExpo"
    });
    // Shrink back title text
    anime({
        targets: ".secondary-font",
        scale: 1,
        duration: 2000,
        easing: "easeOutExpo"
    });
};

function addButtonEvents(){
    var buttons = document.querySelectorAll('.animated-button');  // Select elements with animated button class

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

function main(){
    // When the document is fully loaded, execute the following code:

    $('#config-container').hide();

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
        complete:addButtonEvents
        // Not adding the button event listeners until after the entry animation has completed else it causes bugs
    })

    t1.add({
        targets: '.secondary-font',
        textShadow: '2px 2px rgb(125, 0, 0)',
        easing: "easeInOutExpo",
    })

}

// Don't run any of these animation functions until the document has fully loaded else some elements may be missing
// When I didn't have this none of the animations worked
document.addEventListener("DOMContentLoaded", main);


