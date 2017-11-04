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
jp.Lang = function() {
    /**
     * Constructor
    */
    var self = this;
    this.data = {};

    /**
     * Fetches messages in the language set in the Params config table
    */
    this.fetch = function() {
        $.ajax({
            url: "/lang",
            type: 'GET',
            dataType: 'json',
            success: function(response){
                self.data = response;
            }
        })
    };

    /**
     * Returns a message by its key
     * @param {string} key
     * @return {string}
    */
    this.get = function(key) {
        if( self.data[key] ) {
            return this.data[key];
        }
        else {
            return key;
        }
    }

    /**
     * Automaticaly fetches lang data on init
    */
    this.fetch();
};
