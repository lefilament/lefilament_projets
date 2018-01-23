
// # © 2017 Le Filament (<http://www.le-filament.com>)
// # License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

odoo.define('lefilament_projets.progress_bar', function (require) {
    "use strict";

    var core = require('web.core');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var ProgressBar = require('web.ProgressBar');

    ProgressBar.include({
        _render_value: function(v) {
            var value = this.value;
            var max_value = this.max_value;
            if(!isNaN(v)) {
                if(this.edit_max_value) {
                    max_value = v;
                } else {
                    value = v;
                }
            }
            value = value || 0;
            max_value = max_value || 0;

            var widthComplete;
            if(value <= max_value) {
                widthComplete = value/max_value * 100;
            } else {
                widthComplete = max_value/value * 100;
            }

            this.$('.o_progress').toggleClass('o_progress_overflow', value > max_value);
            this.$('.o_progressbar_complete').css('width', widthComplete + '%');

            if(this.readonly) {
                if(max_value !== 100) {
                    this.$('.o_progressbar_value').html(utils.human_number(value) + " / " + utils.human_number(max_value));
                } else {
                    this.$('.o_progressbar_value').html(utils.human_number(value) + "%");
                }
            } else if(isNaN(v)) {
                this.$('.o_progressbar_value').val(this.edit_max_value ? max_value : value);
            }
        }
    });

});