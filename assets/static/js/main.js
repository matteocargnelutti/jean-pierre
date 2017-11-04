/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * main.js - Main event catcher / handler
*/
window.jp = {}

jQuery(document).ready( function() {
//-----------------------------------------------------------------------------
// Globally accessible objects
//-----------------------------------------------------------------------------
jp.lang = new jp.Lang(); // Use jp.lang.get('key') for localized messages
jp.status = new jp.Status(); // Status bar. use jp.status.say('key')
jp.groceries = new jp.Groceries(); // Groceries page handling

//-----------------------------------------------------------------------------
// Init
//-----------------------------------------------------------------------------
jp.lang.fetch_list( function(){

    // If on groceries page : fetch and show list
    if( jQuery('body.groceries').length > 0 ) {
        jp.groceries.fetch_list( function(){
            jp.groceries.show_list();
        });
    }

    // If on products page : show list
    if( jQuery('body.products').length > 0 ) {

    }

});

//-----------------------------------------------------------------------------
// Event binding
//-----------------------------------------------------------------------------
});
