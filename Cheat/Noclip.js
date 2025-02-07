// {"description":"Let you walk through walls", "usage":"N to toggle on/off", "var":1}
//==============================
// * Put this code in a new file in the js/plugins directory
// * Add the following to the list of plugins in js/plugins.js:
// * {"name":"Noclip","status":true,"description":"Add Noclip","parameters":{}}
// *
// * You can find a list of keycodes here: https://www.toptal.com/developers/keycode
// * By default, the keybind is set to N. You can change it by modifying the keyCode variable.
//==============================


Game_CharacterBase.prototype._noclip = false; // Add noclip variable
let keyCode = 78; // Change keybind here

const _yes_pass = Game_CharacterBase.prototype.canPass; // Save Original function
Game_CharacterBase.prototype.canPass = function(x, y, d) { // Function to override the original
	if (this._noclip) {
		return true;
	} else {
		return _yes_pass.call(this, x, y, d); // Call original function
	}
}

window.addEventListener("keydown", function(event) {  // Check if any key is pressed
    if (event.keyCode === keyCode) {
        if ($gamePlayer._noclip) {
            $gameMessage.add('NoClip OFF'); // Comment / delete this to remove message
            $gamePlayer._noclip = false;
        } else {
            $gameMessage.add('NoClip ON'); // Comment / delete this to remove message
            $gamePlayer._noclip = true;
        }
    }
});