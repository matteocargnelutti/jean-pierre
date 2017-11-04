/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * modules/groceries.js - Groceries page handler
*/

//-----------------------------------------------------------------------------
// Groceries Prototype
//-----------------------------------------------------------------------------
jp.Groceries = function() {
    /**
     * Constructor
    */
    this.list = {} // Grocery list data

    /**
     * Injects the list as HTML content
     * @param {bool} refresh - Should the list be fetched ?
     * @param {string} selector - Where should the list be injected ?
    */
    this.show_list = function(refresh) {
        if( refresh == true ) {
            this.refresh_list();
        }
        console.log(this.list);
    };

    /**
     * Fetches grocery list from the server
    */
    this.refresh_list = function() {
        $.ajax({
            url: "/groceries_list",
            type: 'GET',
            dataType: 'json',
            success: function(response){
                self.list = response;
            },
            error: function(){
                jp.status.say('web_groceries_list_error')
            }

        })
    };

    /**
     * Edits / adds / delete an item in the grocery list
     * Quantity 0 = Delete
     * @param {string} barcode
     * @param {int} quantity
    */
    this.edit_item = function(barcode, quantity) {
        console.log("Edit : "+ barcode + ' - '+ quantity);
    }

};
