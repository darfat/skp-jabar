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

class hr_employee(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
        'task_ids': fields.one2many('project.task','employee_id', 'Kegiatan Pegawai', readonly=True),
        'task_apbn_ids': fields.one2many('project.task','employee_id', 'Kegiatan APBN', domain=[('target_type_id','=','dipa_apbn'),('target_period_year','=', time.strftime('%Y')),('target_period_month','=',time.strftime('%m'))], readonly=True),
        'task_biro_ids': fields.one2many('project.task','employee_id', 'Kegiatan Biro', domain=[('target_type_id','=','dpa_opd_biro'),('target_period_year','=', time.strftime('%Y')),('target_period_month','=',time.strftime('%m'))], readonly=True),
        'task_sotk_ids': fields.one2many('project.task','employee_id', 'Kegiatan SOTK', domain=[('target_type_id','=','sotk'),('target_period_year','=', time.strftime('%Y')),('target_period_month','=',time.strftime('%m'))], readonly=True),
        'task_lain_lain_ids': fields.one2many('project.task','employee_id', 'Kegiatan Lain Lain', domain=[('target_type_id','=','lain_lain'),('target_period_year','=', time.strftime('%Y')),('target_period_month','=',time.strftime('%m'))], readonly=True),
        'task_tambahan_ids': fields.one2many('project.task','employee_id', 'Kegiatan Tambahan', domain=[('target_type_id','=','tambahan'),('target_period_year','=', time.strftime('%Y')),('target_period_month','=',time.strftime('%m'))], readonly=True),
        'task_perilaku_ids': fields.one2many('project.task','employee_id', 'Perilaku', domain=[('target_type_id','=','perilaku'),('target_period_year','=', time.strftime('%Y')),('target_period_month','=',time.strftime('%m'))], readonly=True),
        'skp_employee_ids': fields.one2many('skp.employee','employee_id', 'Nilai Satuan Kerja Pegawai', readonly=True),
        
   }
hr_employee()

