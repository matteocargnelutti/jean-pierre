/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * main.js - Main event catcher / handler
*/
/** Global handler  */
window.jp = {}

jQuery(document).ready( function() {
//-----------------------------------------------------------------------------
// Inits LANG content
//-----------------------------------------------------------------------------
/**
 * Globally accessible objects :
 * - jp.lang = Use jp.lang.get('key') to get a message by its key
 * - jp.status = Use jp.status.say('key') to show a message by its key
*/
jp.lang = new jp.Lang()
jp.status = new jp.Status()
});
