# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    ThinkOpen Solutions Brasil
#    Copyright (C) Thinkopen Solutions <http://www.tkobr.com>.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields, _


class task_type(models.Model):
    _name = 'task.type'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer('Color Index', size=1)
    task_id = fields.Many2one('project.task', string='Task')


class project_task(models.Model):
    _inherit = 'project.task'

    type_name = fields.Char(
        compute='_get_type_name',
        store=True,
        string='Name')
    task_type_id = fields.Many2one('task.type', string='Type')
    color = fields.Integer(compute='_get_color', string='Color', store=False)
    appro_marche=fields.Binary(string='Approation de marché')
    num_marche=fields.Char(string='N° de marché')
    dep=fields.Char(string='Département')
    reg=fields.Char(string='Région')
    nomination=fields.Char(string='Nomination')
    odre_serv_up=fields.Binary(string='Documents à attacher')
    trav_dir=fields.Many2one('project.hr',string='Directeur des travaux')
    cond_trav=fields.Many2one('project.hr',string='Conducteur des travaux')
    resp_geo=fields.Many2one('project.hr',string='Responsable Géotechnique')
    resp_topo=fields.Many2one('project.hr',string='Responsable Topographie')
    comp_chantier=fields.Many2one('rpoject.hr',string='Comptable de chantier')

    @api.multi
    def name_get(self):
        result = []
        for task in self:
            task_type = task.task_type_id and task.task_type_id.name or ''
            result.append(
                (task.id, "%s %s" %
                 ('[' + str(task_type) + ']', task.name or ' ')))
        return result

    @api.depends('task_type_id.name')
    def _get_type_name(self):
        for record in self:
            if record.task_type_id:
                record.type_name = record.task_type_id.name

    @api.depends('task_type_id.color')
    def _get_color(self):
        for record in self:

            if record.task_type_id:
                record.color = record.task_type_id.color

    @api.onchange('task_type_id')
    def _change_task_type(self):
        if self.task_type_id:
            self.color = str(self.task_type_id.color)[-1]
            self.type_name = self.task_type_id.name
class project_hr_point_jour(models.Model):
    _name='project.hr.point.jour'

    name=fields.Char(string='Référence')
    chantier_id=fields.Many2one('project.project',string='Chantier')
    code_chantier=fields.Char(string='Code',related='chantier_id.code')
    gazoil=fields.Float(string='Gazoil')
    huile_moteur=fields.Float(string='Moteur')
    huile_verrin=fields.Float(string='Verrin')
    stock_title=fields.Char(string='stock')
    pos_potence=fields.Integer(string='Position Potence:Pk')
    car_potence=fields.Integer(string='Carrière Potence:Pk')
    ope_potence=fields.Integer(string='Opération en Cours:Pk')
    obs=fields.Text(string='Observation')
    bareme_gazoil=fields.Integer(string='Barème Gazoil')
    trav_exe=fields.Text(string='TRAVAUX EXECUTES')
    lepointeur=fields.Binary(string='Le pointeur')
    
class project_hr_point_perso(models.Model):
    _name='project.hr.point.perso'


    name=fields.Char(string='Personne')
    perso_id=fields.Many2one('project.hr',string='Personnel')
    matricule=fields.Char(string='Matricule')
    presence=fields.Integer(string='Présence')
    trav_effect=fields.Char(string='Travaux Effectués')
    nbr_hr=fields.Integer(string='N° Heure')
    design_matos=fields.Many2one('project.fleet.camion',string='Désignation Matériel')
    dot_gazoil=fields.Float(string='Dotation Gazoil L')
    dot_huile=fields.Float(string='Dotation Huile L')
    profil_1=fields.Integer(string="1")
    profil_2=fields.Integer(string="2")
    voy_requis_1=fields.Integer(string="1")
    voy_requis_2=fields.Integer(string="2")
    rest_litr=fields.Float(string='Rest. Litres')
    

class project_hr_(models.Model):
    _name='project.hr'

    name=fields.Char(string='Personne')
    nom=fields.Char(string='Nom')
    prenom=fields.Char(string='Prénom')
    matricule=fields.Char(string='Matricule')
    num_ci=fields.Float(string='Numéro d\' identité')
    tel=fields.Float(string='Télephone')
    profession=fields.Char('Profession')
class project_fleet_camion(models.Model):
    _name='project.fleet.camion'

    name=fields.Char(string='Camion')
    matricule=fields.Char(string='Matricule')
    categorie=fields.Many2one('project.fleet.cat',string='Catégorie')
class project_fleet_engine(models.Model):
    _name='project.fleet.engine'

    name=fields.Char(string='Engin')
    fleet_id=fields.Many2one('project.fleet',string='Désignation Véhicule')
    matricule=fields.Char(string='Matricule')
    categorie=fields.Char(string='Catégorie',related='fleet_id.categorie_id.name')
