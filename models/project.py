# -*- coding: utf-8 -*-

# © 2017 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, date
import time
from odoo import tools
from odoo import models, fields, api, osv

class FilamentProjet(models.Model):
	_inherit = 'project.project'

	use_prospection = fields.Boolean("Include prospecting", default=False)
	lf_total_budget = fields.Float('Project budget',)
	lf_heures_budget = fields.Float('Budget hours', compute='_budget_heures')
	lf_tarif_jour = fields.Float('Day price',)
	lf_taux_horaire = fields.Float('Hourly rate', compute='_taux_horaire')
	lf_heures_prospection = fields.Float('Prospecting (h)', compute='_total_heures_prospection')
	lf_heures_projet = fields.Float('Allocated (h)', compute='_total_heures')
	lf_heures_passees = fields.Float('Hours spent', compute='_total_heures_passees')
	lf_heures_restantes = fields.Float('Remaining (h)', compute='_total_heures_restantes')
	lf_heures_planifiees = fields.Float('Planned (h)', compute='_total_heures_planifiees')
	lf_couts_annexes =  fields.Float('Additional costs', compute='_couts_annexes')
	lf_couts_estimes =  fields.Float('Estimated costs')
	lf_commentaire = fields.Text('Comments')

	####################################################
	###                Fields Function               ###
	####################################################

	@api.one
	def _taux_horaire(self):
		lf_heures_jour = self.env['ir.values'].get_default('project.config.settings', 'lf_heures_jour')
		self.lf_taux_horaire = self.lf_tarif_jour / lf_heures_jour

	@api.one
	def _total_heures_prospection(self):
		project = self.id		
		self.lf_heures_prospection = 0.0
		## Calcul heures   
		if self.use_prospection:
			self.env.cr.execute("select sum(aal.unit_amount) from account_analytic_line aal, project_task pt where aal.project_id=%s and pt.name like %s and pt.id=aal.task_id;", (project, "Prospection%",) )
			heures_prospection = self.env.cr.fetchone()[0]
			if heures_prospection:
				self.lf_heures_prospection = heures_prospection

	@api.one
	def _total_heures_passees(self):
		project = self.id
		self.lf_heures_passees = 0.0		
		## Calcul heures   
		self.env.cr.execute("select sum(unit_amount) from account_analytic_line where project_id=%s;", (project, ) )
		heures_passees = self.env.cr.fetchone()[0]
		if heures_passees:
			self.lf_heures_passees = heures_passees
			if self.use_prospection:
				self.lf_heures_passees -= self.lf_heures_prospection

	@api.one
	def _total_heures_planifiees(self):
		res = 0.0
		for record in self.task_ids:
			res = res + record.planned_hours
		self.lf_heures_planifiees = res

	@api.one
	def _couts_annexes(self):
		account = self.analytic_account_id.id		
		##############    Calcul couts annexes   ################
		self.env.cr.execute("select -sum(amount) from account_analytic_line where account_id=%s and project_id is null and ref is not null;", (account, ) )
		couts_annexes = self.env.cr.fetchone()[0]
		if couts_annexes:
			self.lf_couts_annexes = couts_annexes
		else:
			self.lf_couts_annexes = 0.0

	@api.one
	@api.depends('lf_total_budget','lf_couts_annexes')
	def _budget_heures(self):
		self.lf_heures_budget = self.lf_total_budget - self.lf_couts_estimes

	@api.one
	def _total_heures(self):
		lf_heures_jour = self.env['ir.values'].get_default('project.config.settings', 'lf_heures_jour')
		if (self.lf_tarif_jour != 0.0):
			self.lf_heures_projet = (self.lf_heures_budget / self.lf_tarif_jour) * lf_heures_jour
		else:
			self.lf_heures_projet = 0.0

	@api.one
	def _total_heures_restantes(self):
		self.lf_heures_restantes = self.lf_heures_projet - self.lf_heures_passees

	
	####################################################
	###                  Actions                     ###
	####################################################

	def open_project(self):
	    return {
	        'type': 'ir.actions.act_window',
	        'name': 'Projet' + self.name,
	        'view_mode': 'kanban',
	        'res_model': 'project.project',
	        'res_id': self.id, 
	        'views': [(False, 'kanban')],
	    }
