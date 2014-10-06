# -*- encoding: utf-8 -*-
##############################################################################
#
#    Darmawan Fatriananda
#    BKD Pemprov Jabar
#    Copyright (c) 2014 <http://www.asdarfat.wordpress.com.com>
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
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp.osv import fields, osv
from datetime import datetime,timedelta
import time
from mx import DateTime

# ====================== res partner ================================= #

class res_partner(osv.Model):
    _inherit = 'res.partner'
    _description ='Data Kepegawaian'
    
    def _get_is_kepala_opd(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context=context):
            if not employee.company_id :
                res[employee.id]=False
            else :
                company_obj = employee.company_id ;
                if not company_obj.head_of_comp_employee_id :
                    res[employee.id]=False
                elif company_obj.head_of_comp_employee_id.id == employee.id  :
                    res[employee.id]=True
                else :
                    res[employee.id]=False
                    
                
           
        return res
  
    def onchange_atasan_banding_nip(self, cr, uid, ids, user_id, context=None):
        res = {'value': {'user_id_banding_nip': False}}
        if user_id:
            user_obj = self.browse(cr, uid, [user_id,])
            res['value']['user_id_banding_nip'] = user_obj and user_obj[0] and user_obj[0].nip or False
        return res
    
    def onchange_atasan(self, cr, uid, ids, user_id_atasan, context=None):
        res = {'value': {'user_id_banding': False,
                         'user_id_atasan_nip': False
                         }}
        if user_id_atasan:
            user_obj = self.browse(cr, uid, [user_id_atasan,])
            res['value']['user_id_banding'] = user_obj and user_obj[0] and user_obj[0].user_id_atasan and user_obj[0].user_id_atasan.id or False
            res['value']['user_id_atasan_nip'] = user_obj and user_obj[0] and user_obj[0].nip  or False
        return res
    
    def _get_status_atasan_data_pegawai(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context=context):
            message=True
            
            if not employee.user_id_banding :
                message=False
            if not employee.user_id_atasan :
                message=False
            if not employee.company_id :
                message=False
            
            if not message:
                res[employee.id] = 'False'
            else :
                res[employee.id] = ''
        return res
    def update_target_and_realisasi(self, cr, uid, ids, context=None):
        task_pool = self.pool.get('project.task')
        target_pool = self.pool.get('project.project')
        if not isinstance(ids, list): ids = [ids]
        for employee in self.browse(cr, uid, ids, context=context):
            vals = {}
            #print "employee.user_id.id : ",employee.user_id.id
            task_ids = task_pool.search(cr,uid,[('user_id','=',employee.user_id.id)],context=None)
            target_ids = target_pool.search(cr,uid,[('user_id','=',employee.user_id.id)],context=None)
            for task_obj in task_pool.browse(cr, uid, task_ids, context=None) :
                if not employee.user_id_atasan :
                    if not employee.user_id_atasan.user_id:
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Data Kepegawaian Belum Lengkap.'))
                    else :
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Data Kepegawaian Belum Lengkap.'))
                if not employee.user_id_banding:
                    if not employee.user_id_banding.user_id:
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Data Kepegawaian Belum Lengkap.'))
                    else :
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Data Kepegawaian Belum Lengkap.'))
                if not employee.company_id:
                    if not employee.company_id.user_id_bkd:
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Data Kepegawaian Belum Lengkap.'))
                    else :
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Data Kepegawaian Belum Lengkap.'))
                update_pic = {
                                    'user_id_atasan': employee.user_id_atasan.user_id.id,
                                    'user_id_banding': employee.user_id_banding.user_id.id,
                                    'user_id_bkd': employee.company_id.user_id_bkd.id,
                                    'company_id': employee.company_id.id,
                                     }
                task_pool.write(cr, 1, [task_obj.id], update_pic)
           
            if target_ids :
                for target_obj in target_pool.browse(cr, uid,target_ids ,  context=None):
                    if target_obj.user_id and target_obj.user_id.id!=employee.user_id.id :
                        continue;
                    update_pic = {
                                        'user_id_atasan': employee.user_id_atasan.user_id.id,
                                        'user_id_banding': employee.user_id_banding.user_id.id,
                                        'user_id_bkd': employee.company_id.user_id_bkd.id,
                                        'company_id': employee.company_id.id,
                                         }
                    target_pool.write(cr, 1, [target_obj.id], update_pic)
        
        return True
    def _get_lower_fullname(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context=context):
            if employee.name:
                res[employee.id] = employee.name.lower()
            
        return res
    def action_summary_task(self, cr, uid, ids, context=None):
        res = {}
        task_pool = self.pool.get('project.task')
        for employee in self.browse(cr, uid, ids, context=context) :
            task_ids = task_pool.search(cr, uid, [('employee_id', '=', employee.id),
                                                   ('work_state', '=', 'done'),
                                                   ], context=None)
            print "len task : ",len(task_ids)
            task_pool.action_task_summary_calculation(cr,uid,task_ids,context)   
            task_pool.do_yearly_summary_calculation(cr, uid, task_ids, context) 
                                    
            
    
    _columns = {
        'nip'     : fields.char('NIP',size=20),
        'lower_full_name'     : fields.function(_get_lower_fullname, method=True, string='Nama Lengkap', type='char', readonly=True,store=True),    
        'masa_kerja'     : fields.integer('Masa Kerja Sesuai Pengangkatan'),
        'tempat_lahir'     : fields.char('Tempat Lahir',size=128),
        'tanggal_lahir'     : fields.date('Tanggal Lahir'),
        'diklat_kepemimpinan'     : fields.char('Diklat Kepemimpinan Terakhir',size=228),
        'diklat_fungsional'     : fields.char('Diklat Fungsional Terakhir',size=228),
        'agama'     : fields.selection([('islam', 'Islam'),  
                                                      ('katholik', 'Katholik'), 
                                                      ('protestan', 'Protestan'), 
                                                      ('hindu', 'Hindu'), 
                                                      ('budha', 'Budha') 
                                                     ,
                                                     ],'Agama', 
                                                     ),
        'biro_id': fields.many2one('hr.employee.biro', 'Biro', ),
        'department_id': fields.many2one('hr.department', 'Unit Kerja'),
        'job_type': fields.selection([('struktural', 'Jabatan Struktural'), ('jft', 'Jabatan Fungsional Tertentu'), ('jfu', 'Jabatan Fungsional Umum')], 'Tipe Jabatan'),
        'eselon_id': fields.many2one('hr.employee.eselon', 'Eselon'),
        'golongan_id': fields.many2one('hr.employee.golongan', 'Golongan'), 
        'job_id': fields.many2one('hr.job', 'Jabatan'),
         'user_id_atasan': fields.many2one('res.partner', 'Pejabat Penilai' ,domain="[('employee','=',True)]" ),
         'user_id_atasan_nip': fields.related('user_id_atasan','nip', type='char', string='Nip Pejabat Penilai', store=False,readonly=True),
        'user_id_banding': fields.many2one('res.partner', 'Atasan Pejabat Penilai' ,domain="[('employee','=',True)]"),   
        'user_id_banding_nip': fields.related('user_id_banding','nip', type='char', string='Nip Atasan Pejabat Penilai', store=False,readonly=True),
   
        'gelar_depan': fields.many2one('hr.employee.title', 'Gelar Depan',domain="[('title_type','=','gelar_depan')]"),
        'gelar_blk': fields.many2one('hr.employee.title', 'Gelar Belakang',domain="[('title_type','=','gelar_belakang')]"),   
        'nama_sekolah': fields.many2one('hr.employee.school', 'Nama Sekolah'),
        'jurusan': fields.many2one('hr.employee.study', 'Jurusan Pendidikan'),
         'is_head_of_all': fields.boolean('Kepala Daerah', ),
         'is_share_users': fields.boolean('Shared', ),
         'data_preparation': fields.boolean('Data Preparation', ),
        'status_data_atasan_pegawai' :fields.function(_get_status_atasan_data_pegawai, method=True, string='Kelengkapan Data Atasan', type='char', readonly=True,store=False),
        #'status_data_pegawai' :fields.function(_get_status_data_pegawai, method=True, string='Kelengkapan Data', type='char', readonly=True,store=False),
         'is_kepala_opd' :fields.function(_get_is_kepala_opd, method=True, string='Kepala OPD', type='boolean', readonly=True,store=True),
      
    }
    _defaults = {
        'employee' : True,
        'is_head_of_all' : False,
        'data_preparation':False,
    }
    _sql_constraints = [
         ('name_uniq', 'unique (nip)',
             'Data Tidak Bisa Dimasukan, NIP Sudah Tersedia')
     ]
    def init(self, cr):
        pass   
res_partner()
