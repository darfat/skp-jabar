# -*- encoding: utf-8 -*-
##############################################################################
#
#    Istana Group, PT
#    IT Department
#    Copyright (c) 2013 <http://www.asdarfat.wordpress.com>
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

from osv import osv
from osv import fields
from tools.translate import _
from datetime import datetime,timedelta
import time

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    _description    ="Data Pegawai | PNS Pemprov Jabar"
   
    def _get_status_data_pegawai(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context=context):
            message=True
            if not employee.nip : 
                message=False
            elif not employee.eselon_id :
                message=False
            if not employee.job_type :
                message=False
            if not employee.job_id :
                message=False
            if not employee.golongan_id :
                message=False
            if not employee.user_id_banding :
                message=False
            if not employee.parent_id :
                message=False
            if not employee.company_id :
                message=False
            
            if not message:
                res[employee.id] = 'False'
            else :
                res[employee.id] = None
        return res
    def _get_status_atasan_data_pegawai(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context=context):
            message=True
            
            if not employee.user_id_banding :
                message=False
            if not employee.parent_id :
                message=False
            if not employee.company_id :
                message=False
            
            if not message:
                res[employee.id] = 'False'
            else :
                res[employee.id] = ''
        return res
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
    def _get_lower_fullname(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        for employee in self.browse(cr, uid, ids, context=context):
            if employee.name:
                res[employee.id] = employee.name.lower()
            
        return res
    def atasan_change(self, cr, uid, ids, parent_id, context=None):
        #print "XXXX : ",parent_id
        if not parent_id:
            return {'value': {}}
        nip = '';
        employee =  self.browse(cr, uid, parent_id, context=context)
        if not employee:
            raise osv.except_osv(_('Invalid Action, Data Pejabat Penilai Tidak Lengkap'),
                                _('Silakan Hubungi Admin Masing-Masing OPD Untuk Kelengkapan Data Pejabat Penilai.'))
            return {'value': {}}
        
        if employee.nip:
           nip =employee.nip 
        val = {
            'parent_id_nip': nip,
        }
        return {'value': val}
        
    def atasan_banding_nip_change(self, cr, uid, ids, user_id_banding, context=None):
        
        if not user_id_banding:
            return {'value': {}}
        nip = '';
        employee =  self.browse(cr, uid, user_id_banding, context=context)
        if not employee:
            raise osv.except_osv(_('Invalid Action, Data Atasan Pejabat Penilai Tidak Lengkap'),
                                _('Silakan Hubungi Admin Masing-Masing OPD Untuk Kelengkapan Data Atasan Pejabat Penilai.'))
            return {'value': {}}
        if employee.nip:
           nip =employee.nip 
        val = {
            'user_id_banding_nip': nip,
        }  
        
        return {'value': val}
    
    _columns = {
        'nip'     : fields.char('NIP',size=20,required=True),        
        'lower_full_name'     : fields.function(_get_lower_fullname, method=True, string='Nama Lengkap', type='char', readonly=True,store=True),
        'usia'     : fields.integer('Usia'),
        'masa_kerja'     : fields.integer('Masa Kerja Sesuai Pengangkatan'),  
        'user_id_banding': fields.many2one('hr.employee', 'Atasan Pengajuan Banding'),   
        'user_id_banding_nip': fields.related('user_id_banding','nip', type='char', string='Nip Atasan Pejabat Penilai', store=False,readonly=True),
        'parent_id_nip': fields.related('parent_id','nip', type='char', string='Nip Atasan Langsung', store=False,readonly=True),
        'gelar_depan': fields.many2one('hr.employee.title', 'Gelar Depan',domain="[('title_type','=','gelar_depan')]"),
        'gelar_blk': fields.many2one('hr.employee.title', 'Gelar Belakang',domain="[('title_type','=','gelar_belakang')]"),   
        'nama_sekolah': fields.many2one('hr.employee.school', 'Nama Sekolah'),
        'jurusan': fields.many2one('hr.employee.study', 'Jurusan Pendidikan'),
        'golongan_id': fields.many2one('hr.employee.golongan', 'Golongan'), 
        'tempat_lahir'     : fields.char('Tempat Lahir',size=128),
        'tanggal_lahir'     : fields.date('Tanggal Lahir'),
        'diklat_kepemimpinan'     : fields.char('Diklat Kepemimpinan Terakhir',size=228),
        'diklat_fungsional'     : fields.char('Diklat Fungsional Terakhir',size=228),
        'alamat_rumah'     : fields.text('Alamat Rumah'),
        'agama'     : fields.selection([('islam', 'Islam'),  
                                                      ('katholik', 'Katholik'), 
                                                      ('protestan', 'Protestan'), 
                                                      ('hindu', 'Hindu'), 
                                                      ('budha', 'Budha') 
                                                     ,
                                                     ],'Agama', 
                                                     ),
        'eselon_id': fields.many2one('hr.employee.eselon', 'Eselon', required=True),
        'biro_id': fields.many2one('hr.employee.biro', 'Biro', ),
        'job_type': fields.selection([('struktural', 'Jabatan Struktural'), ('jft', 'Jabatan Fungsional Umum'), ('jfu', 'Jabatan Fungsional Tertentu')], 'Tipe Jabatan', required=True),
        'task_ids': fields.one2many('project.task','employee_id', 'Satuan Kerja Pegawai', readonly=True),
        'status_data_pegawai' :fields.function(_get_status_data_pegawai, method=True, string='Kelengkapan Data', type='char', readonly=True,store=False),
        'status_data_atasan_pegawai' :fields.function(_get_status_atasan_data_pegawai, method=True, string='Kelengkapan Data Atasan', type='char', readonly=True,store=False),
        'is_kepala_opd' :fields.function(_get_is_kepala_opd, method=True, string='Kepala OPD', type='boolean', readonly=True,store=False),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (nip)',
             'Data Tidak Bisa Dimasukan, NIP Sudah Tersedia')
     ]
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
                
                
              
                        
                if not employee.parent_id :
                    if not employee.parent_id.user_id:
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
                                    'user_id_atasan': employee.parent_id.user_id.id,
                                    'user_id_banding': employee.user_id_banding.user_id.id,
                                    'user_id_bkd': employee.company_id.user_id_bkd.id,
                                    'company_id': employee.company_id.id,
                                     }
                task_pool.write(cr, 1, [task_obj.id], update_pic)
            if target_ids :
                for target_obj in target_pool.browse(cr, uid,target_ids ,  context=None):
                    if target_obj.user_id and target_obj.user_id.id!=uid :
                        continue;
                    update_pic = {
                                        'user_id_atasan': employee.parent_id.user_id.id,
                                        'user_id_banding': employee.user_id_banding.user_id.id,
                                        'user_id_bkd': employee.company_id.user_id_bkd.id,
                                        'company_id': employee.company_id.id,
                                         }
                    target_pool.write(cr, 1, [target_obj.id], update_pic)
        
        return True
