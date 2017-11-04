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
    var self = this;
    this.list = {} // Grocery list data

    /**
     * Injects the list as HTML content
     * @param {string} selector - Where should the list be injected ?
     * @param {function} callback
    */
    this.show_list = function(selector, callback) {
        
        // Prepare list's html
        html = '';
        
        for( entry in self.list ) {
            pic = '/static/img/default.png'
            if( entry.pic == 1) {
                pic = '/static/img/'+barcode+'.jpg'
            }

            html += '<div class="item" id="grocery-'+entry.barcode+'">';
                html += '<img src="'+pic+'" alt="Product\'s pic"/>';
                html += '<h3>';
                    html += '<span>'+entry.name+'</span>';
                    html += '<span class="quantity">x'+entry.quantity+'</span>';
                html += '</h3>';
                html += '<div>';
                    html += '<a href="#grocery-'+barcode+'" class="plus">+1</a>';
                    html += '<a href="#grocery-'+barcode+'" class="minus">-1</a>';
                    html += '<a href="#grocery-'+barcode+'" class="plus">Edit</a>';
                html += '</div>';
            html += '</div>';
        }

        // Inject
        jQuery(''+selector).html(html);

        // Return
        callback();
    };

    /**
     * Fetches grocery list from the server
     * @param {function} callback
    */
    this.fetch_list = function(callback) {
        $.ajax({
            url: "/api/groceries_list",
            type: 'GET',
            dataType: 'json',
            success: function(response){
                self.list = response['items'];
                callback();
            },
            error: function(){
                jp.status.say('web_groceries_list_error')
            }

        });
    };

    /**
     * Edits / adds / delete an item in the grocery list
     * Quantity 0 = Delete
     * @param {string} barcode
     * @param {int} quantity
    */
    this.edit_item = function(barcode, quantity) {
        // Status bar : loading
        jp.status.say('web_groceries_list_process');
        
        // Query
        $.ajax({
            url: "/api/groceries_list_edit/"+barcode+"/"+quantity,
            type: 'GET',
            dataType: 'json',
            success: function(response){
                // Refresh and display new list + display status
                this.fetch_list(function(){
                    this.show_list(function() {
                        jp.status.say('web_groceries_list_edit_ok');
                    })
                });
            },
            error: function(){
                jp.status.say('web_groceries_edit_error')
            }

        });
    }

};
