# -*- coding: utf-8 -*-

# © 2017 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

class ProjectLFConfiguration(models.TransientModel):
	_name = 'project.config.settings'
	_inherit = 'project.config.settings'

	lf_heures_jour = fields.Float('Hours / Day', help="Time base for calculating the number of hours sold per project (default 7h)", default=7.0 )

	@api.multi
	def set_default_lf_heures_jour(self):
		return self.env['ir.values'].sudo().set_default(
            'project.config.settings', 'lf_heures_jour', self.lf_heures_jour)

	@api.multi
	def get_default_lf_heures_jour(self, field):
		lf_heures_jour = self.env['ir.values'].get_default('project.config.settings', 'lf_heures_jour')

		return { 'lf_heures_jour': lf_heures_jour if lf_heures_jour else 7.0 }
        