#NIP    GLR DEPAN    NAMA PEGAWAI    GLR BLKG    JABATAN    GOL    UNIT KERJA/OPD    JURUSAN PENDIDIKAN    NAMA SEKOLAH    USIA    MASA KERJA SESUAI PENGANGKATAN
hr_employee()

class hr_department(osv.osv):
    _inherit = 'hr.department'
    _description    ="Unit Kerja / OPD"
   
    _columns = {
        'name': fields.char("Nama Unit", size=256, required=True),
        'department_type': fields.selection([('Badan', 'Badan'), ('dinas', 'Dinas'), ('giro', 'Giro')], 'Tipe'),
        'bkd_auditor_id': fields.many2one('hr.employee', 'Staff Pemeriksa BKD'),
        
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name)',
             'Data Tidak Bisa Dimasukan, Nama Departemen Sudah Tersedia')
     ]

hr_department()
class hr_job(osv.osv):
    _name = "hr.job"
    _description = "Job Description"
    _inherit = ['hr.job']
    _columns = {
        'name': fields.char('Jabatan Pegawai', size=350, required=True ),
        'name_alias': fields.char('Alias Jabatan ', size=350, help="Nama Jabatan Yang Terlampir Dalam Surat Sesuai Dengan Standarisasi Nomenteratur"),
     }
    _sql_constraints = [
        ('name_company_uniq', 'unique(name, company_id)', 'The name of the job position must be unique per company!'),
    ]
