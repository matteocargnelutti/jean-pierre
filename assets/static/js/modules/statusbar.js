/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * modules/statusbar.js - Handles the status bar
*/

//-----------------------------------------------------------------------------
// StatusBar Prototype
//-----------------------------------------------------------------------------
jeanpierre.StatusBar = function() {
    /**
     * Constructor
    */
    this.message = ""

    /**
     * Updates message and flashes
     * @param {string} message
    */
    this.message = function(message) {
        this.message = message
        console.log(message)
    };

};
