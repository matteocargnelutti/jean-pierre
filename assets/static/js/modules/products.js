/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * modules/products.js - Products page handler
*/

//-----------------------------------------------------------------------------
// Products Prototype
//-----------------------------------------------------------------------------
jp.Products = function() {
    /**
     * Constructor
    */
    var self = this;
    this.list = {}; // Products list data

    /**
     * Injects the list as HTML content
     * @param {bool} refresh - Should the list be fetched ?
     * @param {string} selector - Where should the list be injected ?
    */
    this.show_list = function(refresh, selector) {
        if( refresh == true ) {
            this.refresh_list();
        }
        console.log(this.list);
    };

    /**
     * Fetches products list from the server
    */
    this.refresh_list = function() {
        console.log("Refresh");
    };

    /**
     * Adds / edit an item in the products list
     * @param {string} barcode
     * @param {string} name
    */
    this.edit_item = function(barcode, name) {
        console.log("Edit : "+ barcode + ' - '+ name);
    }

    /**
     * Deletes an item in the products list
     * @param {string} barcode
    */
    this.delete_item = function(barcode) {
        console.log("Edit : "+ barcode + ' - '+ name);
    }

};