hr_job()

#PARAM AND CONFIGURATION #-------------------------------
class hr_employee_title(osv.osv):
    _name = "hr.employee.title"
    _description = "Gelar Depan Dan Belakang"
    _columns = {
        'name': fields.char("Nama Gelar", size=64, required=True),
        'title_type': fields.selection([('gelar_depan', 'Gelar Depan'), ('gelar_belakang', 'Gelar Belakang')], 'Jenis Gelar', required=True,
            help="Contoh Gelar Depan :Dr. H.;H | Contoh Gelar Belakang :S.STP.,MAP;AM.KG "),
        #'employee_ids': fields.many2many('hr.employee', 'employee_title_rel', 'title_id', 'emp_id', 'Pegawai'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name,title_type)',
             'Data Tidak Bisa Dimasukan, Nama Gelar Sudah Tersedia')
     ]
hr_employee_title()

class hr_employee_school(osv.osv):
    _name = "hr.employee.school"
    _description = "Nama Sekolah"
    _columns = {
        'name': fields.char("Nama Sekolah", size=150, required=True),
        'school_type': fields.selection([('sma', 'SMA'), ('smk', 'SMK'), ('stm', 'STM'), ('universitas', 'Universitas'), ('politeknik', 'Politeknik'), ('universitas', 'Universitas'), ('sekolah_tinggi', 'Sekolah Tinggi'), ('institut', 'Institut'), ('lainnya', 'Lainnya')], 'Tipe'),
        #'employee_ids': fields.many2many('hr.employee', 'employee_school_rel', 'school_id', 'emp_id', 'Pegawai'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name)',
             'Data Tidak Bisa Dimasukan, Nama Sekolah Sudah Tersedia')
     ]
hr_employee_school()
class hr_employee_study(osv.osv):
    _name = "hr.employee.study"
    _description = "Gelar Jurusan"
    _columns = {
        'name': fields.char("Jurusan Pendidikan", size=150, required=True),
        #'employee_ids': fields.many2many('hr.employee', 'employee_study_rel', 'study_id', 'emp_id', 'Pegawai'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name)',
             'Data Tidak Bisa Dimasukan, Nama Jurusan Sudah Tersedia')
     ]
    
hr_employee_study()
class hr_employee_golongan(osv.osv):
    _name = "hr.employee.golongan"
    _description = "Golongan Pegawai"
    _columns = {
        'name': fields.char("Golongan", size=12, required=True),
        'description': fields.char("Deskripsi", size=256, ),
        'employee_ids': fields.many2many('hr.employee', 'employee_gol_rel', 'golongan_id', 'emp_id', 'Pegawai'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name)',
             'Data Tidak Bisa Dimasukan, Nama Golongan Sudah Tersedia')
     ]
hr_employee_golongan()
class hr_employee_eselon(osv.osv):
    _name = "hr.employee.eselon"
    _description = "Eselon Pegawai"
    _columns = {
        'code': fields.char("Kode", size=8, required=True),
        'name': fields.char("Eselon", size=25,required=True ),        
    }
    _sql_constraints = [
         ('name_uniq', 'unique (code)',
             'Data Tidak Bisa Dimasukan, Nama Eselon Sudah Tersedia')
     ]
hr_employee_eselon()
class hr_employee_biro(osv.osv):
    _name = "hr.employee.biro"
    _description = "Biro Pegawai"
    _columns = {
        'name': fields.char("Biro", size=25,required=True ),
        'description': fields.text("Deskripsi"),
                
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name)',
             'Data Tidak Bisa Dimasukan, Nama Biro Sudah Tersedia')
     ]
hr_employee_eselon()

