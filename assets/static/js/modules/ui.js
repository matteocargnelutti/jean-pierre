/**
 * Jean-Pierre [Prototype]
 * A Raspberry Pi robot that helps people make their grocery list.
 * Matteo Cargnelutti - github.com/matteocargnelutti
 *
 * modules/ui.js - UI methods
*/

//-----------------------------------------------------------------------------
// UI Prototype
//-----------------------------------------------------------------------------
jp.Ui = function() {
    /**
     * Constructor
    */
    var self = this;
    this.statusbar_lastflash = -1; // Stores interval between two status bar flashes. -1 = no recent flash.

    /**
     * Shows / hide the nav sidebar
    */
    this.navbar = function() {
        console.log('open/close navbar')
    };

    /**
     * Makes the status bar flash
    */
    this.statusbar_flash = function() {
        $('footer .status').addClass('flash');
        self.statusbar_lastflash = 0; // Activates the clean-up loop
    }

    /**
     * Status bar state clean-up loop
    */
    this.statusbar_cleanup = function() {

        // If no flash has been initiated
        if( self.statusbar_lastflash < 0 ) {
            return;
        }
        // If there is a recent flash
        else {
            self.statusbar_lastflash += 500; // Increment its counter
            // If it has been more than 3 second since the last flash
            if( self.statusbar_lastflash >= 3000 ) {
                // End flash and clean-up loop
                self.statusbar_lastflash = -1;
                $('footer .status').removeClass('flash');
            }
        }        
    }

    // Status bar "flash" status clean-up loop
    setInterval( function() { 
        self.statusbar_cleanup() 
    }, 500);

};
