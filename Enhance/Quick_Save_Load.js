// {"description":"Let you quickly save and load", "usage":"F1 to save, F3 to load", "var":["F1", "F3"]}
let keybind = ["F1", "F3"]; // Change keybind here
// The commented line above is for the auto installer ignore it
//==============================
// * Put this code in a new file in the js/plugins directory
// * Add the following to the list of plugins in js/plugins.js:
// * {"name":"Quick_Save_Load","status":true,"description":"Add Quick Save/Load","parameters":{}}
// *
// * By default, the keybind is set to F1 and F3. You can change it by modifying the keyCode variable.
//==============================

let save_file_slot = 4; // Change this to select the slot to save

window.addEventListener("keydown", function(event) {  // Check if any key is pressed
    if (event.key === "F1") {              
        $gameSystem.onBeforeSave();
        if (DataManager.saveGame(save_file_slot)) {
            StorageManager.cleanBackup(save_file_slot);
        }
    }
    if (event.key === "F3") {
        if (DataManager.loadGame(save_file_slot)) {
            $gamePlayer.reserveTransfer($gameMap.mapId(), $gamePlayer.x, $gamePlayer.y);
            $gamePlayer.requestMapReload();
            SceneManager.goto(Scene_Map);
        }
    }
});

