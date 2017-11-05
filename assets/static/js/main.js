/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * main.js - Entry point
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
// Once the language info are loaded ...
jp.lang.fetch_list( function(){

    // If on login page and there is an error
    if( $('body.login').length > 0 && $('form.error').length > 0 ) {
        jp.status.say('web_login_error');
    }

    // If on groceries page
    if( $('body.groceries').length > 0 ) {
        // Fetch and show list, bind events
        jp.groceries.fetch_list( function(){
            jp.groceries.show_list();
            jp.groceries.bind_events(); 
        });
    }

    // If on products page 
    if( $('body.products').length > 0 ) {

    }

});

});
