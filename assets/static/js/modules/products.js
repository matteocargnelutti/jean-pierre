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
    this.list = {} // Products list data

    /**
     * Injects the list as HTML content
     * @param {function} callback
    */
    this.show_list = function() {
        
        // Prepare list's html
        html = '';

        if( $.isEmptyObject(self.list) ) {
            html += '<div class="item empty">';
                html += '<h3>'+jp.lang.get('web_products_list_empty')+'</h3>';
            html += '</div>';
        }
        
        for( var barcode in self.list ) {
            var name = self.list[barcode].name
            var pic = '/static/img/default.png';
            if( self.list[barcode].pic == 1) {
                pic = '/static/img/'+barcode+'.jpg';
            }

            html += '<div class="item" id="item-'+barcode+'">';
                html += '<img src="'+pic+'" alt="Product\'s pic"/>';
                html += '<form>';
                    html += '<input type="text" value="'+barcode+'" name="barcode" placeholder="'+jp.lang.get('ean13')+'" maxlength="13" disabled/>';
                    html += '<input type="text" value="'+name+'" name="name" placeholder="'+jp.lang.get('product_name')+'" maxlength="32" required/>';
                    html += '<button>Ok</button>';
                    html += '<a href="#" class="delete">'+jp.lang.get('delete')+'</a>';
                html += '</form>';
            html += '</div>';
        }

        // Inject
        $('.items').html(html);
    };

    /**
     * Fetches the products list from the server
     * @param {function} callback
    */
    this.fetch_list = function(callback) {
        $.ajax({
            url: "/api/products_list",
            type: 'GET',
            dataType: 'json',
            success: function(response){
                self.list = response['items'];
                callback();
            },
            error: function(){
                jp.status.say('web_products_list_error')
            }

        });
    };

    /**
     * Edits / adds an item in the products list
     *
     * @param {string} barcode
     * @param {string} name
    */
    this.edit_item = function(barcode, name) {
        // Status bar : loading
        jp.status.say('processing');
        
        // Query
        $.ajax({
            url: "/api/products_edit/"+barcode+"/"+encodeURIComponent(name),
            type: 'GET',
            dataType: 'json',
            success: function(response){
                // Refresh and display new list + display status
                self.fetch_list(function(){
                    self.show_list();
                    jp.status.say('web_products_edit_ok');
                });
            },
            error: function(){
                jp.status.say('web_products_edit_error')
            }

        });
    }

    /**
     * Delete an item in the products list
     *
     * @param {string} barcode
    */
    this.delete_item = function(barcode) {
        // Status bar : loading
        jp.status.say('processing');
        
        // Query
        $.ajax({
            url: "/api/products_delete/"+barcode,
            type: 'GET',
            dataType: 'json',
            success: function(response){
                // Refresh and display new list + display status
                self.fetch_list(function(){
                    self.show_list();
                    jp.status.say('web_products_delete_ok');
                });
            },
            error: function(){
                jp.status.say('web_products_delete_error')
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
        $('body.products .menu form').on('submit', function(e){
            e.preventDefault();
            
            var form = $(this).parent(form);
            var barcode = $('input[name="barcode"]', form).val();
            var name = $('input[name="name"]', form).val();
            
            self.edit_item(barcode, name);

            // Clean form
            $('body.products .menu input[name="barcode"]').val('');
            $('body.products .menu input[name="name"]').val('');
        });

        //
        // Edit an item
        //
        $('body.products .items').delegate('.item form', 'submit', function(e){
            e.preventDefault();

            var form = $(this).parent(form);
            var barcode = $('input[name="barcode"]', form).val();
            var name = $('input[name="name"]', form).val();

            self.edit_item(barcode, name);
        });

        //
        // Delete an item
        //
        $('body.products .items').delegate('.item .delete', 'click', function(e){
            e.preventDefault();

            var form = $(this).parent(form);
            var barcode = $('input[name="barcode"]', form).val();
            
            if( confirm(jp.lang.get('web_products_delete_prompt')) ) {
                self.delete_item(barcode);
            }
        });
    }

};
