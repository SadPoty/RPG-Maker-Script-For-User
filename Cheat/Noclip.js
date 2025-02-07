// {"description":"Let you walk through walls", "usage":"N to toggle on/off", "var":["n"]}
let keybind = "n"; // Change keybind here
// The commented line above is for the auto installer ignore it
//==============================
// * Put this code in a new file in the js/plugins directory
// * Add the following to the list of plugins in js/plugins.js:
// * {"name":"Noclip","status":true,"description":"Add Noclip","parameters":{}}
// *
// * By default, the keybind is set to N. You can change it by modifying the key variable.
//==============================


Game_CharacterBase.prototype._noclip = false; // Add noclip variable

const _yes_pass = Game_CharacterBase.prototype.canPass; // Save Original function
Game_CharacterBase.prototype.canPass = function(x, y, d) { // Function to override the original
	if (this._noclip) {
		return true;
	} else {
		return _yes_pass.call(this, x, y, d); // Call original function
	}
}

window.addEventListener("keydown", function(event) {  // Check if any key is pressed
    if (event.key === keybind) {
        if ($gamePlayer._noclip) {
            $gameMessage.add('NoClip OFF'); // Comment / delete this to remove message
            $gamePlayer._noclip = false;
        } else {
            $gameMessage.add('NoClip ON'); // Comment / delete this to remove message
            $gamePlayer._noclip = true;
        }
    }
});