class project_fleet_cat(models.Model):
    _name='project.fleet.cat'

    name=fields.Char(string='Catégorie')
    model_id=fields.Many2one('project.fleet.model',string='Model')
class project_fleet_type(models.Model):
    _name='project.fleet.type'

    name=fields.Char(string='Type')
class project_fleet_cat(models.Model):
    _name='project.fleet.model'

    name=fields.Char(string='Model')
    type_id=fields.Many2one('project.fleet.type',string='Model')
class project_fleet(models.Model):
    _name='project.fleet'

    name=fields.Char(string='Véhicule')
    type_id=fields.Many2one('project.fleet.type',string='Type')
    cat_id=fields.Many2one('project.fleet.cat',string='Catégorie')
    model_id=fields.Many2one('project.fleet.model',string='Model')
    matricule=fields.Char(string='Matricule')
    
class project_hr_point_hebdo(models.Model):
      _name='project.hr.point.hebdo'

      name=fields.Char(string='Référence')
      mois=fields.Date(string='Mois')
      date_beg=fields.Date(string='Semaine du')
      date_fin=fields.Date(string='Au')
      miss_ctrl=fields.Binary(string='La mission de contrôle')
      user_connected=fields.Many2one('res.users',string='Utilisateur Connecté')
class project_hr_point_hebdo_timesheet(models.Model):
      _name='project.hr.point.hebdo.timesheet'

      name=fields.Char(string='Timesheet')
      personne_id=fields.Many2one('project.hr',string='Prénom et Nom')
      matricule=fields.Char(string='Matricule')
      emp_cat=fields.Char(string='Emploi-Catégorie')
      lundi=fields.Integer(string='Lundi')
      mardi=fields.Integer(string='Mardi')
      mercredi=fields.Integer(string='Mercredi')
      jeudi=fields.Integer(string='Jeudi')
      vendredi=fields.Integer(string='Vendredi')
      samedi=fields.Integer(string='Samedi')
      dimanche=fields.Integer(string='Dimanche')
      total_hrpoint=fields.Integer(string='HP')
      total_hrsup=fields.Integer(string='HS')
class project_task_cmd_matos(models.Model):
     _name='project.task.cmd.matos'
     
     name=fields.Char(string='Matériaux')
     quantite=fields.Integer(string='Quantité')
     unite=fields.Char(string='Unité')
     date_mise=fields.Date(string='Date Mise en Place')
     obs=fields.Text(string='Observation')
     user_connected=fields.Many2one('res.users',string='Utilisateur Connecté')
class project_task_topo(models.Model):
      _name='project.task.topo'

      name=fields.Char(string='Tableau Topographie')
      nb_prof=fields.Char(string='NB Numéro de profil')
      lect_arr=fields.Float(string='(LAR) Lecture Arrière')
      lect_av=fields.Float(string='(LAV) Lecture Avant')
      cote_terr=fields.Float(string='(COTE) Cote sur terrain')
      cote_proj=fields.Float(string='Cote Projet')
      diff_pos=fields.Float(string='+')
      diff_nega=fields.Float(string='-')
      obs=fields.Text(string='Observation')


class project_hr_fiche_jour(models.Model):
      _name='project.hr.fiche.jour'


      name=fields.Char(string='Réference')
      personne_id=fields.Many2one('project.hr',string='Prénom et Nom')
      matricule=fields.Char(string='N°',related='personne_id.matricule')
      date=fields.Date(string='Date')
      gazoil=fields.Char(string='Gazoil')
      huile=fields.Char(string='Huile')
      nbr_jour=fields.Integer(string='Nombre de J')
      hr_dep=fields.Integer(string='H. Départ')
      hr_darr=fields.Integer(string='H. d\'arriv')
      hr_fonct=fields.Integer(string='H. Fonct')
      hr_supp=fields.Integer(string='H. Suppl')
      decharge=fields.Char(string='Décharge')
      obs=fields.Text(string='Observation')
      chefchantier=fields.Binary(string='Chef de chantier')
      chauffeur=fields.Binary(string='Le Chauffeur')
      pointeur=fields.Binary(string='Le Pointeur')
      specialist=fields.Binary(string='Le Spécialiste')
      maneuvre=fields.Binary(string='Le Manoeuvre')
      user_connected=fields.Many2one('res.users',string='Utilisateur Connecté')
      my_fiche_id=fields.Many2one('project.hr.fiche.jour',string='Fiche Journalière')
      my_fiche_ids=fields.One2many('project.hr.fiche.jour','my_fiche_id',string='Fiche Journalière')
      
      
     

      
    
    
    
    
    
    












    
    
    
