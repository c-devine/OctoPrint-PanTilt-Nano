/*
 * View model for OctoPrint-Pantilt_nano
 *
 * Author: You
 * License: AGPLv3
 */
$(function() {
    function Pantilt_nanoViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        // self.loginStateViewModel = parameters[0];
        // self.settingsViewModel = parameters[1];

        // TODO: Implement your plugin's view model here.
    }

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        Pantilt_nanoViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        [ /* "loginStateViewModel", "settingsViewModel" */ ],

        // e.g. #settings_plugin_pantilt_nano, #tab_plugin_pantilt_nano, ...
        [ /* ... */ ]
    ]);
});
