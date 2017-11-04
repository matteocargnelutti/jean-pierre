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
     * Fetches lang content in the language the user has defined
    */
    this.fetch_list = function() {
        $.ajax({
            url: "/api/lang",
            type: 'GET',
            dataType: 'json',
            success: function(response){
                self.data = response;
            }
        });
    };

    /**
     * Returns a message by its key
     * @param {string} key
     * @return {string}
    */
    this.get = function(key) {
        if( self.data[key] ) {
            return self.data[key];
        }
        else {
            return key;
        }
    }

    /**
     * Automaticaly fetches lang data on init
    */
    this.fetch_list();
};
