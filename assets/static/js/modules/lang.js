/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * modules/lang.js - Handles language-related content
*/

//-----------------------------------------------------------------------------
// Lang Prototype
//-----------------------------------------------------------------------------
jeanpierre.Lang = function() {
    /**
     * Constructor
    */
    this.data = {}

    /**
     * Fetches messages in the language set in the Params config table
    */
    this.message = function() {
        console.log("Ok")
    };

    /**
     * Returns a message by its key
     * @param {string} key
     * @return {string}
    */
    this.get = function(key) {
        return this.data[key]
    }

};
