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

from osv import osv
from osv import fields
from tools.translate import _
import decimal_precision as dp
from datetime import datetime,timedelta
import time
from mx import DateTime
from openerp.tools import html_email_clean
from openerp.addons.base_status.base_stage import base_stage
from openerp.addons.resource.faces import task as Task
import openerp.addons.decimal_precision as dp


class notification_generate_task(osv.osv_memory):
    _name = "notification.generate.task"
    _columns = {
        'name': fields.char('Notif', size=128),
    }
class notification_cancel_task(osv.osv_memory):
    _name = "notification.cancel.task"
    _columns = {
        'name': fields.char('Notif', size=128),
    }
class project(osv.osv):
    _inherit = 'project.project'
    _description    ="Target Dari Sasaran Kerja"
    def ASDASD(self, cr, uid, fields=None, context=None):
        res = super(project, self).fields_get(cr, uid, fields, context)
        curr_user = self.pool.get('res.users').browse(cr, uid, uid, context)
        for f in res:
            #if f in ('suggest_jumlah_kuantitas_output','suggest_kualitas','suggest_waktu','suggest_biaya','suggest_angka_kredit'):
            if f.find('suggest_')==0:
                for group in curr_user.groups_id :
                    if group.category_id.name =='Project' and group.name == 'User' :
                        res[f]['readonly']=True;
                    if group.category_id.name =='Project' and group.name == 'Evaluasi BKD' :
                        res[f]['readonly']=True;
                    if group.category_id.name =='Project' and group.name == 'Atasan Banding' :
                        res[f]['readonly']=True;
                    if group.category_id.name =='Project' and group.name == 'Manager' :
                        res[f]['readonly']=False;
            elif f in ('target_jumlah_kuantitas_output','target_satuan_kuantitas_output','target_kualitas','target_waktu','target_satuan_waktu','target_biaya','target_angka_kredit'):
                for group in curr_user.groups_id :
                    if group.category_id.name =='Project' and group.name == 'User' :
                        res[f]['readonly']=False;
                    if group.category_id.name =='Project' and group.name == 'Manager' :
                        res[f]['readonly']=True;
                    if group.category_id.name =='Project' and group.name == 'Evaluasi BKD' :
                        res[f]['readonly']=True;
                    if group.category_id.name =='Project' and group.name == 'Atasan Banding' :
                        res[f]['readonly']=True;
            
           
          
        return res
    def write(self, cr, uid, ids, vals, context=None):
        
        #print "Ovveride Write Target...======================="     
        if not isinstance(ids, list): ids = [ids]
        for project_obj in self.browse(cr, uid, ids, context=context):
            task_id = project_obj.id
            if uid != 1:
                if project_obj.state in ('template','draft','new','rejected_manager','correction'):
                    if not self.get_auth_id(cr, uid, [task_id],'user_id', context=context):
                        return False
                if project_obj.state in ('propose','rejected_bkd'):
                    if not self.get_auth_id(cr, uid, [task_id],'user_id_atasan', context=context):
                        return False
                if project_obj.state in ('evaluated','propose_correction','propose_to_close'):
                    if not self.get_auth_id(cr, uid, [task_id],'user_id_bkd', context=context):
                        return False
                if project_obj.state in ('done','cancelled','open','closed','pending'):
                    if not self.get_auth_id(cr, uid, [task_id],'user_id_bkd', context=context):
                        return False
                
        super(project, self).write(cr, uid, ids, vals, context=context)           
        return True
    def onchange_targettype(self, cr, uid, ids, target_type, context=None):
        #print "target_type... : ",target_type
        #print "target_type... : ",ids
        
        if not target_type:
            return {'value': {}}
        if target_type in ('dipa_apbn','dpa_opd_biro','sotk'):
                    val = {
                   'color': 3,
                   }
        if target_type in ('lain_lain'):
                     val = {
                   'color': 4,
                   }
        if target_type in ('tambahan'):
                      val = {
                   'color': 5,
                   }
        if target_type in ('perilaku'):
                 val = {
                           'color': 6,
                           }
        
        
        return {'value': val}
    def onchange_lamakegiatan(self, cr, uid, ids, lama_kegiatan, context=None):
        if lama_kegiatan:
            return {'value': {'target_waktu': lama_kegiatan}}
        return {'value': {}}
    def _get_total_target_biaya_(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        for _target in self.browse(cr, uid, ids, context=context):
            res[_target.id] = 0.0
            if _target.target_biaya >0 :
                if _target.realisasi_lines:
                    for task_obj in _target.realisasi_lines:
                        res[_target.id] += task_obj.target_biaya
                
        return res  
    def _get_total_target_angka_kredit(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        for _target in self.browse(cr, uid, ids, context=context):
            res[_target.id] = 0.0
            if _target.target_angka_kredit >0 :
                if _target.realisasi_lines:
                    for task_obj in _target.realisasi_lines:
                        res[_target.id] += task_obj.target_angka_kredit
                
        return res  
    def _get_employee_from_user(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        if not ids:
            return res
        
        for task_obj in self.browse(cr, uid, ids, context=context):
            user_id = task_obj.user_id
            #    print "User ID",user_id
            if user_id : 
                employees = self.pool.get('res.users').browse(cr, uid, user_id.id, context=context)
                if employees :
                    for user_employees in employees.employee_ids:
                        res[task_obj.id] = user_employees.id
                else :
                     res[task_obj.id] = False
            else :
                res[task_obj.id] = False
        return res
    _columns = {
        #'name': fields.char('Description', size=120, select=True, readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)]},),
        'state': fields.selection([('template', 'Template'),('draft','Draft'),('new','Baru'),
                                   ('propose','Pengajuan Atasan'), ('rejected_manager', 'Pengajuan Ditolak'),
                                   ('evaluated','Verifikasi BKD'), ('rejected_bkd', 'Pengajuan Ditolak BKD'),
                                   ('confirm','Target Di Terima'), 
                                   ('open','In Progress'), ('cancelled', 'Cancelled'),('pending','Pending'),
                                   ('propose_to_close','Pengajuan Closing Target'),('closed','Closed'),
                                   ('deleted', 'Batal'),
                                   ('propose_correction', 'Ajukan Perubahan Target'),
                                   ('correction', 'Revisi Target'),
                                   ], 'Status', required=True,),
        'lama_kegiatan'     : fields.integer('Lama Kegiatan',required=True,readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'correction': [('readonly', False)]},),
        'code'     : fields.char('Kode Kegiatan',size=20,readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)]},),
        'notes'     : fields.text('Catatan'),
        'satuan_lama_kegiatan'     : fields.selection([('bulan', 'Bulan')],'Satuan Waktu Lama Kegiatan',readonly=True),
        'target_type_id': fields.selection([          ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),  
                                                      ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),                                                       
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang SOTK OPD/Biro'), 
                                                      ('lain_lain', 'Lain-Lain'), 
                                                      #('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      #('perilaku', 'Perilaku Kerja')
                                                      ],
                                                      'Jenis Kegiatan', required=True, readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'correction': [('readonly', False)]},
                                                     ),
        'target_category': fields.selection([('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')], 'Kategori',required=True, readonly=True),
        'target_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')],'Periode Bulan'
                                                     ),
        'target_period_year'     : fields.char('Periode Tahun',size=4, required=True, readonly=True),
        'target_jumlah_kuantitas_output'     : fields.float('Kuantitas Output',required=True,readonly=True,digits_compute=dp.get_precision('no_digit'),states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]}, ),
        'target_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output' ,required=True,readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'target_angka_kredit'     : fields.float('Angka Kredit',digits_compute=dp.get_precision('angka_kredit') ,readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'target_kualitas'     : fields.float('Kualitas',required=True,readonly=True,digits_compute=dp.get_precision('no_digit'),states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'target_waktu'     : fields.integer('Waktu',required=True,readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'target_satuan_waktu'     : fields.selection([('bulan', 'Bulan'),('hari', 'Hari')],'Satuan Waktu',select=1,required=True,readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'target_biaya'     : fields.float('Biaya',readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'target_lainlain'     : fields.integer('Lain-Lain',readonly=True,states={'draft': [('readonly', False)],'new': [('readonly', False)],'propose': [('readonly', False)],'correction': [('readonly', False)]},),
        'suggest_jumlah_kuantitas_output'     : fields.float('Kuantitas Output',
                                                            read=['project.group_project_user'],write=['project.group_project_manager'],
                                                            required=True,states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]}, ),
        'suggest_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output' ,required=True,states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]},),
        'suggest_angka_kredit'     : fields.float('Angka Kredit',states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]},),
        'suggest_kualitas'     : fields.float('Kualitas',readonly=True,digits_compute=dp.get_precision('no_digit'),states={'rejected_manager': [('readonly', False)],'propose': [('readonly', False)]},),
        'suggest_waktu'     : fields.integer('Waktu',required=True,readonly=True,states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]},),
        'suggest_satuan_waktu'     : fields.selection([('bulan', 'Bulan'),('hari', 'Hari')],'Satuan Waktu',select=1,required=True,states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]},),
        'suggest_biaya'     : fields.float('Biaya',readonly=True,states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]},),
        'suggest_lainlain'     : fields.integer('Lain-Lain',readonly=True,states={'rejected_bkd': [('readonly', False)],'propose': [('readonly', False)]},),
        
        'status_target_bulanan': fields.selection([('belum', 'Target Bulanan Belum Dibuat'), ('sudah', 'Target Sudah Dibuat')], 'Status Target Bulanan', readonly=True),
        'user_id_atasan': fields.many2one('res.users', 'Pejabat Penilai', ),
        'user_id_banding': fields.many2one('res.users', 'Atasan Pejabat Penilai', ),
        'user_id_bkd': fields.many2one('res.users', 'Pejabat Pengevaluasi (BKD)', ),
        'nilai_akhir': fields.float( 'Nilai',readonly=True),
        'jumlah_perhitungan': fields.float( 'Jumlah Perhitungan',readonly=True),
        'indeks_nilai_akhir': fields.selection([('a', 'A'), ('b', 'B'),('c', 'C'), ('d', 'D')], 'Indeks', readonly=True),
        'indeks_perilaku': fields.selection([('a', 'A'), ('b', 'B'),('c', 'C'), ('d', 'D')], 'Indeks', readonly=True),
        'realisasi_lines': fields.one2many('project.task', 'project_id', 'Target Bulanan',order='target_period_month'),
        'total_biaya_bulanan': fields.function(_get_total_target_biaya_, method=True, readonly=True,string='Total Biaya Hasil Generate', store=False),
        'total_angka_kredit_bulanan': fields.function(_get_total_target_angka_kredit, method=True, readonly=True,digits_compute=dp.get_precision('angka_kredit'),string='Total Angka Kredit Hasil Generate', store=False),
       # 'currency_id': fields.related('company_id', 'currency_id', type='many2one', relation='res.currency', string='Currency', readonly=True,store=False),
         'employee_id': fields.related('user_id', 'partner_id', relation='res.partner', type='many2one', string='Data Pegawai', store=False),
        'count_correction'     : fields.integer('Jumlah Koreksi',readonly=True),
        
    }
    _defaults = {
        'use_tasks': False,
        'target_period_year':lambda *args: time.strftime('%Y'),
        'user_id': lambda self, cr, uid, ctx: uid,
        'date_start':False,
        'satuan_lama_kegiatan':'bulan',
        'lama_kegiatan':1,
        'target_category':'tahunan',
        'target_satuan_waktu':'bulan',
        'target_kualitas':100,
        'status_target_bulanan':'belum',
        'state': 'draft',
        'name':'',
        'target_jumlah_kuantitas_output':False,
        'target_angka_kredit':False,
        'target_kualitas':False,
        'target_waktu':12,
        'target_biaya':0,
        'count_correction':0
    }
    
    def generate_target_realisasi_bulanan(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task =  {}
        member =  {}
        
        target_pool = self.pool.get('project.project')
        member_pool = self.pool.get('project.user.rel')
        task_pool = self.pool.get('project.task')
        stage_pool = self.pool.get('project.task.type')
        for target_obj in self.browse(cr, uid, ids, context=context):
            task_ids = task_pool.search(cr, uid, [('project_id','=',target_obj.id)], context=None)
            task_pool.unlink(cr, uid, task_ids, context=None)
            #print "Target Name : ",target_obj.name
            target_category='bulanan'
            description=target_obj.name
            lama_kegiatan=target_obj.lama_kegiatan
            user_id = target_obj.user_id.id
            target_period_month='xx'
            date_start='xx'
            date_end='xx'
            company_id=None
            currency_id=None
            user_id_bkd=None
            employee = self.get_employee_from_user_id( cr, uid, target_obj);
            if user_id!=uid:
              raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            if not employee :
                raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Ada Beberapa Informasi Kepegawaian Belum Diisi, Khususnya Data Pejabat Penilai Dan Atasan Banding.'))
            else :
                company = employee.company_id
                company_id = company.id
                currency_id= employee.company_id.currency_id
                
                #print "company_id : ",company_id,' - ',currency_id
                
                if not company_id :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Unit Dinas Pegawai Belum Dilengkapi.'))
                #print "employee parent : ",employee.parent_id
                if not target_obj.user_id_bkd:
                    if not company.user_id_bkd :
                        raise osv.except_osv(_('Invalid Action, Data Dinas Kurang Lengkap'),
                                    _('Staff Pemeriksa Dari BKD Tidak Tersedia Untuk Unit Anda, Silahkan hubungi Admin Atau isi Data Pemeriksa.'))
                    else :
                        user_id_bkd = company.user_id_bkd.id
                else :
                    user_id_bkd=target_obj.user_id_bkd.id 
                if not employee.user_id_atasan :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Penilai Belum Terisi.'))
                if not employee.user_id_banding :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Pengajuan Banding.'))
            
            user_id_atasan =target_obj.user_id_atasan.id
            user_id_banding=target_obj.user_id_banding.id 
            
            if not target_obj.user_id_atasan.id :
                user_id_atasan = employee.user_id_atasan.user_id.id
            if not target_obj.user_id_banding.id :
                user_id_banding = employee.user_id_banding.user_id.id
            color=1;
            
            if target_obj.target_type_id in ('dipa_apbn','dpa_opd_biro','sotk'):
                       color=3;
            if target_obj.target_type_id in ('lain_lain'):
                       color=4
            if target_obj.target_type_id in ('tambahan'):
                       color=5
            if target_obj.target_type_id in ('perilaku'):
                       color=6
            task.update({
                           'project_id':target_obj.id,
                           'user_id':user_id,
                           'company_id':company_id,
                           'description':description,
                           'name': target_obj.name,
                           'code': target_obj.code,
                           'target_category': target_category,
                           'sequnce': target_obj.priority,
                           'target_type_id':target_obj.target_type_id,
                           'target_period_year': target_obj.target_period_year,
                           'target_jumlah_kuantitas_output'     : target_obj.target_jumlah_kuantitas_output,
                            'target_satuan_kuantitas_output'     : target_obj.target_satuan_kuantitas_output.id or None,
                            'target_angka_kredit'     : target_obj.target_angka_kredit,
                            'target_kualitas'     : target_obj.target_kualitas,
                            'target_waktu'     : target_obj.target_waktu,
                            'target_satuan_waktu'     : 'hari',
                            'target_biaya'     : target_obj.target_biaya,
                            'target_lainlain'     : target_obj.target_lainlain,
                            'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'priority':'2',
                            'notes':'-',
                            'currency_id':currency_id,
                            'task_category':'skp'
                           })
            #Update Task Target Bulanan
            now=DateTime.today();
            part_jumlah_kuantitas_output=0
            part_angka_kredit=0
            part_biaya=0
            kuantitas=target_obj.target_jumlah_kuantitas_output
            ang_kredit=target_obj.target_angka_kredit
            biaya=target_obj.target_biaya
            x_kuantitas=kuantitas/lama_kegiatan
            y_kuantitas =kuantitas%lama_kegiatan
            x_kredit=ang_kredit/lama_kegiatan
            y_kredit =ang_kredit%lama_kegiatan
            x_biaya=biaya/lama_kegiatan
            y_biaya =biaya%lama_kegiatan
            first_task_id=None
            sum_of_balance_biaya=0
            if target_obj.date_start :
                curr_date = DateTime.strptime(target_obj.date_start,'%Y-%m-%d')
            else :
                january=DateTime.Date(now.year,1,1)
                curr_date =  DateTime.strptime(january.strftime('%Y-%m-%d'),'%Y-%m-%d')
            first_date =curr_date
            #print "THIS IS A DATE ",curr_date
            for i in range(0,lama_kegiatan):
                #Jumlah Kuantitas Output
                if kuantitas >0 :
                    if i < y_kuantitas :
                        part_jumlah_kuantitas_output=x_kuantitas+1
                    else :
                        part_jumlah_kuantitas_output=x_kuantitas
                #angka Kredit
                #if ang_kredit >0 :
                #    if i < y_kredit :
                #        part_angka_kredit=x_kredit+1
                #    else :
                part_angka_kredit=x_kredit   
                #Biaya
                if biaya >0 :
                    part_biaya=round(x_biaya) 
                    sum_of_balance_biaya+=part_biaya    
                next_date = curr_date + DateTime.RelativeDateTime(months=i)
                target_period_month=next_date.strftime('%m')
                task.update({
                           'target_period_month':target_period_month,
                           'target_jumlah_kuantitas_output'     : part_jumlah_kuantitas_output,
                           'target_waktu'     : 20,
                           'target_angka_kredit'     : part_angka_kredit,
                           'target_biaya'     : part_biaya,
                 })
                date_start='xx'
                date_end='xx'
                stage_ids = stage_pool.search(cr,uid,[('sequence','=',0)], context=None)
                #print "stage_id : ",stage_ids
                work_state='draft';
                if stage_ids :
                    task.update({
                                'stage_id': stage_ids[0],
                                'work_state':work_state,
                                'state':'draft',
                                'currency_id':currency_id
                               
                        })
                if i == (lama_kegiatan-1) :
                    balancing_biaya = target_obj.target_biaya - sum_of_balance_biaya
                    task.update({
                                'target_biaya':balancing_biaya+part_biaya
                        })
                   #task_pool.write(cr, uid, task_id,update_biaya)

                #insert task
                task_id = task_pool.create(cr, uid, task)
                #print "Task ID : ",task_id
                
            
            #Update Status Target Bulanan
            update_target = {
                            'status_target_bulanan':'sudah',
                            'color':color,
                             'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'date_start':first_date or False
                        }
            
            target_pool.write(cr,uid,target_obj.id,update_target)
            
            
            
            
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'notification.generate.task',
                'target': 'new',
                'context': context,#['notif_booking'],
            }
    def generate_revisi_target_realisasi_bulanan(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task =  {}
        member =  {}
        
        target_pool = self.pool.get('project.project')
        member_pool = self.pool.get('project.user.rel')
        task_pool = self.pool.get('project.task')
        stage_pool = self.pool.get('project.task.type')
        for target_obj in self.browse(cr, uid, ids, context=context):
            task_ids = task_pool.search(cr, uid, [('project_id','=',target_obj.id),('work_state','in',('draft','realisasi','cancelled'))], context=None)
            task_pool.unlink(cr, uid, task_ids, context=None)
            task_exist_ids = task_pool.search(cr, uid, [('project_id','=',target_obj.id),('work_state','not in',('draft','realisasi','cancelled'))], context=None)
            #print "Target Name : ",target_obj.name
            target_category='bulanan'
            description=target_obj.name
            lama_kegiatan=target_obj.lama_kegiatan
            user_id = target_obj.user_id.id
            target_period_month='xx'
            date_start='xx'
            date_end='xx'
            company_id=None
            currency_id=None
            user_id_bkd=None
            employee = self.get_employee_from_user_id( cr, uid, target_obj);
            if user_id!=uid:
              raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            if not employee :
                raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Ada Beberapa Informasi Kepegawaian Belum Diisi, Khususnya Data Pejabat Penilai Dan Atasan Banding.'))
            else :
                company = employee.company_id
                company_id = company.id
                currency_id= employee.company_id.currency_id
                
                #print "company_id : ",company_id,' - ',currency_id
                
                if not company_id :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Unit Dinas Pegawai Belum Dilengkapi.'))
                #print "employee parent : ",employee.parent_id
                if not target_obj.user_id_bkd:
                    if not company.user_id_bkd :
                        raise osv.except_osv(_('Invalid Action, Data Dinas Kurang Lengkap'),
                                    _('Staff Pemeriksa Dari BKD Tidak Tersedia Untuk Unit Anda, Silahkan hubungi Admin Atau isi Data Pemeriksa.'))
                    else :
                        user_id_bkd = company.user_id_bkd.id
                else :
                    user_id_bkd=target_obj.user_id_bkd.id 
                if not employee.user_id_atasan :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Penilai Belum Terisi.'))
                if not employee.user_id_banding :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Pengajuan Banding.'))
            
            user_id_atasan =target_obj.user_id_atasan.id
            user_id_banding=target_obj.user_id_banding.id 
            
            if not target_obj.user_id_atasan.id :
                user_id_atasan = employee.user_id_atasan.user_id.id
            if not target_obj.user_id_banding.id :
                user_id_banding = employee.user_id_banding.user_id.id
            color=1;
            
            if target_obj.target_type_id in ('dipa_apbn','dpa_opd_biro','sotk'):
                       color=3;
            if target_obj.target_type_id in ('lain_lain'):
                       color=4
            if target_obj.target_type_id in ('tambahan'):
                       color=5
            if target_obj.target_type_id in ('perilaku'):
                       color=6
            task.update({
                           'project_id':target_obj.id,
                           'user_id':user_id,
                           'company_id':company_id,
                           'description':description,
                           'name': target_obj.name,
                           'code': target_obj.code,
                           'target_category': target_category,
                           'sequnce': target_obj.priority,
                           'target_type_id':target_obj.target_type_id,
                           'target_period_year': target_obj.target_period_year,
                           'target_jumlah_kuantitas_output'     : target_obj.target_jumlah_kuantitas_output,
                            'target_satuan_kuantitas_output'     : target_obj.target_satuan_kuantitas_output.id or None,
                            'target_angka_kredit'     : target_obj.target_angka_kredit,
                            'target_kualitas'     : target_obj.target_kualitas,
                            'target_waktu'     : target_obj.target_waktu,
                            'target_satuan_waktu'     : 'hari',
                            'target_biaya'     : target_obj.target_biaya,
                            'target_lainlain'     : target_obj.target_lainlain,
                            'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'priority':'2',
                            'notes':'-',
                            'currency_id':currency_id,
                            'task_category':'skp',
                           })
            #Update Task Target Bulanan
            old_kualitas,old_biaya,old_ak = self.get_total_target_aspect_task(cr,uid,task_exist_ids,context=None)
            now=DateTime.today();
            part_jumlah_kuantitas_output=0
            part_angka_kredit=0
            part_biaya=0
            kuantitas=target_obj.target_jumlah_kuantitas_output - old_kualitas
            ang_kredit=target_obj.target_angka_kredit - old_ak
            biaya=target_obj.target_biaya - old_biaya
            part_lama_kegiatan = lama_kegiatan - len(task_exist_ids)
            x_kuantitas=kuantitas/part_lama_kegiatan
            y_kuantitas =kuantitas%part_lama_kegiatan
            x_kredit=ang_kredit/part_lama_kegiatan
            y_kredit =ang_kredit%part_lama_kegiatan
            x_biaya=biaya/part_lama_kegiatan
            y_biaya =biaya%part_lama_kegiatan
            first_task_id=None
            sum_of_balance_biaya=0
            if target_obj.date_start :
                curr_date = DateTime.strptime(target_obj.date_start,'%Y-%m-%d')
            else :
                january=DateTime.Date(now.year,1,1)
                curr_date =  DateTime.strptime(january.strftime('%Y-%m-%d'),'%Y-%m-%d')
            first_date =curr_date
            #print "THIS IS A DATE ",curr_date
            for i in range(0,lama_kegiatan):
                next_date = curr_date + DateTime.RelativeDateTime(months=i)
                target_period_month=next_date.strftime('%m')
                if self.is_exist_task_in_month(cr,uid,task_exist_ids,target_period_month,target_obj.target_period_year,context=None):
                    #print "Break In Month %s %s",target_period_month,target_obj.target_period_year,
                    continue;
                
                #Jumlah Kuantitas Output
                if kuantitas >0 :
                    if i < y_kuantitas :
                        part_jumlah_kuantitas_output=x_kuantitas+1
                    else :
                        part_jumlah_kuantitas_output=x_kuantitas
                #angka Kredit
                #if ang_kredit >0 :
                #    if i < y_kredit :
                #        part_angka_kredit=x_kredit+1
                #    else :
                part_angka_kredit=x_kredit   
                #Biaya
                if biaya >0 :
                    part_biaya=round(x_biaya) 
                    sum_of_balance_biaya+=part_biaya    
                
                task.update({
                           'target_period_month':target_period_month,
                           'target_jumlah_kuantitas_output'     : part_jumlah_kuantitas_output,
                           'target_waktu'     : 20,
                           'target_angka_kredit'     : part_angka_kredit,
                           'target_biaya'     : part_biaya,
                 })
                date_start='xx'
                date_end='xx'
                stage_ids = stage_pool.search(cr,uid,[('sequence','=',0)], context=None)
                #print "stage_id : ",stage_ids
                work_state='draft';
                if stage_ids :
                    task.update({
                                'stage_id': stage_ids[0],
                                'work_state':work_state,
                                'state':'draft',
                                'currency_id':currency_id
                               
                        })
                if i == (lama_kegiatan-1) :
                    balancing_biaya = biaya - sum_of_balance_biaya
                    task.update({
                                'target_biaya':balancing_biaya+part_biaya
                        })
                   #task_pool.write(cr, uid, task_id,update_biaya)

                #insert task
                task_id = task_pool.create(cr, uid, task)
                
                # Update Realisasi Yang sudah selesai Dan inprogress
                exist_task_data = {}
                for task_exist_obj in task_pool.browse(cr, uid, task_exist_ids, context=context):
                     exist_task_data.update({
                           'project_id':target_obj.id,
                           #'user_id':user_id,
                           #'company_id':company_id,
                           'description':description,
                           'name': target_obj.name,
                           'code': target_obj.code,
                           'target_category': target_category,
                           #'sequence': target_obj.priority,
                           'target_type_id':target_obj.target_type_id,
                           #'target_period_year': target_obj.target_period_year,
                           #'target_jumlah_kuantitas_output'     : target_obj.target_jumlah_kuantitas_output,
                           # 'target_satuan_kuantitas_output'     : target_obj.target_satuan_kuantitas_output.id or None,
                           # 'target_angka_kredit'     : target_obj.target_angka_kredit,
                           # 'target_kualitas'     : target_obj.target_kualitas,
                           # 'target_waktu'     : target_obj.target_waktu,
                           # 'target_satuan_waktu'     : 'hari',
                           # 'target_biaya'     : target_obj.target_biaya,
                           # 'target_lainlain'     : target_obj.target_lainlain,
                            'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'priority':'2',
                            #'notes':'-',
                            #'currency_id':currency_id,
                            'task_category':'skp',
                           })
                     task_pool.write(cr,uid,task_exist_obj.id,exist_task_data)
            #Update Status Target Bulanan
            update_target = {
                            'status_target_bulanan':'sudah',
                            'color':color,
                             'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'date_start':first_date or False
                        }
            
            target_pool.write(cr,uid,target_obj.id,update_target)
            
            
            
            
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'notification.generate.task',
                'target': 'new',
                'context': context,#['notif_booking'],
            }
    def is_exist_task_in_month(self, cr, uid,exist_task_ids, period_month, period_year,context=None):
        if exist_task_ids : 
            for task_obj in self.pool.get('project.task').browse(cr, uid,exist_task_ids, context=context):
                if task_obj.target_period_month == period_month and task_obj.target_period_year == period_year :
                    return True
        return False  
    def get_total_target_aspect_task(self, cr,uid, exist_task_ids,context=None):
        total_kuantitas=total_biaya=total_ak =0.0
        if exist_task_ids : 
            for task_obj in self.pool.get('project.task').browse(cr, uid,exist_task_ids, context=context):
                total_kuantitas +=task_obj.target_jumlah_kuantitas_output
                total_biaya +=task_obj.target_biaya
                total_ak +=task_obj.target_angka_kredit
                
        return total_kuantitas,total_biaya,total_ak      
    def get_employee_from_user_id(self, cr, uid, task_obj, context=None):
        user_id  = task_obj.user_id
        #print "User ID",user_id
        if user_id : 
            #employees = self.pool.get('res.users').browse(cr, uid,user_id.id, context=context).employee_ids
            #print "employees ID",employees
            #for employee in employees:
             return user_id.partner_id
        return False
    def get_auth_id(self, cr, uid, ids,type, context=None):
        if not isinstance(ids, list): ids = [ids]
        #print "CONTEXT : ", context
        by_pass_auth=False
        if context:
            by_pass_auth = context.get('bypass_auth',False)
        if by_pass_auth:
            return True;
        for target in self.browse(cr, uid, ids, context=context):
            #print "type :",type
            if type=='user_id' :
                if target.user_id :
                    if target.user_id.id!=uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            elif type=='user_id_atasan' :
                if target.user_id_atasan :
                    if target.user_id_atasan.id!=uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            elif type=='user_id_bkd' :
                if target.user_id_bkd :
                    if target.user_id_bkd.id!=uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
                
            else : 
               return False;
            
        return True;
    def set_new(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id', context=context) :
            return self.write(cr, uid, ids, {'state':'new'}, context=context)
    def set_propose(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id', context=context) :
            for target in self.browse(cr, uid, ids, context=context):
                #print "Target Bulanan ",target.status_target_bulanan
                if target.status_target_bulanan!='sudah' :
                    raise osv.except_osv(_('Invalid Action!'),
                                             _('Sebelum Pengajuan, Harap Generate Target Bulanan Terlebih Dahulu.'))
                if target.target_biaya >0:
                    if target.target_biaya != target.total_biaya_bulanan:
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Penyusunan Target Biaya Bulanan Tidak Sama Dengan Target Biaya Tahunan'))
                if target.lama_kegiatan != target.target_waktu:
                        raise osv.except_osv(_('Invalid Action!'),
                                                 _('Penyusunan Waktu Antara Lama Kegiatan Dan Target Waktu Harus Sama'))
            return self.write(cr, uid, ids, {'state':'propose'}, context=context)
    def set_propose_rejected(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_atasan', context=context) :
            return self.write(cr, uid, ids, {'state':'new'}, context=context)
    def set_evaluated(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_atasan', context=context) :
            return self.write(cr, uid, ids, {'state':'evaluated'}, context=context)
    def set_evaluate_rejected(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_bkd', context=context) :
            return self.write(cr, uid, ids, {'state':'propose'}, context=context)
    def set_confirm(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_bkd', context=context) :
            task_pool = self.pool.get('project.task')
            stage_pool = self.pool.get('project.task.type')
            stage_ids = stage_pool.search(cr,uid,[('sequence','=',1)], context=None)
            work_state='realisasi';
            if stage_ids :
                    update_stage = {
                                'stage_id': stage_ids[0],
                                'work_state':work_state,
                                'state':'draft',
                        }
            task_ids = task_pool.search(cr, uid, [('project_id','=',ids),('work_state','in',('draft','realisasi','cancelled'))], context=None)
            task_pool.write(cr, uid, task_ids,update_stage)
            return self.write(cr, uid, ids, {'state':'confirm'}, context=context)
    def cancel_target(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task_pool = self.pool.get('project.task')
        stage_pool = self.pool.get('project.task.type')
        for target_obj in self.browse(cr, uid, ids, context=context):
            task_ids = task_pool.search(cr, uid, [('project_id','=',target_obj.id)], context=None)
            task_pool.unlink(cr, uid, task_ids, context=None)
            return self.write(cr, uid, ids, {'state':'deleted'}, context=context)
        
        return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'notification.cancel.task',
                    'target': 'new',
                    'context': context,#['notif_booking'],
                }
    def set_correction_reject(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_bkd', context=context) :
            return self.write(cr, uid, ids, {'state':'confirm'}, context=context)
    def set_correction_approve(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_bkd', context=context) :
            for target_obj in self.browse(cr, uid, [target_id], context=context):
                x_count_correction=0;
                if target_obj.count_correction:
                    x_count_correction = target_obj.count_correction
            
            x_count_correction=x_count_correction+1
            
            update_state = {
                                'count_correction':x_count_correction,
                                'state':'correction',
                        }
            return self.write(cr, uid, ids, update_state, context=context)
    def set_propose_correction(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id', context=context) :
            return self.write(cr, uid, ids, {'state':'propose_correction'}, context=context)
    
    def set_propose_closing(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id', context=context) :
            return self.write(cr, uid, ids, {'state':'propose_to_close'}, context=context)
    def set_closing_reject(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_bkd', context=context) :
            return self.write(cr, uid, ids, {'state':'confirm'}, context=context)
    def set_closing_approve(self, cr, uid, ids, context=None):
        target_id = len(ids) and ids[0] or False
        task_pool = self.pool.get('project.task')
        if not target_id: return False
        if self.get_auth_id(cr, uid, [target_id],'user_id_bkd', context=context) :
            for target_obj in self.browse(cr, uid, [target_id], context=context):
                task_ids = task_pool.search(cr, uid, [('project_id','=',target_obj.id),('work_state','in',('draft','realisasi'))], context=None)
                task_pool.write(cr, uid, task_ids,  {'work_state':'closed'}, context=None)
                
                update_state = {
                                'state':'closed',
                                }
                return self.write(cr, uid, ids, update_state, context=context)
    
project()




