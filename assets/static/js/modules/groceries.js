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
     * @param {function} callback
    */
    this.show_list = function() {
        
        // Prepare list's html
        html = '';

        if( $.isEmptyObject(self.list) ) {
            html += '<div class="item empty">';
                html += '<h3>'+jp.lang.get('web_groceries_list_empty')+'</h3>';
            html += '</div>';
        }
        
        for( var barcode in self.list ) {
            var name = self.list[barcode].name
            var quantity = self.list[barcode].quantity
            var pic = '/static/img/default.png';
            if( self.list[barcode].pic == 1) {
                pic = '/static/img/'+barcode+'.jpg';
            }

            html += '<div class="item" id="item-'+barcode+'">';
                html += '<img src="'+pic+'" alt="Product\'s pic"/>';
                html += '<h3>';
                    if( name === '???' ) {
                        html += '<span>'+name+' ('+barcode+')</span> ';
                    }
                    else {
                        html += '<span>'+name+'</span> ';
                    }
                    html += '<span class="quantity">x'+quantity+'</span>';
                html += '</h3>';
                html += '<div>';
                    html += '<a href="#item-'+barcode+'" class="plus">+1</a>';
                    html += '<a href="#item-'+barcode+'" class="minus">-1</a>';
                    html += '<a href="/products#item-'+barcode+'" class="plus">Edit</a>';
                html += '</div>';
            html += '</div>';
        }

        // Inject
        $('.items').html(html);
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
            url: "/api/groceries_edit/"+barcode+"/"+quantity,
            type: 'GET',
            dataType: 'json',
            success: function(response){
                // Refresh and display new list + display status
                self.fetch_list(function(){
                    self.show_list();
                    jp.status.say('web_groceries_list_edit_ok');
                });
            },
            error: function(){
                jp.status.say('web_groceries_edit_error')
            }

        });
    }

    /**
     * Events binding
    */
    this.bind_events = function() {
        //
        // Add an item
        //
        $('body.groceries .menu .add a').on('click', function(e){
            e.preventDefault();
            barcode = $('.menu .add select').val();
            quantity = 1

            // If the product's already on the list, we increase its quantity
            if( self.list[barcode] ) {
                quantity = self.list[barcode].quantity + 1
            }
            jp.groceries.edit_item(barcode, quantity);
        });

        //
        // Edit an item
        //
        $('body.groceries').delegate('.item a.plus, .item a.minus', 'click', function(e){
            e.preventDefault();

            barcode = $(this).parent('div').parent('div').attr('id').replace('item-', '');

            if( $(this).hasClass('plus')) {
                quantity = jp.groceries.list[barcode].quantity + 1;
            }
            else {
                quantity = jp.groceries.list[barcode].quantity - 1;
            }

            jp.groceries.edit_item(barcode, quantity);
        });
    }

};