class skp_employee(osv.osv):
    _name = 'skp.employee'
    def _get_nilai_skp_percent(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_skp = self._get_nilai_skp(cr, uid, [skp_employee_obj.id], field_names, args, context)
            if nilai_skp and nilai_skp.get(skp_employee_obj.id)>0.0:
                res[skp_employee_obj.id] =  nilai_skp.get(skp_employee_obj.id) * 0.6
            else : 
                res[skp_employee_obj.id] =0.0
        return res
    
    def _get_nilai_skp_tambahan_kreatifitas_percent(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_tambahan=0
            nilai_kreatifitas=0
            nilai_skp = self._get_nilai_skp(cr, uid, [skp_employee_obj.id], field_names, args, context)
            if skp_employee_obj.fn_nilai_tambahan and skp_employee_obj.fn_nilai_tambahan>0.0:
                nilai_tambahan =  skp_employee_obj.fn_nilai_tambahan
            if skp_employee_obj.fn_nilai_kreatifitas and skp_employee_obj.fn_nilai_kreatifitas>0.0:
                nilai_kreatifitas =  skp_employee_obj.fn_nilai_kreatifitas
            if nilai_skp and nilai_skp.get(skp_employee_obj.id)>0.0:
                res[skp_employee_obj.id] =  ( nilai_skp.get(skp_employee_obj.id) * 0.6 ) + nilai_tambahan+nilai_kreatifitas
            else : 
                res[skp_employee_obj.id] =0.0
        return res
    
    
    def _get_nilai_perilaku_percent(self, cr, uid, ids, field_names, args, context=None):
        res = {}
       
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_perilaku = self._get_nilai_perilaku(cr, uid, [skp_employee_obj.id], field_names, args, context)
            if nilai_perilaku and nilai_perilaku.get(skp_employee_obj.id)>0.0:
                res[skp_employee_obj.id] =  nilai_perilaku.get(skp_employee_obj.id) * 0.4   
            else : 
                res[skp_employee_obj.id] =0.0
        return res
   
    def _get_nilai_total_old_tanpa_tambahan(self, cr, uid, ids, field_names, args, context=None):
        res = {}
       
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_total=0.0
            nilai_tambahan=0
            nilai_skp = self._get_nilai_skp_percent(cr, uid, [skp_employee_obj.id], field_names, args, context)
            nilai_perilaku = self._get_nilai_perilaku_percent(cr, uid, [skp_employee_obj.id], field_names, args, context)
            if nilai_skp and nilai_skp.get(skp_employee_obj.id)>0.0:
                nilai_total +=  nilai_skp.get(skp_employee_obj.id) 
            if nilai_perilaku and nilai_perilaku.get(skp_employee_obj.id)>0.0:
                nilai_total +=  nilai_perilaku.get(skp_employee_obj.id) 
            
            
            res[skp_employee_obj.id] =nilai_total
        return res
    def _get_nilai_total(self, cr, uid, ids, field_names, args, context=None):
        res = {}
       
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_total=0.0
            nilai_tambahan=0
            nilai_skp = self._get_nilai_skp_tambahan_kreatifitas_percent(cr, uid, [skp_employee_obj.id], field_names, args, context)
            nilai_perilaku = self._get_nilai_perilaku_percent(cr, uid, [skp_employee_obj.id], field_names, args, context)
            if nilai_skp and nilai_skp.get(skp_employee_obj.id)>0.0:
                nilai_total +=  nilai_skp.get(skp_employee_obj.id) 
            if nilai_perilaku and nilai_perilaku.get(skp_employee_obj.id)>0.0:
                nilai_total +=  nilai_perilaku.get(skp_employee_obj.id) 
            
            
            res[skp_employee_obj.id] =nilai_total
        return res
    
    def _get_nilai_tpp(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        rupiah=50
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            tpp=0.0
            
            nilai_tpp = self._get_nilai_total(cr, uid, [skp_employee_obj.id], field_names, args, context)
            
            if nilai_tpp and nilai_tpp.get(skp_employee_obj.id)>0.0:
                tpp =  nilai_tpp.get(skp_employee_obj.id) *rupiah
            res[skp_employee_obj.id] =round(tpp)
        return res
    def _get_fn_nilai_tambahan(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_tambahan=0
            nilai_tambahan = self._get_nilai_task_tambahan(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            res[skp_employee_obj.id] =nilai_tambahan
        return res
    def _get_fn_nilai_kreatifitas(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai_kreatifitas=0
            nilai_kreatifitas = self._get_nilai_task_kreatifitas(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            res[skp_employee_obj.id] =nilai_kreatifitas
        return res
    def _get_jml_task_perilaku(self, cr, uid, user_id,target_period_month,target_period_year,work_state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',work_state),
                                             ('target_type_id','=','perilaku')], context=None)
        if task_ids:
            return len(task_ids)
        return 0;
    def _get_jml_task_skp(self, cr, uid, user_id,target_period_month,target_period_year,work_state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',work_state),
                                             ('target_type_id','in',('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'))], context=None)
        
        if task_ids:
            return len(task_ids)
        return 0;
    def _get_jml_all_task_skp(self, cr, uid, user_id,target_period_month,target_period_year, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','!=','cancelled'),
                                             ('target_type_id','in',('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'))], context=None)
        
        if task_ids:
            return len(task_ids)
        return 0;
    def _get_nilai_task_tambahan(self, cr, uid, user_id,target_period_month,target_period_year,work_state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',work_state),
                                             ('target_type_id','=','tambahan')],
                                                limit=1,order='id desc',context=None)
        task_list = task_pool.read(cr, uid, task_ids, ['nilai_tambahan'], context=context)
        nilai_total =0
        for task_obj in task_list:  
            nilai_total=nilai_total+task_obj['nilai_tambahan']
        return nilai_total;
    def _get_nilai_task_kreatifitas(self, cr, uid, user_id,target_period_month,target_period_year,work_state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',work_state),
                               				('target_type_id','=','tambahan')], 
                                             limit=1,order='id desc',context=None)
        task_list = task_pool.read(cr, uid, task_ids, ['nilai_kreatifitas'], context=context)
        nilai_total =0
        for task_obj in task_list: 
            nilai_total=nilai_total+task_obj['nilai_kreatifitas']
        return nilai_total;
    def _get_nilai_task_perilaku(self, cr, uid, user_id,target_period_month,target_period_year,work_state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',work_state),
                                             ('target_type_id','=','perilaku')],
                                             limit=1,order='id desc',context=None)
        task_list = task_pool.read(cr, uid, task_ids, ['nilai_akhir'], context=context)
        nilai_total =0
        for task_obj in task_list: 
            nilai_total=nilai_total+task_obj['nilai_akhir']
        return nilai_total;
    def _get_nilai_task_skp(self, cr, uid, user_id,target_period_month,target_period_year,work_state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids=task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',work_state),
                                             ('target_type_id','in',('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'))], context=None)
        task_list = task_pool.read(cr, uid, task_ids, ['nilai_akhir'], context=context)
        
        nilai_total =0
        for task_obj in task_list: 
            nilai_total=nilai_total+task_obj['nilai_akhir']
        return nilai_total; 
    def _get_jml_perilaku(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        jml_perilaku=0
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_perilaku = self._get_jml_task_perilaku(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            
            res[skp_employee_obj.id] =jml_perilaku
        return res
    
    def _get_jml_skp(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        jml_skp=0
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_skp = self._get_jml_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            
            res[skp_employee_obj.id] =jml_skp
        return res
    def _get_jml_all_skp(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        jml_skp=0
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_skp = self._get_jml_all_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,context)
            
            res[skp_employee_obj.id] =jml_skp
        return res
    
    def _get_status_nilai_skp(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        status_nilai_skp='Masih Ada Kegiatan Yang Belum Dinilai'
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_skp = self._get_jml_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            jml_semua_skp = self._get_jml_all_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year ,context)
            if jml_skp == jml_semua_skp :
                res[skp_employee_obj.id] = 'Semua Kegiatan Selesai'                
            else :
                res[skp_employee_obj.id] = str(jml_skp)+' / '+str(jml_semua_skp)+' Kegiatan SKP'
        return res
    def _get_nilai_skp(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        nilai_skp=0
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_skp = self._get_jml_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            jml_semua_skp = self._get_jml_all_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year ,context) #jml_skp
            if jml_skp == jml_semua_skp :
                nilai_total_skp = self._get_nilai_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
                if jml_skp > 0 and nilai_total_skp > 0 :
                    nilai_skp = nilai_total_skp/jml_skp;
                    res[skp_employee_obj.id] =nilai_skp 
                else :
                    res[skp_employee_obj.id] = 0
            else :
                res[skp_employee_obj.id] = 0
        return res
    def _get_nilai_skp_sementara(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        nilai_skp=0
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_skp = self._get_jml_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            jml_semua_skp = jml_skp#self._get_jml_all_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year ,context)
            if jml_skp == jml_semua_skp :
                nilai_total_skp = self._get_nilai_task_skp(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
                if jml_skp > 0 and nilai_total_skp > 0 :
                    nilai_skp = nilai_total_skp/jml_skp;
                    res[skp_employee_obj.id] =nilai_skp
                else :
                    res[skp_employee_obj.id] = 0
            else :
                res[skp_employee_obj.id] = 0
        return res
    def _get_nilai_perilaku(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        nilai_perilaku=0
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            jml_perilaku = self._get_jml_task_perilaku(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            nilai_total_perilaku = self._get_nilai_task_perilaku(cr, uid,skp_employee_obj.user_id.id,skp_employee_obj.target_period_month,skp_employee_obj.target_period_year,'done' ,context)
            if jml_perilaku > 0 and nilai_total_perilaku > 0 :
                nilai_perilaku = nilai_total_perilaku/jml_perilaku;
                res[skp_employee_obj.id] =nilai_perilaku
            else :
                res[skp_employee_obj.id] = 0
        return res      
    def _get_indeks_nilai(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        lookup_nilai_pool = self.pool.get('acuan.penailaian')
        for skp_employee_obj in self.browse(cr, uid, ids, context=context):
            nilai = skp_employee_obj.nilai_total
            lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_nilai', '=', 'threshold'), ('active', '=', True), ('type', '=', 'lain_lain')
                                                                , ('code', 'in', ('index_nilai_a','index_nilai_b','index_nilai_c','index_nilai_d','index_nilai_e'))
                                                                ,('nilai_bawah', '<=', nilai), ('nilai_atas', '>=', nilai)], context=None)
            if lookup_nilai_id :
                lookup_nilai_obj = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                res[skp_employee_obj.id] =lookup_nilai_obj.name
            else :
                res[skp_employee_obj.id] =''
        
        return res      
      
    def get_detail_nilai_perilaku(self, cr, uid, user_id,target_period_month,target_period_year,state, context=None):
        
        task_pool = self.pool.get('project.task')
        task_ids =task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_year','=', target_period_year),('target_period_month','=',target_period_month),('work_state','=',state),
                                             ('target_type_id','=','perilaku')],
                                             limit=1,order='id desc',context=None)
        task_list = task_pool.read(cr, uid, task_ids, ['nilai_pelayanan','nilai_disiplin','nilai_komitmen','nilai_integritas','nilai_kerjasama','nilai_kepemimpinan'], context=context)
        nilai_total =0
        for task_obj in task_list: 
            return task_obj['nilai_pelayanan'],task_obj['nilai_disiplin'],task_obj['nilai_komitmen'],task_obj['nilai_integritas'],task_obj['nilai_kerjasama'],task_obj['nilai_kepemimpinan'],
        return 0,0,0,0,0,0;       
    
    _columns = {
         'target_period_year'     : fields.char('Periode Tahun',size=4, required=True),
         'target_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')],'Periode Bulan'
                                                     ),
        'summary_target_type_id': fields.selection([  ('pokok', 'pokok'), 
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')
                                                      ],
                                                      'Jenis Kegiatan',
                                                     ),
        'employee_id': fields.many2one('res.partner', 'Pegawai Yang Dinilai', readonly=True),
        'is_kepala_opd': fields.related('employee_id', 'is_kepala_opd',  type='boolean', string='Kepala OPD', store=True),
        'user_id': fields.many2one('res.users','User Login', readonly=True ),
        'company_id': fields.related('employee_id', 'company_id', relation='res.company', type='many2one', string='OPD', store=False),
        'biro_id': fields.related('employee_id', 'biro_id', relation='hr.employee.biro', type='many2one', string='Biro', store=False),
        'department_id': fields.related('employee_id', 'department_id', relation='hr.department', type='many2one', string='Bidang', store=False),
        'biro_name': fields.related('biro_id', 'name',  type='char', string='Nama Biro', store=False),
        'department_name': fields.related('department_id', 'name',  type='char', string='Nama Bidang', store=False),
        
        'nilai_dipa_apbn': fields.float( 'DIPA APBN',readonly=True),
        'nilai_dipa_apbn': fields.float( 'DIPA APBN',readonly=True),
        'nilai_dpa_biro': fields.float( 'DPA  OPD/BIRO',readonly=True),
        'nilai_sotk': fields.float( 'SOTK OPD/BIRO',readonly=True),
        'nilai_lain_lain': fields.float( 'Lain Lain',readonly=True),
        'jml_dipa_apbn': fields.float( 'Jumlah Kegiatan DIPA APBN',readonly=True),
        'jml_dpa_biro': fields.float( 'Jumlah Kegiatan DPA OPD/BIRO',readonly=True),
        'jml_sotk': fields.float( 'Jumlah Kegiatan SOTK',readonly=True),
        'jml_lain_lain': fields.float( 'Jumlah Kegiatan Lain-Lain',readonly=True),
        'nilai_tambahan': fields.float( 'Tambahan ',readonly=True),
        'nilai_kreatifitas': fields.float( 'Kreatifitas',readonly=True),
        'nilai_kepemimpinan': fields.float( 'Kepemimpinan',readonly=True),
        'nilai_kerjasama': fields.float( 'Kerjasama',readonly=True),
        'nilai_integritas': fields.float( 'Integritas',readonly=True),
        'nilai_komitmen': fields.float( 'Komitmen',readonly=True),
        'nilai_disiplin': fields.float( 'Disiplin',readonly=True),
        'nilai_pelayanan': fields.float( 'Pelayanan',readonly=True),
        
        'jumlah_perhitungan': fields.float( 'Jumlah Perhitungan',readonly=True),
        'nilai_akhir': fields.float( 'Nilai',readonly=True),
        
        'skp_state_count': fields.function(_get_status_nilai_skp, string='Jml Kegiatan Yg Sudah Dinilai', type='char', help="Status Nilai SKP",
            store = False),
        'jml_skp': fields.function(_get_jml_skp, string='Jumlah SKP', type='integer', help="Jumlah SKP",
            store = False),
        'jml_all_skp': fields.function(_get_jml_all_skp, string='Jumlah Semua SKP', type='integer', help="Jumlah SKP",
            store = False),
        'jml_perilaku': fields.function(_get_jml_perilaku, string='Jumlah Perilaku', type='integer', help="Jumlah SKP",
            store = False),
     
        'nilai_skp': fields.function(_get_nilai_skp, string='Nilai SKP', type='float', help="Nilai SKP Akan Muncul Apabila Semua Kegiatan Dibulan Tertentu Sudah Selesai Dinilai",
            store = False),
        'nilai_skp_percent': fields.function(_get_nilai_skp_percent, string='Nilai SKP(%)', type='float', help="60% Dari Kegiatan DPA Biro, APBN, SOTK",
            store = False),
        'nilai_skp_tambahan_percent': fields.function(_get_nilai_skp_tambahan_kreatifitas_percent, string='Nilai SKP(%)+TB+Kreatifitas', type='float', help="60% Dari Kegiatan DPA Biro, APBN, SOTK",
            store = False),
        'nilai_perilaku': fields.function(_get_nilai_perilaku, string='Nilai Perilaku', type='float', help="40% Kontribusi untuk nilai perilaku",
            store = False),
        'nilai_perilaku_percent': fields.function(_get_nilai_perilaku_percent, string='Nilai Perilaku(%)', type='float', help="40% Kontribusi untuk nilai perilaku",
            store = False),
        'fn_nilai_tambahan': fields.function(_get_fn_nilai_tambahan, string='Nilai Tambahan', type='float', help="Nilai Tambahan",
            store = False),
        'fn_nilai_kreatifitas': fields.function(_get_fn_nilai_kreatifitas, string='Nilai Kreatifitas', type='float', help="Nilai Kreatifitas",
            store = False),
                
        'nilai_total': fields.function(_get_nilai_total, string='Nilai Total (%)', type='float', help="60% SKP + maks 2, Nilai Tambahan + 40% perilaku",
            store = False),
       
        'nilai_tpp': fields.function(_get_nilai_tpp, string='TPP', type='float', help="TPP",
            store = False),
        'nilai_indeks': fields.function(_get_indeks_nilai, string='Indeks Nilai', type='char', help="Indeks Nilai",
            store = False),
   }
skp_employee()




