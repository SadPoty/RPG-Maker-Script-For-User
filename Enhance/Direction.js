// {"description":"Let you change you're character direction", "usage":"ctrl + arrow keys", "var":0}
//==============================
// * Put this code in a new file in the js/plugins directory
// * Add the following to the list of plugins in js/plugins.js:
// * {"name":"Direction","status":true,"description":"Add Noclip","parameters":{}}
// *
// * You can find a list of keycodes here: https://www.toptal.com/developers/keycode
// * By default, the keybind are the arrow keys + ctrl. You can change it by modifying the keyCode variable.
//==============================

// direction = [Up: 8, Left: 4, Down: 2, Right: 6 ]

window.addEventListener("keydown", function(event) {
    if (event.ctrlKey) { // If ctrl in down
        Input.clear();
        if (event.key === "ArrowUp") {
            $gamePlayer.setDirection(8);
        } else if (event.key === "ArrowLeft") {
            $gamePlayer.setDirection(4);
        } else if (event.key === "ArrowDown") {
            $gamePlayer.setDirection(2);
        } else if (event.key === "ArrowRight") {
            $gamePlayer.setDirection(6);
     }
    }
})


