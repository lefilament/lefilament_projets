{
	'name': 'Le Filament - Projets',

	'summary': """
        Projets Le Filament""",

	'version': '10.0.1.0',
	'license': 'AGPL-3',
	'description': """
	
	Module Projet Le Filament

	This module depends upon *hr_timesheet* and *hr_expense* modules.

	This module provides:
 	- the calculation of imputed hours and costs on the project
 	- the project estimate (based on a variable of the number of hours per day)
 	- a progressbar spent / budget
	- prospecting hours (new field to set up at the project level and based on the number of hours charged to a task named Prospection)

	""",
	
	'author': 'LE FILAMENT',
	'category': 'Project',
	'depends': ['hr_timesheet','hr_expense'],
	'contributors': [
                'Benjamin Rivier <benjamin-filament>',
		'Rémi Cazenave <remi-filament>',
		'Juliana Poudou <JulianaPoudou>',
    ],
	'website': 'https://le-filament.com',
	'data': [
		'views/assets.xml',
		'views/lefilament_projets_view.xml',
	],
	'qweb': [
    ],
}
