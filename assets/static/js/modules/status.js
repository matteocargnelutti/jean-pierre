/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * modules/status.js - Handles the status bar
*/

//-----------------------------------------------------------------------------
// Status Prototype
//-----------------------------------------------------------------------------
jp.Status = function() {
    /**
     * Constructor
    */
    var self = this;
    this.message = "";

    /**
     * Updates message in the status bar and makes it flash
     * @param {string} message_key - The key to fetch from jp.Lang
    */
    this.say = function(message_key) {
        self.message = jp.lang.get(message_key)
        $('footer .status').html(self.message)
        jp.ui.statusbar_flash();
    };

};
