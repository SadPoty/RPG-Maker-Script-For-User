// {"description":"Force open the save or load screen", "usage":"I to open save screen, O to open load screen", "var":["i", "o"]}
let keybind = ["i", "o"]; // Change keybind here
// The commented line above is for the auto installer ignore it
//==============================
// * Put this code in a new file in the js/plugins directory
// * Add the following to the list of plugins in js/plugins.js:
// * {"name":"Force_save_load_screen","status":true,"description":"Add a keybind to force open the save or load screen","parameters":{}}
// *
// * You can find a list of keycodes here: https://www.toptal.com/developers/keycode
// * By default, the keybind is set to I and O. You can change it by modifying the event.key === "i" and event.key === "o" variables.
//==============================


window.addEventListener("keydown", function(event) {  // Check if any key is pressed
    if (event.key === keybind[0]) {
        SceneManager.push(Scene_Save);
    }
    if (event.key === keybind[1]) {
        SceneManager.push(Scene_Load);
    }
});
