# -*- encoding: utf-8 -*-
##############################################################################
#
#    
#    Darmawan Fatriananda
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
import decimal_precision as dp
from datetime import datetime, timedelta
import time
from mx import DateTime
from openerp.tools import html_email_clean
from openerp.addons.base_status.base_stage import base_stage
from openerp.addons.resource.faces import task as Task

class notification_delete_task(osv.osv_memory):
    _name = "notification.delete.task"
    _columns = {
        'name': fields.char('Notif', size=128),
    }
# ====================== task ================================= #
class task(base_stage, osv.osv):
    _inherit = "project.task"
    _description = "Kegiatan Per Bulan"
    

    
    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            task_id = task_obj.id
            if not task_obj.project_state :
                if uid != 1:
                    if task_obj.work_state in ('draft', 'realisasi', 'rejected_manager'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id', context=context):
                            return False
                    if task_obj.work_state in ('propose', 'rejected_bkd'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context):
                            return False
                    if task_obj.work_state in ('appeal'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_banding', context=context):
                            return False
                    if task_obj.work_state in ('evaluated'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context):
                            return False
                    if task_obj.work_state in ('done', 'cancelled'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context):
                            return False
            elif  task_obj.project_state == 'confirm' :   
                if uid != 1:
                    if task_obj.work_state in ('draft', 'realisasi', 'rejected_manager'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id', context=context):
                            return False
                    if task_obj.work_state in ('propose', 'rejected_bkd'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context):
                            return False
                    if task_obj.work_state in ('appeal'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_banding', context=context):
                            return False
                    if task_obj.work_state in ('evaluated'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context):
                            return False
                    if task_obj.work_state in ('done', 'cancelled'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context):
                            return False
            elif  task_obj.project_state == 'closed' :   
                if uid != 1:
                    if task_obj.work_state in ('draft', 'realisasi', 'rejected_manager'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id', context=context):
                            return False
                    if task_obj.work_state in ('propose', 'rejected_bkd'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context):
                            return False
                    if task_obj.work_state in ('appeal'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_banding', context=context):
                            return False
                    if task_obj.work_state in ('evaluated'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context):
                            return False
                    if task_obj.work_state in ('done', 'cancelled','closed'):
                        if not self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context):
                            return False
        super(task, self).write(cr, uid, ids, vals, context=context)           
        return True
    def _progress_by_stage(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        if not ids:
            return res
        for task in self.browse(cr, uid, ids, context=context):
            if task.work_state in ('draft'):
                res[task.id] = 0.0
            if task.work_state in ('realisasi'):
                res[task.id] = 20.0
            if task.work_state in ('propose'):
                res[task.id] = 60.0
            if task.work_state in ('rejected_manager'):
                res[task.id] = 30.0
            if task.work_state in ('appeal'):
                res[task.id] = 50.0
            if task.work_state in ('evaluated'):
                res[task.id] = 85.0
            if task.work_state in ('rejected_bkd'):
                res[task.id] = 70.0
            if task.work_state in ('done', 'cancelled','closed'):
                res[task.id] = 100.0
            else :
                res[task.id] = 0.0
        return res
    def _get_status_project_not_exist(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        else : #deactive 
            return res;
        #print "_get_status_project_not_exist"
        for target in self.browse(cr, uid, ids, context=context):
            res[target.id] = False
            target_realiasi_notsame = False
            if target.work_state == 'evaluated' and target.task_category == 'skp':
                 if not target.project_id  :
                    target_realiasi_notsame = True
                 elif target.project_id and target.project_state != 'confirm' :
                    target_realiasi_notsame = True
                 res[target.id] = target_realiasi_notsame
        return res 
    def _get_status_target_realiasi_notsame(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        #print "_get_status_target_realiasi_notsame"
        for target in self.browse(cr, uid, ids, context=context):
            res[target.id] = False
            target_realiasi_notsame = False
            if target.work_state == 'evaluated' and target.task_category == 'skp':
                 if target.nilai_sementara and target.nilai_sementara >100 :
                     res[target.id] = False
                     return res
		         
                 if target.target_jumlah_kuantitas_output > target.realisasi_jumlah_kuantitas_output :
		            target_realiasi_notsame = True
                 if target.target_kualitas != 0 and target.target_kualitas > target.realisasi_kualitas :
		            target_realiasi_notsame = True
                 if target.target_waktu > target.realisasi_waktu :
		            target_realiasi_notsame = True
                 if target.target_biaya > target.realisasi_biaya :
		            target_realiasi_notsame = True
		         
                 res[target.id] = target_realiasi_notsame
        return res 
    def _get_status_suggest_realiasi_notsame(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        
        for target in self.browse(cr, uid, ids, context=context):
            res[target.id] = False
            suggest_realiasi_notsame = False
            if target.suggest_jumlah_kuantitas_output != 0 and target.suggest_jumlah_kuantitas_output != target.target_jumlah_kuantitas_output :
                suggest_realiasi_notsame = True
            if target.suggest_kualitas != 0 and target.suggest_kualitas != target.target_kualitas :
                suggest_realiasi_notsame = True
            if target.suggest_waktu != 0 and target.suggest_waktu != target.target_waktu :
                suggest_realiasi_notsame = True
            if target.suggest_biaya != 0 and target.suggest_biaya != target.target_biaya :
                suggest_realiasi_notsame = True
            res[target.id] = suggest_realiasi_notsame
            # print "target_jumlah_kuantitas_output_notsame : ",target_jumlah_kuantitas_output_notsame 
        return res 
    def _get_employee_from_user(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        if not ids:
            return res
        #print "_get_employee_from_user"
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
    def _get_status_biaya_verifikasi_notsame(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        #print "_get_status_biaya_verifikasi_notsame"
        for task_obj in self.browse(cr, uid, ids, context=context):
            res[task_obj.id] = False
            isNotSame = False
            if task_obj.work_state == 'evaluated' and task_obj.target_type_id in ('dipa_apbn','dpa_opd_biro','sotk','lain_lain') :
                if task_obj.realisasi_biaya != 0 and task_obj.realisasi_biaya != task_obj.target_biaya :
                    isNotSame = True
           
            res[task_obj.id] = isNotSame #Sementara;
            # print "target_jumlah_kuantitas_output_notsame : ",target_jumlah_kuantitas_output_notsame 
        return res 
    def _get_status_komitmen_verifikasi_notsame(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        #print "_get_status_komitmen_verifikasi_notsame"
        for task_obj in self.browse(cr, uid, ids, context=context):
            res[task_obj.id] = False
            isNotSame = False
            if task_obj.work_state == 'evaluated' :
                if task_obj.realisasi_hadir_apel_pagi < task_obj.realisasi_apel_pagi :
                    isNotSame = True
                if  task_obj.realisasi_hadir_hari_kerja < task_obj.realisasi_jumlah_hari_kerja :
                    isNotSame = True
                if  task_obj.realisasi_hadir_jam_kerja < task_obj.realisasi_jumlah_jam_kerja :
                    isNotSame = True
                if task_obj.realisasi_hadir_upacara_hari_besar < task_obj.realisasi_upacara_hari_besar :
                    isNotSame = True
           
            res[task_obj.id] = isNotSame
            # print "target_jumlah_kuantitas_output_notsame : ",target_jumlah_kuantitas_output_notsame 
        return res
    _columns = {
        'target_type_id': fields.selection([ ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),
                                            ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang Sotk Opd/Biro'),
                                                      ('lain_lain', 'Lain-Lain'),
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')], 'Jenis Kegiatan', required=True
                                                     ),
        'task_category': fields.selection([('skp', 'SKP'), ('non_skp', 'Perilaku, Tambahan dan Kreatifitas')], 'Kategori Kegiatan', required=True),
        'target_category': fields.selection([('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')], 'Kategori', required=True),
        'code'     : fields.char('Kode Kegiatan', size=20,),
        'target_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')], 'Periode Bulan'
                                                     ),
        'work_state': fields.selection([('draft', 'Draft'), ('realisasi', 'Realisasi'),
                                        ('propose', 'Atasan'), ('rejected_manager', 'Pengajuan Ditolak Atasan'),
                                        ('appeal', 'Banding'), ('evaluated', 'BKD'), ('rejected_bkd', 'Pengajuan Ditolak BKD'),
                                        ('propose_to_close','Pengajuan Closing Target'),('closed','Closed'),
                                        ('done', 'Selesai'), ('cancelled', 'Cancel')], 'Status Pekerjaan'),
        'target_period_year'     : fields.char('Periode Tahun', size=4, required=True),
        'target_jumlah_kuantitas_output'     : fields.integer('Kuantitas Output', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'target_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output', readonly=True, states={'draft': [('readonly', False)]}),
        'target_angka_kredit'     : fields.float('Angka Kredit', digits_compute=dp.get_precision('angka_kredit')),
        'target_kualitas'     : fields.float('Kualitas', digits_compute=dp.get_precision('no_digit'), required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'target_waktu'     : fields.integer('Waktu', required=True, readonly=True, states={'draft': [('readonly', False)]}),
        'target_satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1, readonly=True, states={'draft': [('readonly', False)]}),
        'target_biaya'     : fields.float('Biaya', readonly=True, states={'draft': [('readonly', False)]}),
        'target_lainlain'     : fields.integer('Lain-Lain', readonly=True, states={'draft': [('readonly', False)]}),
        'target_tugas_tambahan'     : fields.integer('Tugas Tambahan', readonly=True, states={'draft': [('readonly', False)]}),
        'target_nilai_kreatifitas'     : fields.integer('Nilai Kreatifitas', readonly=True, states={'draft': [('readonly', False)]}),
        'target_jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Konsumen Pelayanan', readonly=True, states={'draft': [('readonly', False)]}),
        'target_satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen', readonly=True, states={'draft': [('readonly', False)]}),
        'target_apel_pagi'     : fields.integer('Jumlah Apel Pagi', readonly=True, states={'draft': [('readonly', False)]}),
        'target_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar', readonly=True, states={'draft': [('readonly', False)]}),
        'target_integritas_presiden': fields.boolean('Presiden', readonly=True, states={'draft': [('readonly', False)]}),
        'target_integritas_gubernur': fields.boolean('Gubernur', readonly=True, states={'draft': [('readonly', False)]}),
        'target_integritas_kepalaopd': fields.boolean('Kepala OPD', readonly=True, states={'draft': [('readonly', False)]}),
        'target_integritas_atasan': fields.boolean('Atasan Langsung', readonly=True, states={'draft': [('readonly', False)]}),
        'target_integritas_lainlain': fields.boolean('Lain Lain', readonly=True, states={'draft': [('readonly', False)]}),
        'target_hadir_hari_kerja'     : fields.integer('Kehadiran Kerja', readonly=True, states={'draft': [('readonly', False)]}),
        'target_hadir_jam_kerja': fields.integer('Jumlah Jam Kerja', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kerjasama_nasional': fields.boolean('Nasional', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kerjasama_gubernur': fields.boolean('Provinsi', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kerjasama_kepalaopd': fields.boolean('OPD', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kerjasama_atasan': fields.boolean('Atasan Langsung', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kerjasama_lainlain': fields.boolean('Lain Lain', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kepemimpinan_nasional': fields.boolean('Nasional', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kepemimpinan_gubernur': fields.boolean('Provinsi', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kepemimpinan_kepalaopd': fields.boolean('OPD', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kepemimpinan_atasan': fields.boolean('Atasan Langsung', readonly=True, states={'draft': [('readonly', False)]}),
        'target_kepemimpinan_lainlain': fields.boolean('Lain Lain', readonly=True, states={'draft': [('readonly', False)]}),
        # 'realisasi_type_id': fields.many2one('project.type', 'Jenis', required=True),
        # 'realisasi_category': fields.selection([('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')], 'Kategori', required=True),
        'realisasi_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')], 'Periode Bulan'
                                                     ),
        'realisasi_period_year'     : fields.char('Periode Tahun', size=4),
        'realisasi_jumlah_kuantitas_output'     : fields.integer('Kuantitas Output'),
        'realisasi_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output'),
        'realisasi_angka_kredit'     : fields.float('Angka Kredit', digits_compute=dp.get_precision('angka_kredit')),
        'realisasi_kualitas'     : fields.float('Kualitas', digits_compute=dp.get_precision('no_digit')),
        'realisasi_waktu'     : fields.integer('Waktu'),
        'realisasi_satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1),
        'realisasi_biaya'     : fields.float('Biaya'),
        'realisasi_lainlain'     : fields.integer('Lain-Lain'),
        'realisasi_tugas_tambahan'     : fields.integer('Jumlah Tugas Tambahan'),
        'realisasi_uraian_tugas_tambahan'     : fields.text('Uraian Tugas Tambahan'),
        'realisasi_rl_presiden_tugas_tambahan'     : fields.boolean('Presiden'),
        'realisasi_rl_gubernur_tugas_tambahan'     : fields.boolean('Gubernur'),
        'realisasi_rl_opd_tugas_tambahan'     : fields.boolean('Kepala OPD'),
        'realisasi_attach_tugas_tambahan'              : fields.binary('SK/SP/ST'),
        'realisasi_nilai_kreatifitas'     : fields.integer('Jumlah Kreatifitas'),
        'realisasi_uraian_kreatifitas'     : fields.text('Uraian Kreatifitas'),
        'realisasi_attach_kreatifitas'              : fields.binary('Bukti Pengakuan'),
        'realisasi_tupoksi_kreatifitas': fields.boolean('Tupoksi'),
        'realisasi_rl_presiden_kreatifitas'     : fields.boolean('Presiden'),
        'realisasi_rl_gubernur_kreatifitas'     : fields.boolean('Gubernur'),
        'realisasi_rl_opd_kreatifitas'     : fields.boolean('Kepala OPD'),
        'realisasi_jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Pelayanan'),
        'realisasi_jumlah_tidakpuas_pelayanan'     : fields.integer('Jumlah Ketidakpuasan Pelayanan'),
        'realisasi_satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen'),
        'realisasi_ketepatan_laporan_spj'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan SPJ', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_spj'),('active', '=', True)] ),
        'realisasi_ketepatan_laporan_ukp4'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan UKP4', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_ukp4'),('active', '=', True)] ), 
        'realisasi_efisiensi_biaya_operasional'     : fields.many2one('acuan.penailaian', 'Efisiensi Biaya Operasional Kantor', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'efisiensi_biaya_operasional'),('active', '=', True)] ),
        'realisasi_apel_pagi'     : fields.integer('Jumlah Apel Pagi'),
        'realisasi_hadir_apel_pagi'     : fields.integer('Kehadiran Apel Pagi'),
        'realisasi_upacara_hari_besar': fields.integer('Upacara Hari Besar'),
        'realisasi_integritas_presiden': fields.boolean('Presiden'),
        'realisasi_integritas_gubernur': fields.boolean('Gubernur'),
        'realisasi_integritas_kepalaopd': fields.boolean('Kepala OPD'),
        'realisasi_integritas_atasan': fields.boolean('Atasan Langsung'),
        'realisasi_integritas_lainlain': fields.boolean('Lain Lain'),
        'realisasi_integritas_es1': fields.boolean('Pejabat Eselon I'),
        'realisasi_integritas_es2': fields.boolean('Pejabat Eselon II'),
        'realisasi_integritas_es3': fields.boolean('Pejabat Eselon III'),
        'realisasi_integritas_es4': fields.boolean('Pejabat Eselon IV'),
        'realisasi_integritas_hukuman': fields.selection([('ya', 'Terkena Hukuman Disiplin'), ('tidak', 'Tidak Terkena Hukuman Disiplin')],'Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Atau Tidak "),#fields.boolean('Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Ceklis Di Kotak Ini "),
        'realisasi_integritas_hukuman_ringan': fields.boolean('Ringan'),
        'realisasi_integritas_hukuman_sedang': fields.boolean('Sedang'),
        'realisasi_integritas_hukuman_berat': fields.boolean('Berat'),
        'realisasi_hadir_hari_kerja'     : fields.integer('Kehadiran Hari Kerja'),
        'realisasi_hadir_jam_kerja': fields.integer('Kehadiran Jam Kerja'),
        'realisasi_jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja'),
        'realisasi_jumlah_jam_kerja': fields.integer('Jumlah Jam Kerja'),
        'realisasi_hadir_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'realisasi_kerjasama_nasional': fields.boolean('Nasional'),
        'realisasi_kerjasama_gubernur': fields.boolean('Provinsi'),
        'realisasi_kerjasama_kepalaopd': fields.boolean('OPD'),
        'realisasi_kerjasama_atasan': fields.boolean('Atasan Langsung'),
        'realisasi_kerjasama_lainlain': fields.boolean('Lain Lain'),
        'realisasi_kerjasama_rapat_atasan': fields.boolean('Rapat Atasan Langsung'),
        'realisasi_kerjasama_rapat_perangkat_daerah': fields.boolean('Rapat Perangkat Daerah'),
        'realisasi_kerjasama_rapat_provinsi': fields.boolean('Rapat Provinsi'),
        'realisasi_kerjasama_rapat_nasional': fields.boolean('Rapat Nasional'),
        'realisasi_kepemimpinan_nasional': fields.boolean('Nasional'),
        'realisasi_kepemimpinan_gubernur': fields.boolean('Provinsi'),
        'realisasi_kepemimpinan_kepalaopd': fields.boolean('OPD'),
        'realisasi_kepemimpinan_atasan': fields.boolean('Atasan Langsung'),
        'realisasi_kepemimpinan_lainlain': fields.boolean('Lain Lain'),
        'realisasi_kepemimpinan_narsum_unitkerja': fields.boolean('Narasumber Kerja Atasan Langsung'),
        'realisasi_kepemimpinan_narsum_perangkat_daerah': fields.boolean('Narasumber Perangkat Daerah'),
        'realisasi_kepemimpinan_narsum_provinsi': fields.boolean('Narasumber Provinsi'),
        'realisasi_kepemimpinan_narsum_nasional': fields.boolean('Narasumber Nasional'),
        'user_id_atasan': fields.many2one('res.users', 'Pejabat Penilai',),
        'user_id_banding': fields.many2one('res.users', 'Atasan Pejabat Penilai',),
        'user_id_bkd': fields.many2one('res.users', 'Pejabat Pengevaluasi (BKD)',),
        'notes'     : fields.text('Catatan', states={'draft': [('required', False)]}),
        'notes_from_bkd'     : fields.text('Catatan Petugas Verifikasi', ),
        'attachment_1'              : fields.binary('Lampiran'),
        'attachment_2'              : fields.binary('Lampiran 2'),
        'attachment_3'              : fields.binary('Lampiran 3'),
        'is_suggest': fields.boolean('Tambahkan Koreski Penilaian'),
        'is_appeal': fields.boolean('Tambahkan Koreski Banding'),
        'is_control': fields.boolean('Verifikasi Penilaian'),
        'is_verificated': fields.boolean('Verifikasi Diterima'),
        
        'suggest_jumlah_kuantitas_output'     : fields.integer('Kuantitas Output', readonly=False),
        'suggest_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output', readonly=False),
        'suggest_angka_kredit'     : fields.float('Angka Kredit', digits_compute=dp.get_precision('angka_kredit'), readonly=False),
        'suggest_kualitas'     : fields.float('Kualitas', digits_compute=dp.get_precision('no_digit'), readonly=False),
        'suggest_waktu'     : fields.integer('Waktu', readonly=False),
        'suggest_satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1, readonly=False),
        'suggest_biaya'     : fields.float('Biaya', readonly=False),
        'suggest_lainlain'     : fields.integer('Lain-Lain', readonly=False),
        'suggest_tugas_tambahan'     : fields.integer('Jumlah Tugas Tambahan'),
        'suggest_uraian_tugas_tambahan'     : fields.text('Uraian Tugas Tambahan'),
        'suggest_rl_presiden_tugas_tambahan'     : fields.boolean('Presiden'),
        'suggest_rl_gubernur_tugas_tambahan'     : fields.boolean('Gubernur'),
        'suggest_rl_opd_tugas_tambahan'     : fields.boolean('Kepala OPD'),
        'suggest_attach_tugas_tambahan'              : fields.binary('SK/SP/ST'),
        'suggest_nilai_kreatifitas'     : fields.integer('Jumlah Kreatifitas'),
        'suggest_uraian_kreatifitas'     : fields.text('Uraian Kreatifitas'),
        'suggest_attach_kreatifitas'              : fields.binary('Bukti Pengakuan'),
        'suggest_tupoksi_kreatifitas': fields.boolean('Tupoksi'),
        'suggest_rl_presiden_kreatifitas'     : fields.boolean('Presiden'),
        'suggest_rl_gubernur_kreatifitas'     : fields.boolean('Gubernur'),
        'suggest_rl_opd_kreatifitas'     : fields.boolean('Kepala OPD'),
        'suggest_jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Pelayanan'),
        'suggest_jumlah_tidakpuas_pelayanan'     : fields.integer('Jumlah Ketidakpuasan Pelayanan'),
        'suggest_satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen'),
        'suggest_ketepatan_laporan_spj'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan SPJ', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_spj'),('active', '=', True)] ),
        'suggest_ketepatan_laporan_ukp4'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan UKP4', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_ukp4'),('active', '=', True)] ), 
        'suggest_efisiensi_biaya_operasional'     : fields.many2one('acuan.penailaian', 'Efisiensi Biaya Operasional Kantor', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'efisiensi_biaya_operasional'),('active', '=', True)] ),
        'suggest_apel_pagi'     : fields.integer('Jumlah Apel Pagi'),
        'suggest_hadir_apel_pagi'     : fields.integer('Kehadiran Apel Pagi'),
        'suggest_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'suggest_integritas_presiden': fields.boolean('Presiden'),
        'suggest_integritas_gubernur': fields.boolean('Gubernur'),
        'suggest_integritas_kepalaopd': fields.boolean('Kepala OPD'),
        'suggest_integritas_atasan': fields.boolean('Atasan Langsung'),
        'suggest_integritas_lainlain': fields.boolean('Lain Lain'),
        'suggest_integritas_es1': fields.boolean('Pejabat Eselon I'),
        'suggest_integritas_es2': fields.boolean('Pejabat Eselon II'),
        'suggest_integritas_es3': fields.boolean('Pejabat Eselon III'),
        'suggest_integritas_es4': fields.boolean('Pejabat Eselon IV'),
        'suggest_integritas_hukuman': fields.selection([('ya', 'Terkena Hukuman Disiplin'), ('tidak', 'Tidak Terkena Hukuman Disiplin')],'Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Atau Tidak "),
        'suggest_integritas_hukuman_ringan': fields.boolean('Ringan'),
        'suggest_integritas_hukuman_sedang': fields.boolean('Sedang'),
        'suggest_integritas_hukuman_berat': fields.boolean('Berat'),
        'suggest_hadir_hari_kerja'     : fields.integer('Kehadiran Hari Kerja'),
        'suggest_hadir_jam_kerja': fields.integer('Kehadiran Jam Kerja'),
        'suggest_jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja'),
        'suggest_jumlah_jam_kerja': fields.integer('Jumlah Jam Kerja'),
        'suggest_hadir_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'suggest_kerjasama_nasional': fields.boolean('Nasional'),
        'suggest_kerjasama_gubernur': fields.boolean('Provinsi'),
        'suggest_kerjasama_kepalaopd': fields.boolean('OPD'),
        'suggest_kerjasama_atasan': fields.boolean('Atasan Langsung'),
        'suggest_kerjasama_lainlain': fields.boolean('Lain Lain'),
        'suggest_kerjasama_rapat_atasan': fields.boolean('Rapat Atasan Langsung'),
        'suggest_kerjasama_rapat_perangkat_daerah': fields.boolean('Rapat Perangkat Daerah'),
        'suggest_kerjasama_rapat_provinsi': fields.boolean('Rapat Provinsi'),
        'suggest_kerjasama_rapat_nasional': fields.boolean('Rapat Nasional'),
        'suggest_kepemimpinan_nasional': fields.boolean('Nasional'),
        'suggest_kepemimpinan_gubernur': fields.boolean('Provinsi'),
        'suggest_kepemimpinan_kepalaopd': fields.boolean('OPD'),
        'suggest_kepemimpinan_atasan': fields.boolean('Atasan Langsung'),
        'suggest_kepemimpinan_lainlain': fields.boolean('Lain Lain'),
        'suggest_kepemimpinan_narsum_unitkerja': fields.boolean('Narasumber Kerja Atasan Langsung'),
        'suggest_kepemimpinan_narsum_perangkat_daerah': fields.boolean('Narasumber Perangkat Daerah'),
        'suggest_kepemimpinan_narsum_provinsi': fields.boolean('Narasumber Provinsi'),
        'suggest_kepemimpinan_narsum_nasional': fields.boolean('Narasumber Nasional'),
        
        'appeal_jumlah_kuantitas_output'     : fields.integer('Kuantitas Output'),
        'appeal_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output'),
        'appeal_angka_kredit'     : fields.float('Angka Kredit', digits_compute=dp.get_precision('angka_kredit')),
        'appeal_kualitas'     : fields.float('Kualitas', digits_compute=dp.get_precision('no_digit')),
        'appeal_waktu'     : fields.integer('Waktu'),
        'appeal_satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1),
        'appeal_biaya'     : fields.float('Biaya'),
        'appeal_lainlain'     : fields.integer('Lain-Lain'),
        'appeal_tugas_tambahan'     : fields.integer('Jumlah Tugas Tambahan'),
        'appeal_uraian_tugas_tambahan'     : fields.text('Uraian Tugas Tambahan'),
        'appeal_rl_presiden_tugas_tambahan'     : fields.boolean('Presiden'),
        'appeal_rl_gubernur_tugas_tambahan'     : fields.boolean('Gubernur'),
        'appeal_rl_opd_tugas_tambahan'     : fields.boolean('Kepala OPD'),
        'appeal_attach_tugas_tambahan'              : fields.binary('SK/SP/ST'),
        'appeal_nilai_kreatifitas'     : fields.integer('Jumlah Kreatifitas'),
        'appeal_uraian_kreatifitas'     : fields.text('Uraian Kreatifitas'),
        'appeal_attach_kreatifitas'              : fields.binary('Bukti Pengakuan'),
        'appeal_tupoksi_kreatifitas': fields.boolean('Tupoksi'),
        'appeal_rl_presiden_kreatifitas'     : fields.boolean('Presiden'),
        'appeal_rl_gubernur_kreatifitas'     : fields.boolean('Gubernur'),
        'appeal_rl_opd_kreatifitas'     : fields.boolean('Kepala OPD'),
        'appeal_jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Pelayanan'),
        'appeal_jumlah_tidakpuas_pelayanan'     : fields.integer('Jumlah Ketidakpuasan Pelayanan'),
        'appeal_satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen'),
        'appeal_ketepatan_laporan_spj'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan SPJ', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_spj'),('active', '=', True)] ),
        'appeal_ketepatan_laporan_ukp4'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan UKP4', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_ukp4'),('active', '=', True)] ), 
        'appeal_efisiensi_biaya_operasional'     : fields.many2one('acuan.penailaian', 'Efisiensi Biaya Operasional Kantor', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'efisiensi_biaya_operasional'),('active', '=', True)] ),
        'appeal_apel_pagi'     : fields.integer('Jumlah Apel Pagi'),
        'appeal_hadir_apel_pagi'     : fields.integer('Kehadiran Apel Pagi'),
        'appeal_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'appeal_integritas_presiden': fields.boolean('Presiden'),
        'appeal_integritas_gubernur': fields.boolean('Gubernur'),
        'appeal_integritas_kepalaopd': fields.boolean('Kepala OPD'),
        'appeal_integritas_atasan': fields.boolean('Atasan Langsung'),
        'appeal_integritas_lainlain': fields.boolean('Lain Lain'),
        'appeal_integritas_es1': fields.boolean('Pejabat Eselon I'),
        'appeal_integritas_es2': fields.boolean('Pejabat Eselon II'),
        'appeal_integritas_es3': fields.boolean('Pejabat Eselon III'),
        'appeal_integritas_es4': fields.boolean('Pejabat Eselon IV'),
        'appeal_integritas_hukuman': fields.selection([('ya', 'Terkena Hukuman Disiplin'), ('tidak', 'Tidak Terkena Hukuman Disiplin')],'Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Atau Tidak "),
        'appeal_integritas_hukuman_ringan': fields.boolean('Ringan'),
        'appeal_integritas_hukuman_sedang': fields.boolean('Sedang'),
        'appeal_integritas_hukuman_berat': fields.boolean('Berat'),
        'appeal_hadir_hari_kerja'     : fields.integer('Kehadiran Hari Kerja'),
        'appeal_hadir_jam_kerja': fields.integer('Kehadiran Jam Kerja'),
        'appeal_jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja'),
        'appeal_jumlah_jam_kerja': fields.integer('Jumlah Jam Kerja'),
        'appeal_hadir_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'appeal_kerjasama_nasional': fields.boolean('Nasional'),
        'appeal_kerjasama_gubernur': fields.boolean('Provinsi'),
        'appeal_kerjasama_kepalaopd': fields.boolean('OPD'),
        'appeal_kerjasama_atasan': fields.boolean('Atasan Langsung'),
        'appeal_kerjasama_lainlain': fields.boolean('Lain Lain'),
        'appeal_kerjasama_rapat_atasan': fields.boolean('Rapat Atasan Langsung'),
        'appeal_kerjasama_rapat_perangkat_daerah': fields.boolean('Rapat Perangkat Daerah'),
        'appeal_kerjasama_rapat_provinsi': fields.boolean('Rapat Provinsi'),
        'appeal_kerjasama_rapat_nasional': fields.boolean('Rapat Nasional'),
        'appeal_kepemimpinan_nasional': fields.boolean('Nasional'),
        'appeal_kepemimpinan_gubernur': fields.boolean('Provinsi'),
        'appeal_kepemimpinan_kepalaopd': fields.boolean('OPD'),
        'appeal_kepemimpinan_atasan': fields.boolean('Atasan Langsung'),
        'appeal_kepemimpinan_lainlain': fields.boolean('Lain Lain'),
        'appeal_kepemimpinan_narsum_unitkerja': fields.boolean('Narasumber Kerja Atasan Langsung'),
        'appeal_kepemimpinan_narsum_perangkat_daerah': fields.boolean('Narasumber Perangkat Daerah'),
        'appeal_kepemimpinan_narsum_provinsi': fields.boolean('Narasumber Provinsi'),
        'appeal_kepemimpinan_narsum_nasional': fields.boolean('Narasumber Nasional'),
        
        'control_jumlah_kuantitas_output'     : fields.integer('Kuantitas Output'),
        'control_satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output'),
        'control_angka_kredit'     : fields.float('Angka Kredit', digits_compute=dp.get_precision('angka_kredit')),
        'control_kualitas'     : fields.float('Kualitas', digits_compute=dp.get_precision('no_digit')),
        'control_waktu'     : fields.integer('Waktu'),
        'control_satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1),
        'control_biaya'     : fields.float('Biaya'),
        'control_lainlain'     : fields.integer('Lain-Lain'),
        'control_tugas_tambahan'     : fields.integer('Jumlah Tugas Tambahan'),
        'control_uraian_tugas_tambahan'     : fields.text('Uraian Tugas Tambahan'),
        'control_rl_presiden_tugas_tambahan'     : fields.boolean('Presiden'),
        'control_rl_gubernur_tugas_tambahan'     : fields.boolean('Gubernur'),
        'control_rl_opd_tugas_tambahan'     : fields.boolean('Kepala OPD'),
        'control_attach_tugas_tambahan'              : fields.binary('SK/SP/ST'),
        'control_nilai_kreatifitas'     : fields.integer('Jumlah Kreatifitas'),
        'control_uraian_kreatifitas'     : fields.text('Uraian Kreatifitas'),
        'control_attach_kreatifitas'              : fields.binary('Bukti Pengakuan'),
        'control_tupoksi_kreatifitas': fields.boolean('Tupoksi'),
        'control_rl_presiden_kreatifitas'     : fields.boolean('Presiden'),
        'control_rl_gubernur_kreatifitas'     : fields.boolean('Gubernur'),
        'control_rl_opd_kreatifitas'     : fields.boolean('Kepala OPD'),
        'control_jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Pelayanan'),
        'control_jumlah_tidakpuas_pelayanan'     : fields.integer('Jumlah Ketidakpuasan Pelayanan'),
        'control_satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen'),
        'control_ketepatan_laporan_spj'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan SPJ', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_spj'),('active', '=', True)] ),
        'control_ketepatan_laporan_ukp4'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan UKP4', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_ukp4'),('active', '=', True)] ), 
        'control_efisiensi_biaya_operasional'     : fields.many2one('acuan.penailaian', 'Efisiensi Biaya Operasional Kantor', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'efisiensi_biaya_operasional'),('active', '=', True)] ),
        'control_apel_pagi'     : fields.integer('Jumlah Apel Pagi'),
        'control_hadir_apel_pagi'     : fields.integer('Kehadiran Apel Pagi'),
        'control_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'control_integritas_presiden': fields.boolean('Presiden'),
        'control_integritas_gubernur': fields.boolean('Gubernur'),
        'control_integritas_kepalaopd': fields.boolean('Kepala OPD'),
        'control_integritas_atasan': fields.boolean('Atasan Langsung'),
        'control_integritas_lainlain': fields.boolean('Lain Lain'),
        'control_integritas_es1': fields.boolean('Pejabat Eselon I'),
        'control_integritas_es2': fields.boolean('Pejabat Eselon II'),
        'control_integritas_es3': fields.boolean('Pejabat Eselon III'),
        'control_integritas_es4': fields.boolean('Pejabat Eselon IV'),
        'control_integritas_hukuman': fields.selection([('ya', 'Terkena Hukuman Disiplin'), ('tidak', 'Tidak Terkena Hukuman Disiplin')],'Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Atau Tidak "),
        'control_integritas_hukuman_ringan': fields.boolean('Ringan'),
        'control_integritas_hukuman_sedang': fields.boolean('Sedang'),
        'control_integritas_hukuman_berat': fields.boolean('Berat'),
        'control_hadir_hari_kerja'     : fields.integer('Kehadiran Hari Kerja'),
        'control_hadir_jam_kerja': fields.integer('Kehadiran Jam Kerja'),
        'control_jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja'),
        'control_jumlah_jam_kerja': fields.integer('Jumlah Jam Kerja'),
        'control_hadir_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar'),
        'control_kerjasama_nasional': fields.boolean('Nasional'),
        'control_kerjasama_gubernur': fields.boolean('Provinsi'),
        'control_kerjasama_kepalaopd': fields.boolean('OPD'),
        'control_kerjasama_atasan': fields.boolean('Atasan Langsung'),
        'control_kerjasama_lainlain': fields.boolean('Lain Lain'),
        'control_kerjasama_rapat_atasan': fields.boolean('Rapat Atasan Langsung'),
        'control_kerjasama_rapat_perangkat_daerah': fields.boolean('Rapat Perangkat Daerah'),
        'control_kerjasama_rapat_provinsi': fields.boolean('Rapat Provinsi'),
        'control_kerjasama_rapat_nasional': fields.boolean('Rapat Nasional'),
        'control_kepemimpinan_nasional': fields.boolean('Nasional'),
        'control_kepemimpinan_gubernur': fields.boolean('Provinsi'),
        'control_kepemimpinan_kepalaopd': fields.boolean('OPD'),
        'control_kepemimpinan_atasan': fields.boolean('Atasan Langsung'),
        'control_kepemimpinan_lainlain': fields.boolean('Lain Lain'),
        'control_kepemimpinan_narsum_unitkerja': fields.boolean('Narasumber Kerja Atasan Langsung'),
        'control_kepemimpinan_narsum_perangkat_daerah': fields.boolean('Narasumber Perangkat Daerah'),
        'control_kepemimpinan_narsum_provinsi': fields.boolean('Narasumber Provinsi'),
        'control_kepemimpinan_narsum_nasional': fields.boolean('Narasumber Nasional'),
        
        'lookup_apel_pagi'     : fields.integer('Jumlah Apel Pagi', readonly=True),
        'lookup_jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja', readonly=True),
        'lookup_jumlah_jam_kerja'     :fields.integer('Jumlah Jam Kerja', readonly=True),
        'lookup_upacara_hari_besar'     : fields.integer('Upacara Hari Besar', readonly=True),
        'lookup_biaya'     : fields.float('Verifikasi Biaya', readonly=True),
                                        
        'control_count': fields.integer('Jumlah Pengajuan Verifikasi', readonly=True),
        'nilai_akhir': fields.float('Nilai', readonly=True),
        'nilai_sementara': fields.float('Nilai Sementara', readonly=True),
        
        'nilai_kepemimpinan': fields.float('Nilai Kepemimpinan', readonly=True),
        'nilai_kerjasama': fields.float('Nilai Kerjasama', readonly=True),
        'nilai_integritas': fields.float('Nilai Integritas', readonly=True),
        'nilai_komitmen': fields.float('Nilai Komitmen', readonly=True),
        'nilai_disiplin': fields.float('Nilai Disiplin', readonly=True),
        'nilai_pelayanan': fields.float('Nilai Pelayanan', readonly=True),
        'nilai_tambahan': fields.float('Nilai Tugas Tambahan', readonly=True),
        'nilai_kreatifitas': fields.float('Nilai Kreatifitas', readonly=True),
        'jumlah_perhitungan': fields.float('Jumlah Perhitungan', readonly=True),
        'indeks_nilai': fields.char('Indeks', size=20, readonly=True),
        'project_state': fields.related('project_id', 'state', type='char', string='Target Status', store=False),
        'progress': fields.function(_progress_by_stage, string='Progress (%)', type='float', help="Progress Berdasarkan Status",
            store=False),
        'target_realiasi_notsame' :fields.function(_get_status_target_realiasi_notsame, method=True, string='Realisasi Tidak Sama Target', type='boolean', readonly=True, store=False),
        'suggest_realiasi_notsame' :fields.function(_get_status_suggest_realiasi_notsame, method=True, string='Status Suggest Target Output', type='boolean', readonly=True, store=False),
        'biaya_verifikasi_notsame' :fields.function(_get_status_biaya_verifikasi_notsame, method=True, string='Status Verifikasi Biaya', type='boolean', readonly=True, store=False),
        'komitmen_verifikasi_notsame' :fields.function(_get_status_komitmen_verifikasi_notsame, method=True, string='Status Verifikasi Biaya', type='boolean', readonly=True, store=False),
        'project_not_exist' :fields.function(_get_status_project_not_exist, method=True, string='Status Target Tahunan', type='boolean', readonly=True, store=False),
         'employee_id': fields.related('user_id', 'partner_id', relation='res.partner', type='many2one', string='Data Pegawai', store=False),
        'employee_job_type': fields.related('employee_id', 'job_type', type='char', string='Tipe Jabatan', store=False),
        'is_kepala_opd': fields.related('employee_id', 'is_kepala_opd', type='boolean', string='Tugas Untuk Kepala OPD', store=False),
        'use_target_for_calculation': fields.boolean('Perhitungan Menggunakan Target',help="Pengakuan perhitungan berdasar target, Bukan Realisasi"),
        #'wakilkan_pengajuan_bkd': fields.boolean('Wakilkan Pengajuan Ke BKD',help="True Pengajuan BKD Diwakilkan Petugas Verifikasi"),
        'notes_atasan'      : fields.text('Catatan Koreksi Pejabat Penilai',readolny=True),
        'notes_atasan_banding'      : fields.text('Catatan Koreksi Atasan Pejabat Penilai' ,readolny=True),
        
    }
    _defaults = {
        'target_category':'bulanan',
        'user_id': lambda self, cr, uid, ctx: uid,
        'control_biaya':None,
        'control_hadir_hari_kerja':None,
        'control_hadir_jam_kerja':None,
        'control_count':0,
        'work_state':'draft',
        'name':'',
        'target_period_year':lambda *args: time.strftime('%Y'),
        'realisasi_integritas_hukuman':'tidak',
        #'task_category':'non_skp'
        #'wakilkan_pengajuan_bkd':False,
        
    }
    def onchange_iscontrol(self, cr, uid, ids, is_control, context=None):
        value = {'is_suggest': False}

        if is_control:
            value['is_suggest'] = is_control
        return {'value': value}
    def get_stage_id(self, cr, uid, stage_sequence, context=None):
        stage_pool = self.pool.get('project.task.type')
        stage_ids = stage_pool.search(cr, uid, [('sequence', '=', stage_sequence)], context=None)
        if stage_ids :
            return stage_ids[0]
        return False
    def get_task_auth_id(self, cr, uid, ids, context=None):
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            #print task_obj.user_id
            if task_obj.user_id :
                #print task_obj.user_id.id, ' --- ', uid
                if task_obj.user_id.id != uid :
                    raise osv.except_osv(_('Invalid Action!'),
                                         _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
                else : 
                    return True;
            else :
                return True;
    def get_auth_id(self, cr, uid, ids, type, context=None):
        if not isinstance(ids, list): ids = [ids]
        for task in self.browse(cr, uid, ids, context=context):
            
            if type == 'user_id' :
                if task.user_id :
                    if task.user_id.id != uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            elif type == 'user_id_atasan' :
                if task.user_id_atasan :
                    if task.user_id_atasan.id != uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            elif type == 'user_id_banding' :
                if task.user_id_banding :
                    if task.user_id_banding.id != uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            elif type == 'user_id_bkd' :
                if task.user_id_bkd :
                    if task.user_id_bkd.id != uid :
                        raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
                
            else : 
               return False;
            
        return True;
# <!-- workflow -->            
    def init_user_approval(self, cr, uid, ids, context=None):
        for task_obj in self.browse(cr, uid, ids, context=context):
            employee = self.get_employee_from_user_id(cr, uid, task_obj);
            task_property = {}
           
            if not employee :
                raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Ada Beberapa Informasi Kepegawaian Belum Diisi, Khususnya Data Pejabat Penilai Dan Atasan Banding.'))
            else :
                company = employee.company_id
                company_id = company.id
                currency_id = employee.company_id.currency_id
                
                #print "company_id : ", company_id, ' - ', currency_id
                
                if not company_id :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Unit Dinas Pegawai Belum Dilengkapi.'))
                #print "employee parent : ", employee.parent_id
                if not task_obj.user_id_bkd:
                    if not company.user_id_bkd :
                        raise osv.except_osv(_('Invalid Action, Data Dinas Kurang Lengkap'),
                                    _('Staff Pemeriksa Dari BKD Tidak Tersedia Untuk Unit Anda, Silahkan hubungi Admin Atau isi Data Pemeriksa.'))
                    else :
                        user_id_bkd = company.user_id_bkd.id
                else :
                    user_id_bkd = task_obj.user_id_bkd.id 
                if not employee.parent_id :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Penilai Belum Terisi.'))
                if not employee.user_id_banding :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Pengajuan Banding.'))
            
            user_id_atasan = task_obj.user_id_atasan.id
            user_id_banding = task_obj.user_id_banding.id 
            
            if not task_obj.user_id_atasan.id :
                user_id_atasan = employee.parent_id.user_id.id
            if not task_obj.user_id_banding.id :
                user_id_banding = employee.user_id_banding.user_id.id
                #print "USER ID BANDING : ", employee.user_id_banding.user_id.name
            task_property.update({   'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'currency_id':currency_id
                           })
            self.write(cr, uid, [task_obj.id], task_property)
        return True
    def action_target_done(self, cr, uid, ids, context=None):
        """ Khusus untuk kegiatan perilaku dan  tambahan & kreatifitas.
            Kondisi pegawai siap mengisikan realisasi
        """
        task_id = len(ids) and ids[0] or False
        ret_val = False
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id', context=context) :
            if self.validate_target_state(cr, uid, [task_id], context) :
                    self.fill_task_automatically_with_target(cr, uid, [task_id], context);
                    self.fill_target_perilaku(cr, uid, [task_id], context);
                    self.fill_lookup_perilaku_komitmen(cr, uid, [task_id], context);
                    ret_val = self.do_target_done(cr, uid, [task_id], context=context)
                    self.do_target_done_notification(cr, uid, [task_id], context=context)
               
        return ret_val
    def validate_target_state(self,cr,uid,ids,context=None):
         for task_obj in self.browse(cr, uid, ids, context=context):
             if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                 if task_obj.project_id:
                     if task_obj.project_id.state=='confirm':
                         return True;
                     else :
                         raise osv.except_osv(_('Invalid Action, Proses Tidak Dapat Dilanjutkan'),
                                        _('Proses Tidak Dapat Dilanjutkan Karena Target Belum Di Terima.'))
         return True;
                
    def do_target_done(self, cr, uid, ids, context=None):
        """ Pembuatan Target Selesai """
        #print "draft->realisasi...Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            update_stage_state = {
                                'work_state': 'realisasi',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
        self.init_user_approval(cr, uid, ids);
        return True
    def action_realisasi(self, cr, uid, ids, context=None):
        """ Selesai mengerjakan input realisasi, 
        """
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id', context=context) :
            if self.validate_ajukan_atasan_state(cr, uid, [task_id], context) :
                self.fill_target_automatically_with_task(cr, uid, [task_id], context);
                return self.do_realisasi(cr, uid, [task_id], context=context)

    def do_realisasi(self, cr, uid, ids, context=None):
        """ Realisasi-> Pengajuan ke atasan Langsung """
        #print "Realisasi-> Pengajuan ke atasan Langsung...Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'propose',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
        return True
    def validate_ajukan_atasan_state(self,cr,uid,ids,context=None):
         for task_obj in self.browse(cr, uid, ids, context=context):
             if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                 if not task_obj.project_id:
                     raise osv.except_osv(_('Invalid Action, Proses Tidak Dapat Dilanjutkan'),
                                        _('Karena Kegiatan Tidak Memiliki Target Tahunan.'))
                 if task_obj.project_id:
                     if task_obj.project_id.state=='confirm':
                         return True;
                     else :
                         raise osv.except_osv(_('Invalid Action, Proses Tidak Dapat Dilanjutkan'),
                                        _('Proses Tidak Dapat Dilanjutkan Karena Target Belum Di Terima.'))
         return True;
    def action_propose(self, cr, uid, ids, context=None):
        """ Pengajuan Realisasi selesai dan diterima. Siap diajukan ke BKD, 
        """
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context) :
            #self.fill_control_automatically_with_task(cr,uid,[task_id],context);
            return self.do_propose(cr, uid, [task_id], context=context)

    def set_status_pengajuan_bkd(self, cr, uid, task_id,status, context=None):
        """ Shorcut untuk pengajuakn ke bkd """
        
        #update_val = {
        #              'wakilkan_pengajuan_bkd': status,
        #            }
        #self.write(cr, uid, task_id, update_val)
        return True
    def do_propose(self, cr, uid, ids, context=None):
        """ Propose->BKD """
        #print "Propose->BKD...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'evaluated',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
            #self.do_task_poin_calculation_temporary(cr,uid,[task_obj.id], context=context)
        return True
    def action_propose_rejected_popup(self, cr, uid, ids, context=None):
        if not ids: return []
        
        if self.get_auth_id(cr, uid, ids, 'user_id_atasan', context=context) :
            task_obj = self.browse(cr, uid, ids[0], context=context)
            
            if task_obj.task_category == 'skp' :
                dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_propose_rejected_popup_form_view')
                return {
                    'name':_("Pengajuan Di Tolak"),
                    'view_mode': 'form',
                    'view_id': view_id,
                    'view_type': 'form',
                    'res_model': 'project.task.propose.rejected',
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                    'context': {
                        'default_jumlah_kuantitas_output': task_obj.realisasi_jumlah_kuantitas_output,
                        'default_satuan_kuantitas_output':task_obj.realisasi_satuan_kuantitas_output.id,
                        'default_kualitas':task_obj.realisasi_kualitas ,
                        'default_waktu': task_obj.realisasi_waktu,
                        'default_satuan_waktu': task_obj.realisasi_satuan_waktu,
                        'default_biaya': task_obj.realisasi_biaya,
                        'default_angka_kredit': task_obj.realisasi_angka_kredit,
                        'default_is_suggest': True,
                        'default_task_id':task_obj.id
        
                    }
                }
            else :
                if task_obj.target_type_id == 'perilaku' :
                    dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_perilaku_propose_rejected_popup_form_view')
                    return {
                        'name':_("Pengajuan Perilaku DiTolak"),
                        'view_mode': 'form',
                        'view_id': view_id,
                        'view_type': 'form',
                        'res_model': 'project.task.perilaku.propose.rejected',
                        'type': 'ir.actions.act_window',
                        'nodestroy': True,
                        'target': 'new',
                        'domain': '[]',
                        'context': {
                            'default_jumlah_konsumen_pelayanan'       : task_obj.realisasi_jumlah_konsumen_pelayanan,
                                        'default_satuan_jumlah_konsumen_pelayanan': task_obj.realisasi_satuan_jumlah_konsumen_pelayanan.id or None,
                                        'default_jumlah_tidakpuas_pelayanan'      : task_obj.realisasi_jumlah_tidakpuas_pelayanan,
                                        'default_ketepatan_laporan_spj'           : task_obj.realisasi_ketepatan_laporan_spj.id or None,
                                        'default_ketepatan_laporan_ukp4'          : task_obj.realisasi_ketepatan_laporan_ukp4.id or None,
                                        'default_efisiensi_biaya_operasional'     : task_obj.realisasi_efisiensi_biaya_operasional.id or None,
                                        
                                        'default_hadir_upacara_hari_besar': task_obj.realisasi_hadir_upacara_hari_besar,
                                        'default_hadir_hari_kerja'     : task_obj.realisasi_hadir_hari_kerja,
                                        'default_hadir_jam_kerja': task_obj.realisasi_hadir_jam_kerja,
                                        'default_hadir_apel_pagi': task_obj.realisasi_hadir_apel_pagi,
                                        
                                        'default_integritas_presiden': task_obj.realisasi_integritas_presiden,
                                        'default_integritas_gubernur': task_obj.realisasi_integritas_gubernur,
                                        'default_integritas_kepalaopd': task_obj.realisasi_integritas_kepalaopd,
                                        'default_integritas_atasan': task_obj.realisasi_integritas_atasan,
                                        'default_integritas_es1': task_obj.realisasi_integritas_es1,
                                        'default_integritas_es2': task_obj.realisasi_integritas_es2,
                                        'default_integritas_es3': task_obj.realisasi_integritas_es3,
                                        'default_integritas_es4': task_obj.realisasi_integritas_es4,
                                        
                                        'default_integritas_hukuman': task_obj.realisasi_integritas_hukuman,
                                        'default_integritas_hukuman_ringan': task_obj.realisasi_integritas_hukuman_ringan,
                                        'default_integritas_hukuman_sedang': task_obj.realisasi_integritas_hukuman_sedang,
                                        'default_integritas_hukuman_berat': task_obj.realisasi_integritas_hukuman_berat,
                                        
                                        'default_kerjasama_nasional': task_obj.realisasi_kerjasama_nasional,
                                        'default_kerjasama_gubernur': task_obj.realisasi_kerjasama_gubernur,
                                        'default_kerjasama_kepalaopd': task_obj.realisasi_kerjasama_kepalaopd,
                                        'default_kerjasama_atasan':task_obj.realisasi_kerjasama_atasan,
                                        'default_kerjasama_rapat_nasional': task_obj.realisasi_kerjasama_rapat_nasional,
                                        'default_kerjasama_rapat_provinsi': task_obj.realisasi_kerjasama_rapat_provinsi,
                                        'default_kerjasama_rapat_perangkat_daerah': task_obj.realisasi_kerjasama_rapat_perangkat_daerah,
                                        'default_kerjasama_rapat_atasan': task_obj.realisasi_kerjasama_rapat_atasan,
                                        
                                        'default_kepemimpinan_nasional': task_obj.realisasi_kepemimpinan_nasional,
                                        'default_kepemimpinan_gubernur': task_obj.realisasi_kepemimpinan_gubernur,
                                        'default_kepemimpinan_kepalaopd': task_obj.realisasi_kepemimpinan_kepalaopd,
                                        'default_kepemimpinan_atasan':  task_obj.realisasi_kepemimpinan_atasan,
                                        'default_kepemimpinan_narsum_nasional': task_obj.realisasi_kepemimpinan_narsum_nasional,
                                        'default_kepemimpinan_narsum_provinsi': task_obj.realisasi_kepemimpinan_narsum_provinsi,
                                        'default_kepemimpinan_narsum_perangkat_daerah': task_obj.realisasi_kepemimpinan_narsum_perangkat_daerah,
                                        'default_kepemimpinan_narsum_unitkerja': task_obj.realisasi_kepemimpinan_narsum_unitkerja,
                                        
                                        'default_target_type_id': task_obj.target_type_id,
                                        'default_is_kepala_opd': task_obj.is_kepala_opd,
                                        'default_employee_job_type': task_obj.employee_job_type,
                                        'default_is_suggest': True,
                                        'default_task_id':task_obj.id
            
                        }
                    }
                elif task_obj.target_type_id == 'tambahan' :
                    dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_tambahan_propose_rejected_popup_form_view')
                    return {
                    'name':_("Pengajuan Tugas Tambahan Dan Kreatifitas DiTolak"),
                    'view_mode': 'form',
                    'view_id': view_id,
                    'view_type': 'form',
                    'res_model': 'project.task.tambahan.propose.rejected',
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                    'context': {
                                   'default_tugas_tambahan'              : task_obj.realisasi_tugas_tambahan,
                                    'default_uraian_tugas_tambahan'       : task_obj.realisasi_uraian_tugas_tambahan,
                                    'default_rl_opd_tugas_tambahan'       : task_obj.realisasi_rl_opd_tugas_tambahan,
                                    'default_rl_gubernur_tugas_tambahan'  : task_obj.realisasi_rl_gubernur_tugas_tambahan,
                                    'default_rl_presiden_tugas_tambahan'  : task_obj.realisasi_rl_presiden_tugas_tambahan,
                                    'default_nilai_kreatifitas'           : task_obj.realisasi_nilai_kreatifitas,
                                    'default_uraian_kreatifitas'          : task_obj.realisasi_uraian_kreatifitas,
                                    'default_tupoksi_kreatifitas'         : task_obj.realisasi_tupoksi_kreatifitas,
                                    'default_rl_opd_kreatifitas'          : task_obj.realisasi_rl_opd_kreatifitas,
                                    'default_rl_gubernur_kreatifitas'     : task_obj.realisasi_rl_gubernur_kreatifitas,
                                    'default_rl_presiden_kreatifitas'     : task_obj.realisasi_rl_presiden_kreatifitas,
                                        
                                 'default_target_type_id': task_obj.target_type_id,
                                 'default_is_suggest': True,
                                 'default_task_id':task_obj.id
        
                    }
                }
                    
            
        return False
    
    def action_rejected_manager(self, cr, uid, ids, context=None):
        """ Pengajuan Realisasi ditolak. Harus dikoreksi, 
        """
        #print "Propose->action_rejected_manager...(Updated)"
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context) :
            return self.do_rejected_manager(cr, uid, [task_id], context=context)
    
    def do_rejected_manager(self, cr, uid, ids, context=None):
        """ Propose->action_rejected_manager """
        #print "Propose->action_rejected_manager...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if not task_obj.is_suggest :
                raise osv.except_osv(_('Invalid Action, Field Required!'),
                                         _('Silahkan Ceklis Terlebih Tanda Dibawah Catatan, Dan Isikan Nilai Usulan Serta Catatan Penolakan.'))
                return False;
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'rejected_manager',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
        return True
    def action_appeal_reject_popup(self, cr, uid, ids, context=None):
        if not ids: return []
        
        if self.get_auth_id(cr, uid, ids, 'user_id_banding', context=context) :
            task_obj = self.browse(cr, uid, ids[0], context=context)
            
            if task_obj.task_category == 'skp' :
                dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_appeal_rejected_popup_form_view')
                return {
                'name':_("Pengajuan Banding Di Tolak"),
                'view_mode': 'form',
                'view_id': view_id,
                'view_type': 'form',
                'res_model': 'project.task.appeal.rejected',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': {
                    'default_jumlah_kuantitas_output': task_obj.suggest_jumlah_kuantitas_output,
                    'default_satuan_kuantitas_output':task_obj.suggest_satuan_kuantitas_output.id,
                    'default_kualitas':task_obj.suggest_kualitas ,
                    'default_waktu': task_obj.suggest_waktu,
                    'default_satuan_waktu': task_obj.suggest_satuan_waktu,
                    'default_biaya': task_obj.suggest_biaya,
                    'default_angka_kredit': task_obj.suggest_angka_kredit,
                    'default_is_appeal': True,
                    'default_task_id':task_obj.id
    
                }
            }
            else :
                if task_obj.target_type_id == 'perilaku' :
                    dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_perilaku_appeal_rejected_popup_form_view')
                    return {
                        'name':_("Pengajuan Banding Perilaku Ditolak"),
                        'view_mode': 'form',
                        'view_id': view_id,
                        'view_type': 'form',
                        'res_model': 'project.task.perilaku.appeal.rejected',
                        'type': 'ir.actions.act_window',
                        'nodestroy': True,
                        'target': 'new',
                        'domain': '[]',
                        'context': {
                            'default_jumlah_konsumen_pelayanan'       : task_obj.suggest_jumlah_konsumen_pelayanan,
                                        'default_satuan_jumlah_konsumen_pelayanan': task_obj.suggest_satuan_jumlah_konsumen_pelayanan.id or None,
                                        'default_jumlah_tidakpuas_pelayanan'      : task_obj.suggest_jumlah_tidakpuas_pelayanan,
                                        'default_ketepatan_laporan_spj'           : task_obj.suggest_ketepatan_laporan_spj.id or None,
                                        'default_ketepatan_laporan_ukp4'          : task_obj.suggest_ketepatan_laporan_ukp4.id or None,
                                        'default_efisiensi_biaya_operasional'     : task_obj.suggest_efisiensi_biaya_operasional.id or None,
                                        
                                        'default_hadir_upacara_hari_besar': task_obj.suggest_hadir_upacara_hari_besar,
                                        'default_hadir_hari_kerja'     : task_obj.suggest_hadir_hari_kerja,
                                        'default_hadir_jam_kerja': task_obj.suggest_hadir_jam_kerja,
                                        'default_hadir_apel_pagi': task_obj.suggest_hadir_apel_pagi,
                                        
                                        'default_integritas_presiden': task_obj.suggest_integritas_presiden,
                                        'default_integritas_gubernur': task_obj.suggest_integritas_gubernur,
                                        'default_integritas_kepalaopd': task_obj.suggest_integritas_kepalaopd,
                                        'default_integritas_atasan': task_obj.suggest_integritas_atasan,
                                        'default_integritas_es1': task_obj.suggest_integritas_es1,
                                        'default_integritas_es2': task_obj.suggest_integritas_es2,
                                        'default_integritas_es3': task_obj.suggest_integritas_es3,
                                        'default_integritas_es4': task_obj.suggest_integritas_es4,
                                        
                                        'default_integritas_hukuman': task_obj.suggest_integritas_hukuman,
                                        'default_integritas_hukuman_ringan': task_obj.suggest_integritas_hukuman_ringan,
                                        'default_integritas_hukuman_sedang': task_obj.suggest_integritas_hukuman_sedang,
                                        'default_integritas_hukuman_berat': task_obj.suggest_integritas_hukuman_berat,
                                        
                                        'default_kerjasama_nasional': task_obj.suggest_kerjasama_nasional,
                                        'default_kerjasama_gubernur': task_obj.suggest_kerjasama_gubernur,
                                        'default_kerjasama_kepalaopd': task_obj.suggest_kerjasama_kepalaopd,
                                        'default_kerjasama_atasan':task_obj.suggest_kerjasama_atasan,
                                        'default_kerjasama_rapat_nasional': task_obj.suggest_kerjasama_rapat_nasional,
                                        'default_kerjasama_rapat_provinsi': task_obj.suggest_kerjasama_rapat_provinsi,
                                        'default_kerjasama_rapat_perangkat_daerah': task_obj.suggest_kerjasama_rapat_perangkat_daerah,
                                        'default_kerjasama_rapat_atasan': task_obj.suggest_kerjasama_rapat_atasan,
                                        
                                        'default_kepemimpinan_nasional': task_obj.suggest_kepemimpinan_nasional,
                                        'default_kepemimpinan_gubernur': task_obj.suggest_kepemimpinan_gubernur,
                                        'default_kepemimpinan_kepalaopd': task_obj.suggest_kepemimpinan_kepalaopd,
                                        'default_kepemimpinan_atasan':  task_obj.suggest_kepemimpinan_atasan,
                                        'default_kepemimpinan_narsum_nasional': task_obj.suggest_kepemimpinan_narsum_nasional,
                                        'default_kepemimpinan_narsum_provinsi': task_obj.suggest_kepemimpinan_narsum_provinsi,
                                        'default_kepemimpinan_narsum_perangkat_daerah': task_obj.suggest_kepemimpinan_narsum_perangkat_daerah,
                                        'default_kepemimpinan_narsum_unitkerja': task_obj.suggest_kepemimpinan_narsum_unitkerja,
                                        
                                        'default_target_type_id': task_obj.target_type_id,
                                        'default_is_kepala_opd': task_obj.is_kepala_opd,
                                        'default_employee_job_type': task_obj.employee_job_type,
                                        'default_is_suggest': True,
                                        'default_task_id':task_obj.id
            
                        }
                    }
                elif task_obj.target_type_id == 'tambahan' :
                    dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_tambahan_appeal_rejected_popup_form_view')
                    return {
                    'name':_("Pengajuan Banding Tugas Tambahan Dan Kreatifitas Ditolak"),
                    'view_mode': 'form',
                    'view_id': view_id,
                    'view_type': 'form',
                    'res_model': 'project.task.tambahan.appeal.rejected',
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                    'context': {
                                   'default_tugas_tambahan'              : task_obj.suggest_tugas_tambahan,
                                    'default_uraian_tugas_tambahan'       : task_obj.suggest_uraian_tugas_tambahan,
                                    'default_rl_opd_tugas_tambahan'       : task_obj.suggest_rl_opd_tugas_tambahan,
                                    'default_rl_gubernur_tugas_tambahan'  : task_obj.suggest_rl_gubernur_tugas_tambahan,
                                    'default_rl_presiden_tugas_tambahan'  : task_obj.suggest_rl_presiden_tugas_tambahan,
                                    'default_nilai_kreatifitas'           : task_obj.suggest_nilai_kreatifitas,
                                    'default_uraian_kreatifitas'          : task_obj.suggest_uraian_kreatifitas,
                                    'default_tupoksi_kreatifitas'         : task_obj.suggest_tupoksi_kreatifitas,
                                    'default_rl_opd_kreatifitas'          : task_obj.suggest_rl_opd_kreatifitas,
                                    'default_rl_gubernur_kreatifitas'     : task_obj.suggest_rl_gubernur_kreatifitas,
                                    'default_rl_presiden_kreatifitas'     : task_obj.suggest_rl_presiden_kreatifitas,
                                        
                                 'default_target_type_id': task_obj.target_type_id,
                                 'default_is_appeal': True,
                                 'default_task_id':task_obj.id
        
                    }
                }
        return False
    
    def action_dont_appeal(self, cr, uid, ids, context=None):
        """ Penolakan Diterima, Langsung ajukan Ke BKD, 
        """
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        ret_val = False;
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id', context=context) :
            self.fill_task_automatically_with_suggest(cr, uid, [task_id], context);
            ret_val = self.do_propose(cr, uid, [task_id], context=context)
            # if ret_val:
                
        return ret_val;
    def action_appeal(self, cr, uid, ids, context=None):
        """ Penolakan di Banding ke Atasan 
        """
        task_id = len(ids) and ids[0] or False
        ret_val = False;
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id', context=context) :
            self.fill_task_appeal_automatically_with_suggest(cr, uid, [task_id], context);
            ret_val = self.do_appeal(cr, uid, [task_id], context=context)
            # if ret_val:
                
            
            
        return ret_val;
    def do_appeal(self, cr, uid, ids, context=None):
        """ rejected manager->Atasan Langsung (Appeal) """
        #print "rejected manager->Atasan Langsung (Appeal)...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'appeal',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
        return True
    def action_appeal_approve(self, cr, uid, ids, context=None):
        """ Banding DIterima, Langsung ajukan Ke BKD, 
        """
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_banding', context=context) :
            return self.do_propose(cr, uid, [task_id], context=context)

    def action_appeal_reject(self, cr, uid, ids, context=None):
        """ Banding Ditolak
        """
        ret_val = False;
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_banding', context=context) :
            self.fill_task_automatically_with_appeal(cr, uid, [task_id], context);
            ret_val = self.do_appeal_reject(cr, uid, [task_id], context=context)
            
        return ret_val;
    def do_appeal_reject(self, cr, uid, ids, context=None):
        """ Propose->BKD """
        #print "Propose->BKD...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            if not task_obj.is_appeal :
                raise osv.except_osv(_('Invalid Action, Field Required!'),
                                         _('Silahkan Ceklis Terlebih Tanda Dibawah Catatan, Dan Isikan Nilai Final Serta Catatan Penolakan.'))
            update_stage_state = {
                                'work_state': 'evaluated',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
            #self.do_task_poin_calculation_temporary(cr,uid,[task_obj.id], context=context)
        return True
    def action_work_rejected_popup(self, cr, uid, ids, context=None):
        """ Verifikasi Ditolak
        """
        
        if not ids: return []
        
        if self.get_auth_id(cr, uid, ids, 'user_id_bkd', context=context) :
            dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'df_project', 'action_verificate_rejected_popup_form_view')
            task_obj = self.browse(cr, uid, ids[0], context=context)
            print "task_obj.control_count :",task_obj.control_count
            if task_obj.control_count >= 2 :
                raise osv.except_osv(_('Invalid Action, '),
                                         _('Hasil Verifikasi Tidak Dapat Ditolak, Karena Sudah Dilakukan Pengajuan Dan Verifikasi Sebanyak 2 Kali.'))
            return {
                'name':_("Verifikasi Ditolak"),
                'view_mode': 'form',
                'view_id': view_id,
                'view_type': 'form',
                'res_model': 'project.task.verificate.rejected',
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                'domain': '[]',
                'context': {
                    'default_control_count':task_obj.control_count,
                    'default_is_control': True,
                    'default_task_id':task_obj.id
    
                }
            }
        return False
    def action_work_rejected(self, cr, uid, ids, context=None):
        """ Pengajuan Realisasi ditolak oleh BKD. Harus Dikoreksi Oleh atasan, 
        """
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context) :
            return self.do_work_rejected(cr, uid, [task_id], context=context)
    def do_work_rejected(self, cr, uid, ids, context=None):
        """ BKD->Rejected (Atasan) """
        #print "BKD->Rejected (Atasan)...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj.control_count > 1 :
                raise osv.except_osv(_('Invalid Action, Limit Action'),
                                         _('Hasil Verifikasi Tidak Dapat Ditolak, Karena Sudah Dilakukan Pengajuan Dan Verifikasi Sebanyak 2 Kali.'))
            if not task_obj.is_control :
                raise osv.except_osv(_('Invalid Action, Field Required!'),
                                         _('Silahkan Ceklis Terlebih Tanda Dibawah Catatan, Dan Isikan Nilai Verifikasi Serta Catatan Penolakan.'))
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'rejected_bkd',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
        return True
    def action_accept_verificate(self, cr, uid, ids, context=None):
        """ Hasil Verifikasi DIterima, Langsung ajukan Ke BKD, 
        """
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context) :
            #self.fill_task_automatically_with_control(cr, uid, [task_id], context);
            return self.do_accept_verificate(cr, uid, [task_id], context=context)
    def do_accept_verificate(self, cr, uid, ids, context=None):
        """ Accept Verifikasi->BKD """
        
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'evaluated',
                                'realisasi_biaya': task_obj.lookup_biaya,
                                'is_control':True,
                                'control_count':task_obj.control_count,
                                'is_verificated':True,
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
            #self.do_task_poin_calculation_temporary(cr,uid,[task_obj.id], context=context)
        return True
    def action_reject_verificate(self, cr, uid, ids, context=None):
        """ Hasil Verifikasi Ditolak Tetap ajukan nilai
        """
        ret_val = False;
        task_id = len(ids) and ids[0] or False
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_atasan', context=context) :
            self.fill_task_automatically_with_suggest(cr, uid, [task_id], context);
            ret_val = self.do_reject_verificate(cr, uid, [task_id], context=context)
        
        
        return ret_val;
    def do_reject_verificate(self, cr, uid, ids, context=None):
        """ Accept Verifikasi->BKD """
        
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            
            update_stage_state = {
                                'work_state': 'evaluated',
                                'is_control':True,
                                'control_count':task_obj.control_count,
                                'is_verificated':False,
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
            #self.do_task_poin_calculation_temporary(cr,uid,[task_obj.id], context=context)
        return True
    
    def action_work_done(self, cr, uid, ids, context=None):
        """ Pengajuan Realisasi selesai dan sudah dievaluasi BKD. Siap diajukan ke Keuangan dan Proses Selesai, 
        """
        task_id = len(ids) and ids[0] or False
        #print "TASK id : ", task_id
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context) :
            ret_val = self.do_work_done(cr, uid, [task_id], context=context)
            self.do_task_poin_calculation(cr, uid, [task_id], context=context)
            self.do_task_summary_calculation(cr, uid, [task_id], 1, context=context)
            return ret_val
        return False

    def do_work_done(self, cr, uid, ids, context=None):
        """ BKD->Done (Keuangan) """
        #print "BKD->Done (Keuangan)...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'work_state': 'done',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
            
        return True
    def action_work_done_use_target(self, cr, uid, ids, context=None):
        """ Pengajuan Realisasi selesai dan sudah dievaluasi BKD. Siap diajukan ke Keuangan dan Proses Selesai, 
        """
        task_id = len(ids) and ids[0] or False
        #print "TASK id : ", task_id
        # super(self)._check_child_task(cr, uid, ids, context=context)
        if not task_id: return False
        if self.get_auth_id(cr, uid, [task_id], 'user_id_bkd', context=context) :
            ret_val = self.do_work_done_use_target(cr, uid, [task_id], context=context)
            self.do_task_poin_calculation(cr, uid, [task_id], context=context)
            self.do_task_summary_calculation(cr, uid, [task_id], 1, context=context)
            return ret_val
        return False
    def do_work_done_use_target(self, cr, uid, ids, context=None):
        """ BKD->Done (Keuangan) """
        #print "BKD->Done (Keuangan)...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            # close task
            # vals['remaining_hours'] = 0.0
            update_stage_state = {
                                'use_target_for_calculation': True,
                                'work_state': 'done',
                                 }
            self.write(cr, uid, [task_obj.id], update_stage_state)
            
        return True
# <!-- POIN      -->
    def get_employee_from_user_id(self, cr, uid, task_obj, context=None):
        user_id = task_obj.user_id
        if user_id : 
            employees = self.pool.get('res.users').browse(cr, uid, user_id.id, context=context).employee_ids
            for employee in employees:
                return employee
    def get_value_poin(self, cr, uid, ids, nilai_akhir, context=None):
            # Tingkat kepuasan sebanyak 91 s.d 100 persen, maka nilai perilaku orientasi pelayanan Sangat Baik, dengan nilai antara 91 s.d 100 poin sesuai prosentase kepuasan    
            # Tingkat kepuasan sebanyak 76 s.d 90 persen, maka nilai perilaku orientasi pelayanan Baik, 
            # Tingkat kepuasan sebanyak 61 s.d 75 persen, maka nilai perilaku orientasi pelayanan Cukup, dengan nilai antara 61 s.d 75 poin sesuai prosentase kepuasan       
            # Tingkat kepuasan sebanyak 51 s.d 60 persen, maka nilai perilaku orientasi pelayanan Kurang, dengan nilai antara 51 s.d 60 poin sesuai prosentase kepuasan            
            # Tingkat kepuasan sebanyak kurang dari 50 persen, maka nilai perilaku orientasi pelayanan Buruk, dengan nilai antara 0 s.d 50 poin sesuai prosentase kepuasan
            value = '-'
            if nilai_akhir >= 91.0 and nilai_akhir <= 100.0 :
                value = 'Sangat Baik'; 
            if nilai_akhir >= 76.0 and nilai_akhir <= 90.0 :
                value = 'Baik'; 
            if nilai_akhir >= 61.0 and nilai_akhir <= 75.0 :
                value = 'Cukup'; 
            if nilai_akhir >= 51.0 and nilai_akhir <= 60.0 :
                value = 'Kurang'; 
            if nilai_akhir <= 50.0 :
                value = 'Buruk'; 
            return value;
    def get_value_realisasi_or_target(self, target,realisasi, use_target_for_calculation):
        if use_target_for_calculation : 
           return target
        return realisasi
    def prepare_task_poin_calculation(self, cr, uid, ids, context=None):
        """ BKD->Done (Keuangan) """
        #print "Poin Calculation"
        target_pool = self.pool.get('project.project')
        lookup_nilai_pool = self.pool.get('acuan.penailaian')
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            
            # close task...
            nilai_orientasi_pelayanan = 0
            nilai_integritas = 0
            nilai_komitment = 0
            nilai_disiplin = 0
            nilai_kerjasama = 0
            nilai_kepemimpinan = 0
            nilai_tambahan=0
            nilai_kreatifitas=0
            nilai_akhir = 0
            jumlah_perhitungan = 0
            indeks_nilai = 'a'
            pengali_waktu_ids = self.pool.get('config.skp').search(cr, uid, [('code', '=', 'x_waktu'), ('active', '=', True), ('type', '=', 'nilai')], context=None)
            pengali_waktu = self.pool.get('config.skp').browse(cr, uid, pengali_waktu_ids)[0].config_value_float
            pengali_biaya_ids = self.pool.get('config.skp').search(cr, uid, [('code', '=', 'x_biaya'), ('active', '=', True), ('type', '=', 'nilai')], context=None)
            pengali_biaya = self.pool.get('config.skp').browse(cr, uid, pengali_biaya_ids)[0].config_value_float
            efektifitas_biaya_ids = self.pool.get('config.skp').search(cr, uid, [('code', '=', 'x_std_b'), ('active', '=', True), ('type', '=', 'nilai')], context=None)
            efektifitas_biaya = self.pool.get('config.skp').browse(cr, uid, efektifitas_biaya_ids)[0].config_value_int or 0
            efektifitas_waktu_ids = self.pool.get('config.skp').search(cr, uid, [('code', '=', 'x_std_w'), ('active', '=', True), ('type', '=', 'nilai')], context=None)
            efektifitas_waktu = self.pool.get('config.skp').browse(cr, uid, efektifitas_waktu_ids)[0].config_value_int or 0
            
            employee = self.get_employee_from_user_id(cr, uid, task_obj);
            #print " pengali_waktu : ", pengali_waktu, " | pengali_biaya : ", pengali_biaya
            if not employee :
                 raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena User Login Belum Dikaitkan Dengan Data Pegawai.'))
            else :
                job_type = employee.job_type
                if not job_type :
                     raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Jenis Jabatan Pegawai Belum Diisi, Harap Dilengkapi Terlebih Dahulu Di Data Pegawai, Atau Data Jabatan.'))
            if task_obj:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    #validator Project
                    if not task_obj.project_id:
                        raise osv.except_osv(_('Invalid Action, Realisasi SKP Tidak Bisa Dinilai'),
                                    _('Realisasi SKP Tidak Bisa Dinilai, Karena Kegiatan Ini Tidak Memiliki Target Tahunan'))
                    else :
                        if task_obj.project_state != 'confirm':
                            raise osv.except_osv(_('Invalid Action, Realisasi SKP Tidak Bisa Dinilai'),
                                        _('Realisasi SKP Tidak Bisa Dinilai, Karena Target Tahunan Belum Diterima'))
                    
                    # (target/realisasi)*100
                    # =((1.76*I16-O16)/I16)*100
                    # =(((2.24*J16-P16)/J16)*100)
                    pembagi = 0
                    a = b = c = d = e = 0
                    if job_type in ('struktural', 'jft', 'jfu') :
                        if task_obj.target_jumlah_kuantitas_output != 0:
                            x = float (self.get_value_realisasi_or_target(task_obj.target_jumlah_kuantitas_output,
                                                                          task_obj.realisasi_jumlah_kuantitas_output,
                                                                          task_obj.use_target_for_calculation)
                                       )
                            y = float (task_obj.target_jumlah_kuantitas_output)
                            a = (x / y) * 100
                            if a > 100 :
                                a=100
                            pembagi += 1
                            
                        elif task_obj.target_jumlah_kuantitas_output == 0 and task_obj.realisasi_jumlah_kuantitas_output > 0 :
                             a=100
                             pembagi +=1
                        if task_obj.target_kualitas != 0 :
                            b = (float(self.get_value_realisasi_or_target(task_obj.target_kualitas,
                                                                          task_obj.realisasi_kualitas,
                                                                          task_obj.use_target_for_calculation) 
                                       / task_obj.target_kualitas)) * 100
                            if b > 100 :
                                b=100
                            pembagi += 1
                        elif task_obj.target_kualitas == 0 and task_obj.realisasi_kualitas >0 :
                            b=100
                            pembagi+=1
                        if task_obj.target_waktu > 0:
                            x = float (self.get_value_realisasi_or_target(task_obj.target_waktu,
                                                                          task_obj.realisasi_waktu,
                                                                          task_obj.use_target_for_calculation))
                            y = float (task_obj.target_waktu)
                            if efektifitas_waktu == 1:
                                x_efektifitas = 100 - ((x / y) * 100)
                                #print "x_efektifitas Waktu : ", x_efektifitas
                                #print "realisasi_waktu : ", x
                                #print "target_waktu : ", y
                                #print "y-x : ", (y - x)
                                #print "(pengali_waktu*(y-x)) : ", (pengali_waktu * (y - x))
                                #print "(pengali_waktu*(y-x)) /y: ", (pengali_waktu * (y - x)) / y
                                if x_efektifitas == 0.0 :
                                    c = (x / y) * 100
                                if x_efektifitas > 0.0 and x_efektifitas <= 24.0 :
                                    c = ((pengali_waktu * y - x) / y) * 100
                                if  x_efektifitas > 24.0 :
                                    c = ((pengali_waktu * y - x) / y) * 100
                                    c = 76 - (c - 100)
                            else :
                                c= (x / y) * 100
                            if c > 100 :
                                c=100
                            pembagi += 1
                    if job_type in ('struktural') :
                        if task_obj.target_biaya > 0:
                            x = float (self.get_value_realisasi_or_target(task_obj.target_biaya,
                                                                          task_obj.realisasi_biaya,
                                                                          task_obj.use_target_for_calculation))
                            y = float (task_obj.target_biaya)
                            if efektifitas_biaya == 1:
                                x_efektifitas = 100 - ((x / y) * 100)
                                #print "x_efektifitas Biaya : ", x_efektifitas
                                #print "realisasi_biaya : ", x
                                #print "target_biaya : ", y
                                #print "y-x : ", (y - x)
                                #print "(pengali_biaya*(y-x)) : ", (pengali_biaya * (y - x))
                                #print "(pengali_biaya*(y-x)) /y: ", (pengali_biaya * (y - x)) / y
                                if x_efektifitas == 0.0 :
                                    d = (x / y) * 100
                                if x_efektifitas > 0.0 and x_efektifitas <= 24.0 :
                                    d = ((pengali_biaya * y - x) / y) * 100
                                if  x_efektifitas > 24.0 :
                                    d = ((pengali_biaya * y - x) / y) * 100
                                    d = 76 - (d - 100)
                            else :
                                d= (x / y) * 100
                            if d > 100 :
                                d=100
                            pembagi += 1
                    if job_type in ('jft') :
                        if task_obj.target_angka_kredit != 0:
                            x = float (self.get_value_realisasi_or_target(task_obj.target_angka_kredit,
                                                                          task_obj.realisasi_angka_kredit,
                                                                          task_obj.use_target_for_calculation))
                            y = float (task_obj.target_angka_kredit)
                            e = (x / y) * 100
                            if e > 100 :
                                e=100
                            pembagi += 1
                        elif task_obj.target_angka_kredit == 0  and task_obj.realisasi_angka_kredit > 0 :
                             e=100
                             pembagi += 1
                            
                    
                    #print " Calc : ", a, " ,", b, " ,", c, " ,", d, " ,", e , " = ", (a + b + c + d + e)
                    if pembagi > 0 :
                        jumlah_perhitungan = (a + b + c + d + e)
                        nilai_akhir = (jumlah_perhitungan / pembagi)
                        if nilai_akhir>100:
                            nilai_akhir=100;
                    
               
                
                if task_obj.target_type_id in ('tambahan'):
                    a = b = 0
                    if task_obj.realisasi_tugas_tambahan >= 1 :
                       # print "task_obj.realisasi_tugas_tambahan : -,",task_obj.realisasi_tugas_tambahan
                        lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_nilai', '=', 'threshold'), ('active', '=', True), ('type', '=', 'tugas_tambahan')
                                                                            ,('nilai_bawah', '<=', task_obj.realisasi_tugas_tambahan), ('nilai_atas', '>=', task_obj.realisasi_tugas_tambahan)], context=None)
                       # print "lookup_nilai_id : -,- ",lookup_nilai_id
                        lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                        nilai_tambahan = lookup_nilai.nilai_tunggal
                        a = nilai_tambahan;
                    if task_obj.realisasi_nilai_kreatifitas >= 1 :
                        if task_obj.realisasi_rl_opd_kreatifitas :
                            lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kreatifitas', '=', 'kepalaopd'), ('active', '=', True), ('type', '=', 'kreatifitas')], context=None)
                            lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                            nilai_kreatifitas = nilai_kreatifitas + lookup_nilai.nilai_tunggal
                        elif task_obj.realisasi_rl_gubernur_kreatifitas :
                            lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kreatifitas', '=', 'gubernur'), ('active', '=', True), ('type', '=', 'kreatifitas')], context=None)
                            lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                            nilai_kreatifitas = nilai_kreatifitas + lookup_nilai.nilai_tunggal
                        elif task_obj.realisasi_rl_presiden_kreatifitas :
                            lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kreatifitas', '=', 'presiden'), ('active', '=', True), ('type', '=', 'kreatifitas')], context=None)
                            lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                            nilai_kreatifitas = nilai_kreatifitas + lookup_nilai.nilai_tunggal
                        
                        b = nilai_kreatifitas;
                    jumlah_perhitungan = (a + b)
                    nilai_akhir = (a + b)
                # =(I62-O62)/I62*100
                if task_obj.target_type_id in ('perilaku'):
                     # if not task_obj.realisasi_integritas_atasan :
                     #    raise osv.except_osv(_('Invalid Process,'),
                     #               _('Proses Penilaian Kinerja Pegawai Tidak Bisa Dilanjutkan, Untuk Kategori Integritas Pegawai Minimal Mendapat Penghargaan Dari Atasan Langsung.'))
                     # if not task_obj.realisasi_kerjasama_atasan :
                     #    raise osv.except_osv(_('Invalid Process,'),
                     #               _('Proses Penilaian Kinerja Pegawai Tidak Bisa Dilanjutkan, Untuk Kategori Kerjasama Pegawai Minimal Melakukan Kerjasama Dengan Atasan Langsung.'))
                     # if not task_obj.realisasi_kepemimpinan_atasan :
                     #    raise osv.except_osv(_('Invalid Process,'),
                     #               _('Proses Penilaian Kinerja Pegawai Tidak Bisa Dilanjutkan, Untuk Kategori Kepemimpinan Pegawai Minimal Mendapat Penghargaan Kepemimpinan Dari Atasan Langsung.'))
                     
                    #ORIENTASI PELAYANAN
                     if task_obj.realisasi_jumlah_konsumen_pelayanan > 0 :
                        x = float (task_obj.realisasi_jumlah_konsumen_pelayanan)
                        y = float (task_obj.realisasi_jumlah_tidakpuas_pelayanan)
                        a = ((x - y) / x) * 100
                        #PENILAIAN TAMBAHAN JIKA KEPALA OPD
                        if task_obj.is_kepala_opd :
                            a_efisiensi=a_ukp4=a_spj=0
                            lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_nilai', '=', 'threshold'), ('active', '=', True), ('type', '=', 'orientasi')
                                                                                 ,('nilai_bawah', '<=', task_obj.realisasi_jumlah_konsumen_pelayanan ), ('nilai_atas', '>=', task_obj.realisasi_jumlah_konsumen_pelayanan)], context=None)
                            if lookup_nilai_id : 
                                lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                                a =  lookup_nilai.nilai_tunggal
                            if task_obj.realisasi_ketepatan_laporan_spj:
                                    a_spj=task_obj.realisasi_ketepatan_laporan_spj.nilai_tunggal
                            if task_obj.realisasi_ketepatan_laporan_ukp4:
                                    a_ukp4=task_obj.realisasi_ketepatan_laporan_ukp4.nilai_tunggal
                            if task_obj.realisasi_efisiensi_biaya_operasional:
                                    a_efisiensi=task_obj.realisasi_efisiensi_biaya_operasional.nilai_tunggal
                                
                            nilai_orientasi_pelayanan = a + a_efisiensi+a_ukp4+a_spj
                        else :
                            nilai_orientasi_pelayanan = a
                     
                     #print "Total Nilai nilai_rientasi_pelayanan : ", nilai_orientasi_pelayanan
                     if nilai_orientasi_pelayanan > 100 :
                         nilai_orientasi_pelayanan = 100;
                     # Komitment : =(H66/G66)*100
                     nilai_apel_pagi = nilai_upacara_hari_besar = 0
                     
                     if task_obj.realisasi_apel_pagi==0 or task_obj.realisasi_jumlah_jam_kerja==0 or task_obj.realisasi_jumlah_hari_kerja==0   :
                         raise osv.except_osv(_('Invalid Action, Data Inisiasi Tidak Lengkap'),
                                    _('Proses Penilaian Data Tidak Bisa Dilanjutkan, Silakan Klik Tombol Lookup Data Inisiasi. Jika Masih 0 Silakan Isi Di Menu Inisiasi Hari Kerja'))
                         
                     if task_obj.realisasi_apel_pagi > 0 :
                        x = float (task_obj.realisasi_hadir_apel_pagi)
                        y = float (task_obj.realisasi_apel_pagi)
                        a = (x / y) * 100
                        
                        nilai_apel_pagi = a
                        nilai_upacara_hari_besar = task_obj.realisasi_hadir_upacara_hari_besar
                        
                        if nilai_apel_pagi < 50.0 and  nilai_upacara_hari_besar == 0 :
                            nilai_komitment = (nilai_apel_pagi - 10) + nilai_upacara_hari_besar
                        else :
                            nilai_komitment = nilai_apel_pagi #+ nilai_upacara_hari_besar
                        #print "Nilai Komitment| Apel  : ", nilai_apel_pagi , "| Upacara :", nilai_upacara_hari_besar, " = ", nilai_komitment
                     if nilai_komitment > 100 :
                         nilai_komitment = 100;
                     # Disiplin : =(H68/G68)G68*100
                     nilai_hari_kerja = nilai_hadir_jam_kerja = 0
                     if task_obj.realisasi_hadir_hari_kerja > 0 and task_obj.realisasi_hadir_jam_kerja > 0 :
                          x = float (task_obj.realisasi_hadir_hari_kerja)
                          y = float (task_obj.realisasi_jumlah_hari_kerja)
                          a = (x / y) * 100
                          nilai_hari_kerja = a
                          x = float (task_obj.realisasi_hadir_jam_kerja)
                          y = float (task_obj.realisasi_jumlah_jam_kerja)
                          a = (x / y) * 100
                          nilai_hadir_jam_kerja = a
                          
                          nilai_disiplin = (nilai_hari_kerja + nilai_hadir_jam_kerja) / 2
                      #    print 'nilai_hari_kerja ', nilai_hari_kerja, ' dan jam kerja ', nilai_hadir_jam_kerja, " = ", nilai_disiplin
                     if nilai_disiplin > 100 :
                         nilai_disiplin = 100;
                     #INTEGRITAS!!!!!!!!!!!!!!!!!!!!!
                     integritas = 0
                     nilai_integritas_lainlain = nilai_integritas_atasan = nilai_integritas_kepalaopd = nilai_integritas_gubernur = nilai_integritas_presiden = 0
                     nilai_hukuman_disiplin=nilai_hukuman_ringan=nilai_hukuman_sedang=nilai_hukuman_berat=0
                     if task_obj.realisasi_integritas_atasan :
                         lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'atasan'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                         lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                         nilai_integritas = lookup_nilai.nilai_tunggal
                         integritas += 1
                     if task_obj.realisasi_integritas_presiden :
                        lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'presiden'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                        lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                        if task_obj.realisasi_integritas_atasan :
                            nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                        else :
                            nilai_integritas = lookup_nilai.nilai_tunggal  
                        integritas += 1
                     if task_obj.realisasi_integritas_gubernur :
                         lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'gubernur'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                         lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                         if integritas != 0 :
                            nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                         else :
                            nilai_integritas = lookup_nilai.nilai_tunggal  
                         integritas += 1
                     if task_obj.realisasi_integritas_kepalaopd :
                         lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'kepalaopd'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                         lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                         if integritas != 0 :
                            nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                         else :
                            nilai_integritas = lookup_nilai.nilai_tunggal  
                         integritas += 1
                     # if task_obj.realisasi_integritas_lainlain :
                     if task_obj.realisasi_integritas_es4 :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'pejabat_es4'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                             integritas += 1
                     if task_obj.realisasi_integritas_es3 :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'pejabat_es3'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                             integritas += 1
                     if task_obj.realisasi_integritas_es3 :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'pejabat_es2'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                             integritas += 1
                     if task_obj.realisasi_integritas_es1 :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'pejabat_es1'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_integritas = nilai_integritas + lookup_nilai.nilai_tambahan
                             integritas += 1
                     #HUKUMAN DISIPLIN
                     if task_obj.realisasi_integritas_hukuman and task_obj.realisasi_integritas_hukuman == 'tidak' :
                        lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'tidak_hukuman'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                        lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                        nilai_hukuman_disiplin = lookup_nilai.nilai_tunggal
                     elif task_obj.realisasi_integritas_hukuman and task_obj.realisasi_integritas_hukuman  == 'ya':
                         if task_obj.realisasi_integritas_hukuman_berat :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'hukuman_berat'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_hukuman_berat = lookup_nilai.nilai_tunggal
                         if task_obj.realisasi_integritas_hukuman_sedang :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'hukuman_sedang'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             if nilai_hukuman_berat == 0 :
                                nilai_hukuman_sedang = lookup_nilai.nilai_tunggal
                         if task_obj.realisasi_integritas_hukuman_ringan :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_integritas', '=', 'hukuman_ringan'), ('active', '=', True), ('type', '=', 'integritas')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             if nilai_hukuman_berat == 0  and nilai_hukuman_sedang == 0 :
                                nilai_hukuman_ringan = lookup_nilai.nilai_tunggal
                         nilai_hukuman_disiplin = nilai_hukuman_ringan + nilai_hukuman_sedang + nilai_hukuman_berat
                         
                         
                     #print "Nilai Integritas : ", nilai_integritas, " Dan  ", nilai_hukuman_disiplin, " -"
                     if nilai_integritas > 100 :
                         nilai_integritas = 100;
                     #nilai_integritas = nilai_integritas/10
                     nilai_integritas = nilai_hukuman_disiplin + nilai_integritas
                     #print "Total Nilai Integritas : ", nilai_integritas
                     if nilai_integritas > 100 :
                         nilai_integritas = 100;
                     # Kerja Sama
                     kerjasama = 0
                     nilai_kerjasama_lainlain = nilai_kerjasama_atasan = nilai_kerjasama_kepalaopd = nilai_kerjasama_gubernur = nilai_kerjasama_presiden = 0
                     if task_obj.realisasi_kerjasama_atasan :
                         lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'atasan'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                         lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                         nilai_kerjasama = lookup_nilai.nilai_tunggal
                         kerjasama += 1
                     if task_obj.realisasi_kerjasama_nasional :
                        lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'nasional'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                        lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                        if task_obj.realisasi_kerjasama_atasan :
                            nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                        else :
                            nilai_kerjasama = lookup_nilai.nilai_tunggal  
                        kerjasama += 1
                     if task_obj.realisasi_kerjasama_gubernur :
                         lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'provinsi'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                         lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                         if kerjasama != 0 :
                            nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                         else :
                            nilai_kerjasama = lookup_nilai.nilai_tunggal  
                         kerjasama += 1
                     if task_obj.realisasi_kerjasama_kepalaopd :
                         lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'perangkat_daerah'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                         lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                         if kerjasama != 0 :
                            nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                         else :
                            nilai_kerjasama = lookup_nilai.nilai_tunggal  
                         kerjasama += 1
                     
                     
                     if task_obj.realisasi_kerjasama_rapat_atasan :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'rapat_atasan'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                             kerjasama += 1
                     if task_obj.realisasi_kerjasama_rapat_perangkat_daerah :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'rapat_perangkat_daerah'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                             kerjasama += 1
                     if task_obj.realisasi_kerjasama_rapat_provinsi :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'rapat_provinsi'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                             kerjasama += 1
                     if task_obj.realisasi_kerjasama_rapat_nasional :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kerjasama', '=', 'rapat_nasional'), ('active', '=', True), ('type', '=', 'kerjasama')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_kerjasama = nilai_kerjasama + lookup_nilai.nilai_tambahan
                             kerjasama += 1
                    
                     #print "Nilai kerjasama : ", nilai_kerjasama, " Dari ", kerjasama, " Aspek"
                     if nilai_kerjasama > 100 :
                         nilai_kerjasama = 100;
                     
                    # Kepemimpinan
                    
                     kepemimpinan = 0
                     nilai_kepemimpinan_lainlain = nilai_kepemimpinan_atasan = nilai_kepemimpinan_kepalaopd = nilai_kepemimpinan_gubernur = nilai_kepemimpinan_presiden = 0
                     if job_type in ('struktural') :
                         if task_obj.realisasi_kepemimpinan_atasan :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'unitkerja'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             nilai_kepemimpinan = lookup_nilai.nilai_tunggal
                             kepemimpinan += 1
                         if task_obj.realisasi_kepemimpinan_nasional :
                            lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'nasional'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                            lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                            if task_obj.realisasi_kepemimpinan_atasan :
                                nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                            else :
                                nilai_kepemimpinan = lookup_nilai.nilai_tunggal  
                            kepemimpinan += 1
                         if task_obj.realisasi_kepemimpinan_gubernur :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'provinsi'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             if kepemimpinan != 0 :
                                nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                             else :
                                nilai_kepemimpinan = lookup_nilai.nilai_tunggal  
                             kepemimpinan += 1
                         if task_obj.realisasi_kepemimpinan_kepalaopd :
                             lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'perangkat_daerah'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                             lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                             if kepemimpinan != 0 :
                                nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                             else :
                                nilai_kepemimpinan = lookup_nilai.nilai_tunggal  
                             kepemimpinan += 1
                         # if task_obj.realisasi_kepemimpinan_lainlain :
                         if task_obj.realisasi_kepemimpinan_narsum_unitkerja :
                                 lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'narsum_unitkerja'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                                 lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                                 nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                                 kepemimpinan += 1
                         if task_obj.realisasi_kepemimpinan_narsum_perangkat_daerah :
                                 lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'narsum_perangkat_daerah'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                                 lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                                 nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                                 kepemimpinan += 1
                         if task_obj.realisasi_kepemimpinan_narsum_provinsi :
                                 lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'narsum_provinsi'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                                 lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                                 nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                                 kepemimpinan += 1
                         if task_obj.realisasi_kepemimpinan_narsum_nasional :
                                 lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_kepemimpinan', '=', 'narsum_nasional'), ('active', '=', True), ('type', '=', 'kepemimpinan')], context=None)
                                 lookup_nilai = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
                                 nilai_kepemimpinan = nilai_kepemimpinan + lookup_nilai.nilai_tambahan
                                 kepemimpinan += 1
                        
                         #print "Nilai kepemimpinan : ", nilai_kepemimpinan, " Dari ", kepemimpinan, " Aspek"
                         if nilai_kepemimpinan > 100 :
                             nilai_kepemimpinan = 100;
                     
                     #print "nilai_orientasi_pelayanan =", nilai_orientasi_pelayanan
                     #print "nilai_integritas =", nilai_integritas
                     #print "nilai_komitment=", nilai_komitment
                     #print "nilai_disiplin=", nilai_disiplin
                     #print "nilai_kerjasama=", nilai_kerjasama
                     #print "nilai_kepemimpinan=", nilai_kepemimpinan
                     jumlah_perhitungan = nilai_orientasi_pelayanan + nilai_integritas + nilai_komitment + nilai_disiplin + nilai_kerjasama + nilai_kepemimpinan
                     if job_type in ('struktural') :
                         nilai_akhir = jumlah_perhitungan / 6
                     else :
                         nilai_akhir = jumlah_perhitungan / 5
                     #print "Hasil : ", jumlah_perhitungan, " -> ", nilai_akhir
                # end if          
            update_poin = {
                                'nilai_akhir': nilai_akhir,
                                'indeks_nilai': self.get_value_poin(cr, uid, ids, nilai_akhir),
                                'jumlah_perhitungan':jumlah_perhitungan,
                                'nilai_pelayanan': nilai_orientasi_pelayanan,
                                'nilai_integritas': nilai_integritas,
                                'nilai_komitmen':nilai_komitment,
                                'nilai_disiplin': nilai_disiplin,
                                'nilai_kerjasama': nilai_kerjasama,
                                'nilai_kepemimpinan':nilai_kepemimpinan,
                                'nilai_tambahan': nilai_tambahan,
                                'nilai_kreatifitas':nilai_kreatifitas,
                                 }
            return update_poin;
            
        return False
    def do_task_poin_calculation_temporary(self, cr, uid, ids, context=None):
        return True
        update_poin = self.prepare_task_poin_calculation(cr, uid, ids, context=context)
        if update_poin:
            nilai_sementara = update_poin.get('nilai_akhir',0)
            self.write(cr, uid, ids, {
                                'nilai_sementara': nilai_sementara}
                       )
    def do_task_poin_calculation(self, cr, uid, ids, context=None):
        """ BKD->Done (Keuangan) """
        update_poin = self.prepare_task_poin_calculation(cr, uid, ids, context=context)
        if update_poin:
            self.write(cr, uid, ids, update_poin)
            
        return True
    def do_task_temp_poin_calculation(self, cr, uid, ids, context=None):
        """ Perhitungan Nilai Sementara """
        update_poin = self.prepare_task_poin_calculation(cr, uid, ids, context=context)
        if update_poin:
            nilai_sementara = update_poin.get('nilai_akhir',0)
            update_poin = {
                                'nilai_sementara': nilai_sementara,
                                '0': 0,
                                'jumlah_perhitungan':0,
                                'nilai_pelayanan': 0,
                                'nilai_integritas': 0,
                                'nilai_komitmen':0,
                                'nilai_disiplin': 0,
                                'nilai_kerjasama': 0,
                                'nilai_kepemimpinan':0,
                                'nilai_tambahan': 0,
                                'nilai_kreatifitas':0,
                                 }
            self.write(cr, uid, ids, update_poin)
            
        return True
    
    def do_task_summary_calculation(self, cr, uid, ids, in_sign, context=None):
        """ BKD->Done (Rekap Summary) """
        # Summary Calculation
        #print "do_task_summary_calculation"
        target_pool = self.pool.get('project.project')
        lookup_nilai_pool = self.pool.get('acuan.penailaian')
        skp_employee_pool = self.pool.get('skp.employee')
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            
            jumlah_perhitungan = 0
            nilai_dipa_apbn = nilai_dpa_biro = nilai_sotk = nilai_lain_lain = nilai_akhir = 0
            jml_dipa_apbn = jml_dpa_biro = jml_sotk = jml_lain_lain = 0
            nilai_kreatifitas = nilai_tambahan = nilai_pelayanan = nilai_integritas = nilai_komitmen = nilai_disiplin = nilai_kerjasama = nilai_kepemimpinan = 0
            sign = in_sign
            summary_target_type_id = False;
            if task_obj:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    jumlah_perhitungan = task_obj.jumlah_perhitungan * sign
                    nilai_akhir = task_obj.nilai_akhir * sign
                    summary_target_type_id = 'pokok'
                    if task_obj.target_type_id == 'dpa_opd_biro' :
                        nilai_dpa_biro = task_obj.nilai_akhir * sign
                        jml_dpa_biro = 1 * sign
                    if task_obj.target_type_id == 'dipa_apbn' :
                        nilai_dipa_apbn = task_obj.nilai_akhir * sign
                        jml_dipa_apbn = 1 * sign
                    if task_obj.target_type_id == 'sotk' :
                        nilai_sotk = task_obj.nilai_akhir * sign
                        jml_sotk = 1 * sign
                    if task_obj.target_type_id == 'lain_lain' :
                        nilai_lain_lain = task_obj.nilai_akhir * sign
                        jml_lain_lain = 1 * sign
                if task_obj.target_type_id in ('tambahan'):
                    jumlah_perhitungan = task_obj.jumlah_perhitungan * sign
                    # nilai_akhir=task_obj.nilai_akhir
                    nilai_tambahan = task_obj.nilai_akhir * sign
                    nilai_kreatifitas = task_obj.nilai_akhir * sign
                    summary_target_type_id = 'tambahan'
                if task_obj.target_type_id in ('perilaku'):
                    jumlah_perhitungan = task_obj.jumlah_perhitungan * sign
                    nilai_akhir = task_obj.nilai_akhir * sign
                    nilai_pelayanan = task_obj.nilai_pelayanan * sign
                    nilai_integritas = task_obj.nilai_integritas * sign
                    nilai_komitmen = task_obj.nilai_komitmen * sign
                    nilai_disiplin = task_obj.nilai_disiplin * sign
                    nilai_kerjasama = task_obj.nilai_kerjasama * sign
                    nilai_kepemimpinan = task_obj.nilai_kepemimpinan * sign
                    summary_target_type_id = 'perilaku'
                
                skp_employee_ids = skp_employee_pool.search(cr, uid, [('employee_id', '=', task_obj.employee_id.id),
                                                   ('target_period_year', '=', task_obj.target_period_year),
                                                   ('target_period_month', '=', task_obj.target_period_month),
                                                   # ('summary_target_type_id','=',summary_target_type_id)
                                                   ], context=None)
                if skp_employee_ids:
                    #print "Update.. ", skp_employee_ids
                    for skp_employee_obj in skp_employee_pool.browse(cr, uid, skp_employee_ids, context=None):
                        #print " skp_employee_obj : ", skp_employee_obj.id
                        if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                            jumlah_perhitungan = task_obj.jumlah_perhitungan
                            nilai_akhir = task_obj.nilai_akhir
                            summary_target_type_id = 'pokok'
                            if task_obj.target_type_id == 'dpa_opd_biro' :
                                #print " nilai_dpa_biro : ", nilai_dpa_biro
                                nilai_dpa_biro = nilai_dpa_biro + skp_employee_obj.nilai_dpa_biro
                                jml_dpa_biro = jml_dpa_biro + skp_employee_obj.jml_dpa_biro
                                values = {
                                'nilai_dpa_biro': nilai_dpa_biro,
                                'jml_dpa_biro':jml_dpa_biro,
                                }
                            if task_obj.target_type_id == 'dipa_apbn' :
                                nilai_dipa_apbn = nilai_dipa_apbn + skp_employee_obj.nilai_dipa_apbn
                                jml_dipa_apbn = jml_dipa_apbn + skp_employee_obj.jml_dipa_apbn
                                values = {
                                'nilai_dipa_apbn': nilai_dipa_apbn,
                                'jml_dipa_apbn': jml_dipa_apbn,
                                }
                            if task_obj.target_type_id == 'sotk' :
                                nilai_sotk = nilai_sotk + skp_employee_obj.nilai_sotk
                                jml_sotk = jml_sotk + skp_employee_obj.jml_sotk
                                values = {
                                'nilai_sotk':nilai_sotk,
                                'jml_sotk': jml_sotk,
                                }
                            if task_obj.target_type_id == 'lain_lain' :
                                nilai_lain_lain = nilai_lain_lain + skp_employee_obj.nilai_lain_lain
                                jml_lain_lain = jml_lain_lain + skp_employee_obj.jml_lain_lain
                                values = {
                                'nilai_lain_lain': nilai_lain_lain,
                                'jml_lain_lain':jml_lain_lain,
                                }
                        if task_obj.target_type_id in ('tambahan'):
                            nilai_tambahan = nilai_tambahan 
                            nilai_kreatifitas = nilai_kreatifitas 
                            values = {
                                'nilai_tambahan': nilai_tambahan,
                                'nilai_kreatifitas':nilai_kreatifitas,
                                }
                        if task_obj.target_type_id in ('perilaku'):
                            jumlah_perhitungan = task_obj.jumlah_perhitungan
                            nilai_pelayanan = nilai_pelayanan 
                            nilai_integritas = nilai_integritas
                            nilai_komitmen = nilai_komitmen 
                            nilai_disiplin = nilai_disiplin 
                            nilai_kerjasama = nilai_kerjasama
                            nilai_kepemimpinan = nilai_kepemimpinan 
                            values = {
                            'nilai_pelayanan': nilai_pelayanan,
                            'nilai_integritas': nilai_integritas,
                            'nilai_komitmen':nilai_komitmen,
                            'nilai_disiplin': nilai_disiplin,
                            'nilai_kerjasama': nilai_kerjasama,
                            'nilai_kepemimpinan':nilai_kepemimpinan,
                            }
                    #print "Values : ", sign, " > ", values
                    skp_employee_pool.write(cr, uid, skp_employee_obj.id, values, context=None)
                        
                else :
                    if sign == 1:
                        values = {
                            'employee_id': task_obj.employee_id.id,
                            'user_id': task_obj.user_id.id,
                            'target_period_year': task_obj.target_period_year,
                            'target_period_month':task_obj.target_period_month,
                            # 'summary_target_type_id':summary_target_type_id,
                            'nilai_akhir': nilai_akhir,
                            'jumlah_perhitungan': jumlah_perhitungan,
                            'nilai_dipa_apbn': nilai_dipa_apbn,
                            'nilai_dpa_biro': nilai_dpa_biro,
                            'nilai_sotk':nilai_sotk,
                            'nilai_lain_lain': nilai_lain_lain,
                            'jml_dipa_apbn': jml_dipa_apbn,
                            'jml_dpa_biro':jml_dpa_biro,
                            'jml_sotk': jml_sotk,
                            'jml_lain_lain':jml_lain_lain,
                            'nilai_tambahan': nilai_tambahan,
                            'nilai_kreatifitas':nilai_kreatifitas,
                            'nilai_pelayanan': nilai_pelayanan,
                            'nilai_integritas': nilai_integritas,
                            'nilai_komitmen':nilai_komitmen,
                            'nilai_disiplin': nilai_disiplin,
                            'nilai_kerjasama': nilai_kerjasama,
                            'nilai_kepemimpinan':nilai_kepemimpinan,
                        }
                        skp_employee_pool.create(cr , uid, values, context=None)
           
        return True;
    
    def do_recalculate_poin(self, cr, uid, ids, context=None):
        
         for task_obj in self.browse(cr, uid, ids, context=context):
             vals = {}
             update_poin = {
                                    'nilai_akhir': 0,
                                    'indeks_nilai': False,
                                    'jumlah_perhitungan':0,
                                    'nilai_pelayanan': 0,
                                    'nilai_integritas': 0,
                                    'nilai_komitmen':0,
                                    'nilai_disiplin': 0,
                                    'nilai_kerjasama': 0,
                                    'nilai_kepemimpinan':0,
                                     }
             self.do_task_summary_calculation(cr, uid, [task_obj.id], -1, context=context)
             self.write(cr, uid, [task_obj.id], update_poin)
             update_stage_state = {
                                'work_state': 'evaluated',
                                 }
             self.write(cr, uid, [task_obj.id], update_stage_state)
             #self.do_task_poin_calculation_temporary(cr,uid,[task_obj.id], context=context)
         return True;
# <!-- end workflow --> 
   
# Notification
    def do_target_done_notification(self, cr, uid, ids, context=None):
        """ BKD->Done (Keuangan) """
        #print "BKD->Done (Keuangan)...(Updated)"
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            mail_message_obj = self.pool.get('mail.message')
            vals = (
                    '<div> &nbsp; &nbsp; &bull; <b>Target Bulanan Telah Dibuat</b>: %s</div>'\
                    '' % ('-'))
            body_html = html_email_clean(vals)
            values = {
                    'body': body_html,
                    'model': 'project.task',
                    'record_name': task_obj.name,
                    'type': 'notification',
                    'res_id': ids[0],
                }
            message_id = mail_message_obj.create(cr, uid, values)
        return True

# mass work flow
    def action_mass_work_done(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task_obj = self.pool.get('project.task')
        #print "IDS : ", ids
        #print "COntext ", context

        # partner_id = move_line_obj.read(cr, uid, context['active_id'], ['partner_id'])['partner_id']
        # if partner_id:
           # res_partner_obj.write(cr, uid, partner_id[0], {'last_reconciliation_date': time.strftime('%Y-%m-%d')}, context)
        return {'type': 'ir.actions.act_window_close'}

# Proses
    def fill_task_automatically_with_target(self, cr, uid, ids, context=None):
        """ Jika selesai mebuat target. Maka secara default realisasi akan otomatis terisi dengan nilai target tersebit"""
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'realisasi_jumlah_kuantitas_output'     : task_obj.target_jumlah_kuantitas_output,
                                    'realisasi_satuan_kuantitas_output'     : task_obj.target_satuan_kuantitas_output.id or None,
                                    'realisasi_angka_kredit'     : task_obj.target_angka_kredit,
                                    'realisasi_kualitas'     : task_obj.target_kualitas,
                                    'realisasi_waktu'     : task_obj.target_waktu,
                                    'realisasi_satuan_waktu'     : task_obj.target_satuan_waktu,
                                    'realisasi_biaya'     : task_obj.target_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'realisasi_lainlain'     : task_obj.target_lainlain,
                                })
               
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    def fill_task_automatically_with_control(self, cr, uid, ids, context=None):
        """ Jika selesai mebuat target. Maka secara default realisasi akan otomatis terisi dengan nilai target tersebit"""
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj.is_suggest:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'realisasi_jumlah_kuantitas_output'     : task_obj.control_jumlah_kuantitas_output,
                                    'realisasi_satuan_kuantitas_output'     : task_obj.control_satuan_kuantitas_output.id or None,
                                    'realisasi_angka_kredit'                : task_obj.control_angka_kredit,
                                    'realisasi_kualitas'                    : task_obj.control_kualitas,
                                    'realisasi_waktu'                       : task_obj.control_waktu,
                                    'realisasi_satuan_waktu'                : task_obj.control_satuan_waktu,
                                    'realisasi_biaya'                       : task_obj.control_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'realisasi_lainlain'                    : task_obj.control_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                    
                                    'realisasi_tugas_tambahan'              : task_obj.control_tugas_tambahan,
                                    'realisasi_uraian_tugas_tambahan'       : task_obj.control_uraian_tugas_tambahan,
                                    'realisasi_rl_opd_tugas_tambahan'       : task_obj.control_rl_opd_tugas_tambahan,
                                    'realisasi_rl_gubernur_tugas_tambahan'  : task_obj.control_rl_gubernur_tugas_tambahan,
                                    'realisasi_rl_presiden_tugas_tambahan'  : task_obj.control_rl_presiden_tugas_tambahan,
                                    'realisasi_nilai_kreatifitas'           : task_obj.control_nilai_kreatifitas,
                                    'realisasi_uraian_kreatifitas'          : task_obj.control_uraian_kreatifitas,
                                    'realisasi_tupoksi_kreatifitas'         : task_obj.control_tupoksi_kreatifitas,
                                    'realisasi_rl_opd_kreatifitas'          : task_obj.control_rl_opd_kreatifitas,
                                    'realisasi_rl_gubernur_kreatifitas'     : task_obj.control_rl_gubernur_kreatifitas,
                                    'realisasi_rl_presiden_kreatifitas'     : task_obj.control_rl_presiden_kreatifitas,
                                    
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'realisasi_jumlah_konsumen_pelayanan'       : task_obj.control_jumlah_konsumen_pelayanan,
                                'realisasi_satuan_jumlah_konsumen_pelayanan': task_obj.control_satuan_jumlah_konsumen_pelayanan.id or None,
                                'realisasi_jumlah_tidakpuas_pelayanan'      : task_obj.control_jumlah_tidakpuas_pelayanan,
                                'realisasi_ketepatan_laporan_spj'           : task_obj.control_ketepatan_laporan_spj.id or None,
                                'realisasi_ketepatan_laporan_ukp4'          : task_obj.control_ketepatan_laporan_ukp4.id or None,
                                'realisasi_efisiensi_biaya_operasional'     : task_obj.control_efisiensi_biaya_operasional.id or None,
                                
                                'realisasi_apel_pagi'                       : task_obj.control_apel_pagi,
                                'realisasi_upacara_hari_besar'              : task_obj.control_upacara_hari_besar,
                                'realisasi_hadir_upacara_hari_besar'        : task_obj.control_hadir_upacara_hari_besar,
                                'realisasi_jumlah_hari_kerja'               : task_obj.control_jumlah_hari_kerja,
                                'realisasi_jumlah_jam_kerja'                : task_obj.control_jumlah_jam_kerja,
                                'realisasi_hadir_hari_kerja'                : task_obj.control_hadir_hari_kerja,
                                'realisasi_hadir_jam_kerja'                 : task_obj.control_hadir_jam_kerja,
                                'realisasi_hadir_apel_pagi'                 : task_obj.control_hadir_apel_pagi,
                                
                                'realisasi_integritas_presiden'             : task_obj.control_integritas_presiden,
                                'realisasi_integritas_gubernur'             : task_obj.control_integritas_gubernur,
                                'realisasi_integritas_kepalaopd'            : task_obj.control_integritas_kepalaopd,
                                'realisasi_integritas_atasan'               : task_obj.control_integritas_atasan,
                                'realisasi_integritas_es1'                  : task_obj.control_integritas_es1,
                                'realisasi_integritas_es2'                  : task_obj.control_integritas_es2,
                                'realisasi_integritas_es3'                  : task_obj.control_integritas_es3,
                                'realisasi_integritas_es4'                  : task_obj.control_integritas_es4,
                                
                                'realisasi_integritas_hukuman'              : task_obj.control_integritas_hukuman,
                                'realisasi_integritas_hukuman_ringan'       : task_obj.control_integritas_hukuman_ringan,
                                'realisasi_integritas_hukuman_sedang'       : task_obj.control_integritas_hukuman_sedang,
                                'realisasi_integritas_hukuman_berat'        : task_obj.control_integritas_hukuman_berat,
                                
                                'realisasi_kerjasama_nasional'              : task_obj.control_kerjasama_nasional,
                                'realisasi_kerjasama_gubernur'              : task_obj.control_kerjasama_gubernur,
                                'realisasi_kerjasama_kepalaopd'             : task_obj.control_kerjasama_kepalaopd,
                                'realisasi_kerjasama_atasan'                : task_obj.control_kerjasama_atasan,
                                'realisasi_kerjasama_rapat_nasional'        : task_obj.control_kerjasama_rapat_nasional,
                                'realisasi_kerjasama_rapat_provinsi'        : task_obj.control_kerjasama_rapat_provinsi,
                                'realisasi_kerjasama_rapat_perangkat_daerah': task_obj.control_kerjasama_rapat_perangkat_daerah,
                                'realisasi_kerjasama_rapat_atasan'          : task_obj.control_kerjasama_rapat_atasan,
                                
                                'realisasi_kepemimpinan_nasional'           : task_obj.control_kepemimpinan_nasional,
                                'realisasi_kepemimpinan_gubernur'           : task_obj.control_kepemimpinan_gubernur,
                                'realisasi_kepemimpinan_kepalaopd'          : task_obj.control_kepemimpinan_kepalaopd,
                                'realisasi_kepemimpinan_atasan'             :  task_obj.control_kepemimpinan_atasan,
                                'realisasi_kepemimpinan_narsum_nasional'    : task_obj.control_kepemimpinan_narsum_nasional,
                                'realisasi_kepemimpinan_narsum_provinsi'    : task_obj.control_kepemimpinan_narsum_provinsi,
                                'realisasi_kepemimpinan_narsum_perangkat_daerah': task_obj.control_kepemimpinan_narsum_perangkat_daerah,
                                'realisasi_kepemimpinan_narsum_unitkerja'   : task_obj.control_kepemimpinan_narsum_unitkerja,
                                })               
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    
    def fill_task_automatically_with_suggest(self, cr, uid, ids, context=None):
        """ Jika selesai mebuat target. Maka secara default realisasi akan otomatis terisi dengan nilai target tersebit"""
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj.is_suggest:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'realisasi_jumlah_kuantitas_output'     : task_obj.suggest_jumlah_kuantitas_output,
                                    'realisasi_satuan_kuantitas_output'     : task_obj.suggest_satuan_kuantitas_output.id or None,
                                    'realisasi_angka_kredit'                : task_obj.suggest_angka_kredit,
                                    'realisasi_kualitas'                    : task_obj.suggest_kualitas,
                                    'realisasi_waktu'                       : task_obj.suggest_waktu,
                                    'realisasi_satuan_waktu'                : task_obj.suggest_satuan_waktu,
                                    'realisasi_biaya'                       : task_obj.suggest_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'realisasi_lainlain'                    : task_obj.suggest_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                    
                                    'realisasi_tugas_tambahan'              : task_obj.suggest_tugas_tambahan,
                                    'realisasi_uraian_tugas_tambahan'       : task_obj.suggest_uraian_tugas_tambahan,
                                    'realisasi_rl_opd_tugas_tambahan'       : task_obj.suggest_rl_opd_tugas_tambahan,
                                    'realisasi_rl_gubernur_tugas_tambahan'  : task_obj.suggest_rl_gubernur_tugas_tambahan,
                                    'realisasi_rl_presiden_tugas_tambahan'  : task_obj.suggest_rl_presiden_tugas_tambahan,
                                    'realisasi_nilai_kreatifitas'           : task_obj.suggest_nilai_kreatifitas,
                                    'realisasi_uraian_kreatifitas'          : task_obj.suggest_uraian_kreatifitas,
                                    'realisasi_tupoksi_kreatifitas'         : task_obj.suggest_tupoksi_kreatifitas,
                                    'realisasi_rl_opd_kreatifitas'          : task_obj.suggest_rl_opd_kreatifitas,
                                    'realisasi_rl_gubernur_kreatifitas'     : task_obj.suggest_rl_gubernur_kreatifitas,
                                    'realisasi_rl_presiden_kreatifitas'     : task_obj.suggest_rl_presiden_kreatifitas,
                                    
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'realisasi_jumlah_konsumen_pelayanan'       : task_obj.suggest_jumlah_konsumen_pelayanan,
                                'realisasi_satuan_jumlah_konsumen_pelayanan': task_obj.suggest_satuan_jumlah_konsumen_pelayanan.id or None,
                                'realisasi_jumlah_tidakpuas_pelayanan'      : task_obj.suggest_jumlah_tidakpuas_pelayanan,
                                'realisasi_ketepatan_laporan_spj'           : task_obj.suggest_ketepatan_laporan_spj.id or None,
                                'realisasi_ketepatan_laporan_ukp4'          : task_obj.suggest_ketepatan_laporan_ukp4.id or None,
                                'realisasi_efisiensi_biaya_operasional'     : task_obj.suggest_efisiensi_biaya_operasional.id or None,
                                
                                'realisasi_apel_pagi'                       : task_obj.suggest_apel_pagi,
                                'realisasi_upacara_hari_besar'              : task_obj.suggest_upacara_hari_besar,
                                'realisasi_hadir_upacara_hari_besar'        : task_obj.suggest_hadir_upacara_hari_besar,
                                'realisasi_jumlah_hari_kerja'               : task_obj.suggest_jumlah_hari_kerja,
                                'realisasi_jumlah_jam_kerja'                : task_obj.suggest_jumlah_jam_kerja,
                                'realisasi_hadir_hari_kerja'                : task_obj.suggest_hadir_hari_kerja,
                                'realisasi_hadir_jam_kerja'                 : task_obj.suggest_hadir_jam_kerja,
                                'realisasi_hadir_apel_pagi'                 : task_obj.suggest_hadir_apel_pagi,
                                
                                'realisasi_integritas_presiden'             : task_obj.suggest_integritas_presiden,
                                'realisasi_integritas_gubernur'             : task_obj.suggest_integritas_gubernur,
                                'realisasi_integritas_kepalaopd'            : task_obj.suggest_integritas_kepalaopd,
                                'realisasi_integritas_atasan'               : task_obj.suggest_integritas_atasan,
                                'realisasi_integritas_es1'                  : task_obj.suggest_integritas_es1,
                                'realisasi_integritas_es2'                  : task_obj.suggest_integritas_es2,
                                'realisasi_integritas_es3'                  : task_obj.suggest_integritas_es3,
                                'realisasi_integritas_es4'                  : task_obj.suggest_integritas_es4,
                                
                                'realisasi_integritas_hukuman'              : task_obj.suggest_integritas_hukuman,
                                'realisasi_integritas_hukuman_ringan'       : task_obj.suggest_integritas_hukuman_ringan,
                                'realisasi_integritas_hukuman_sedang'       : task_obj.suggest_integritas_hukuman_sedang,
                                'realisasi_integritas_hukuman_berat'        : task_obj.suggest_integritas_hukuman_berat,
                                
                                'realisasi_kerjasama_nasional'              : task_obj.suggest_kerjasama_nasional,
                                'realisasi_kerjasama_gubernur'              : task_obj.suggest_kerjasama_gubernur,
                                'realisasi_kerjasama_kepalaopd'             : task_obj.suggest_kerjasama_kepalaopd,
                                'realisasi_kerjasama_atasan'                : task_obj.suggest_kerjasama_atasan,
                                'realisasi_kerjasama_rapat_nasional'        : task_obj.suggest_kerjasama_rapat_nasional,
                                'realisasi_kerjasama_rapat_provinsi'        : task_obj.suggest_kerjasama_rapat_provinsi,
                                'realisasi_kerjasama_rapat_perangkat_daerah': task_obj.suggest_kerjasama_rapat_perangkat_daerah,
                                'realisasi_kerjasama_rapat_atasan'          : task_obj.suggest_kerjasama_rapat_atasan,
                                
                                'realisasi_kepemimpinan_nasional'           : task_obj.suggest_kepemimpinan_nasional,
                                'realisasi_kepemimpinan_gubernur'           : task_obj.suggest_kepemimpinan_gubernur,
                                'realisasi_kepemimpinan_kepalaopd'          : task_obj.suggest_kepemimpinan_kepalaopd,
                                'realisasi_kepemimpinan_atasan'             :  task_obj.suggest_kepemimpinan_atasan,
                                'realisasi_kepemimpinan_narsum_nasional'    : task_obj.suggest_kepemimpinan_narsum_nasional,
                                'realisasi_kepemimpinan_narsum_provinsi'    : task_obj.suggest_kepemimpinan_narsum_provinsi,
                                'realisasi_kepemimpinan_narsum_perangkat_daerah': task_obj.suggest_kepemimpinan_narsum_perangkat_daerah,
                                'realisasi_kepemimpinan_narsum_unitkerja'   : task_obj.suggest_kepemimpinan_narsum_unitkerja,
                                })               
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
     
    def fill_task_automatically_with_appeal(self, cr, uid, ids, context=None):
        """ Jika selesai mebuat target. Maka secara default realisasi akan otomatis terisi dengan nilai target tersebit"""
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj.is_appeal:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'realisasi_jumlah_kuantitas_output'     : task_obj.appeal_jumlah_kuantitas_output,
                                    'realisasi_satuan_kuantitas_output'     : task_obj.appeal_satuan_kuantitas_output.id or None,
                                    'realisasi_angka_kredit'                : task_obj.appeal_angka_kredit,
                                    'realisasi_kualitas'                    : task_obj.appeal_kualitas,
                                    'realisasi_waktu'                       : task_obj.appeal_waktu,
                                    'realisasi_satuan_waktu'                : task_obj.appeal_satuan_waktu,
                                    'realisasi_biaya'                       : task_obj.appeal_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'realisasi_lainlain'                    : task_obj.appeal_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                    'realisasi_tugas_tambahan'     : task_obj.appeal_tugas_tambahan,
                                    'realisasi_uraian_tugas_tambahan'     : task_obj.appeal_uraian_tugas_tambahan,
                                    'realisasi_rl_opd_tugas_tambahan'     : task_obj.appeal_rl_opd_tugas_tambahan,
                                    'realisasi_rl_gubernur_tugas_tambahan'     : task_obj.appeal_rl_gubernur_tugas_tambahan,
                                    'realisasi_rl_presiden_tugas_tambahan'     : task_obj.appeal_rl_presiden_tugas_tambahan,
                                    'realisasi_nilai_kreatifitas'     : task_obj.appeal_nilai_kreatifitas,
                                    'realisasi_uraian_kreatifitas'     : task_obj.appeal_uraian_kreatifitas,
                                    'realisasi_tupoksi_kreatifitas'     : task_obj.appeal_tupoksi_kreatifitas,
                                    'realisasi_rl_opd_kreatifitas'     : task_obj.appeal_rl_opd_kreatifitas,
                                    'realisasi_rl_gubernur_kreatifitas'     : task_obj.appeal_rl_gubernur_kreatifitas,
                                    'realisasi_rl_presiden_kreatifitas'     : task_obj.appeal_rl_presiden_kreatifitas,
                                    
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'realisasi_jumlah_konsumen_pelayanan'       : task_obj.appeal_jumlah_konsumen_pelayanan,
                                'realisasi_satuan_jumlah_konsumen_pelayanan': task_obj.appeal_satuan_jumlah_konsumen_pelayanan.id or None,
                                'realisasi_jumlah_tidakpuas_pelayanan'      : task_obj.appeal_jumlah_tidakpuas_pelayanan,
                                'realisasi_ketepatan_laporan_spj'           : task_obj.appeal_ketepatan_laporan_spj.id or None,
                                'realisasi_ketepatan_laporan_ukp4'          : task_obj.appeal_ketepatan_laporan_ukp4.id or None,
                                'realisasi_efisiensi_biaya_operasional'     : task_obj.appeal_efisiensi_biaya_operasional.id or None,
                                
                                'realisasi_apel_pagi'     : task_obj.appeal_apel_pagi,
                                'realisasi_upacara_hari_besar': task_obj.appeal_upacara_hari_besar,
                                'realisasi_hadir_upacara_hari_besar': task_obj.appeal_hadir_upacara_hari_besar,
                                'realisasi_jumlah_hari_kerja'     : task_obj.appeal_jumlah_hari_kerja,
                                'realisasi_jumlah_jam_kerja': task_obj.appeal_jumlah_jam_kerja,
                                'realisasi_hadir_hari_kerja'     : task_obj.appeal_hadir_hari_kerja,
                                'realisasi_hadir_jam_kerja': task_obj.appeal_hadir_jam_kerja,
                                'realisasi_hadir_apel_pagi': task_obj.appeal_hadir_apel_pagi,
                                
                                'realisasi_integritas_presiden': task_obj.appeal_integritas_presiden,
                                'realisasi_integritas_gubernur': task_obj.appeal_integritas_gubernur,
                                'realisasi_integritas_kepalaopd': task_obj.appeal_integritas_kepalaopd,
                                'realisasi_integritas_atasan': task_obj.appeal_integritas_atasan,
                                'realisasi_integritas_es1': task_obj.appeal_integritas_es1,
                                'realisasi_integritas_es2': task_obj.appeal_integritas_es2,
                                'realisasi_integritas_es3': task_obj.appeal_integritas_es3,
                                'realisasi_integritas_es4': task_obj.appeal_integritas_es4,
                                
                                'realisasi_integritas_hukuman': task_obj.appeal_integritas_hukuman,
                                'realisasi_integritas_hukuman_ringan': task_obj.appeal_integritas_hukuman_ringan,
                                'realisasi_integritas_hukuman_sedang': task_obj.appeal_integritas_hukuman_sedang,
                                'realisasi_integritas_hukuman_berat': task_obj.appeal_integritas_hukuman_berat,
                                
                                'realisasi_kerjasama_nasional': task_obj.appeal_kerjasama_nasional,
                                'realisasi_kerjasama_gubernur': task_obj.appeal_kerjasama_gubernur,
                                'realisasi_kerjasama_kepalaopd': task_obj.appeal_kerjasama_kepalaopd,
                                'realisasi_kerjasama_atasan':task_obj.appeal_kerjasama_atasan,
                                'realisasi_kerjasama_rapat_nasional': task_obj.appeal_kerjasama_rapat_nasional,
                                'realisasi_kerjasama_rapat_provinsi': task_obj.appeal_kerjasama_rapat_provinsi,
                                'realisasi_kerjasama_rapat_perangkat_daerah': task_obj.appeal_kerjasama_rapat_perangkat_daerah,
                                'realisasi_kerjasama_rapat_atasan': task_obj.appeal_kerjasama_rapat_atasan,
                                
                                'realisasi_kepemimpinan_nasional': task_obj.appeal_kepemimpinan_nasional,
                                'realisasi_kepemimpinan_gubernur': task_obj.appeal_kepemimpinan_gubernur,
                                'realisasi_kepemimpinan_kepalaopd': task_obj.appeal_kepemimpinan_kepalaopd,
                                'realisasi_kepemimpinan_atasan':  task_obj.appeal_kepemimpinan_atasan,
                                'realisasi_kepemimpinan_narsum_nasional': task_obj.appeal_kepemimpinan_narsum_nasional,
                                'realisasi_kepemimpinan_narsum_provinsi': task_obj.appeal_kepemimpinan_narsum_provinsi,
                                'realisasi_kepemimpinan_narsum_perangkat_daerah': task_obj.appeal_kepemimpinan_narsum_perangkat_daerah,
                                'realisasi_kepemimpinan_narsum_unitkerja': task_obj.appeal_kepemimpinan_narsum_unitkerja,
                                })                  
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    
    def fill_task_appeal_automatically_with_suggest(self, cr, uid, ids, context=None):
        """ Jika selesai mebuat target. Maka secara default realisasi akan otomatis terisi dengan nilai target tersebit"""
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            
            if task_obj.is_suggest:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'appeal_jumlah_kuantitas_output'     : task_obj.suggest_jumlah_kuantitas_output,
                                    'appeal_satuan_kuantitas_output'     : task_obj.suggest_satuan_kuantitas_output.id or None,
                                    'appeal_angka_kredit'     : task_obj.suggest_angka_kredit,
                                    'appeal_kualitas'     : task_obj.suggest_kualitas,
                                    'appeal_waktu'     : task_obj.suggest_waktu,
                                    'appeal_satuan_waktu'     : task_obj.suggest_satuan_waktu,
                                    'appeal_biaya'     : task_obj.suggest_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'appeal_lainlain'     : task_obj.suggest_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                   
                                    'appeal_tugas_tambahan'     : task_obj.suggest_tugas_tambahan,
                                    'appeal_uraian_tugas_tambahan'     : task_obj.suggest_uraian_tugas_tambahan,
                                    'appeal_rl_opd_tugas_tambahan'     : task_obj.suggest_rl_opd_tugas_tambahan,
                                    'appeal_rl_gubernur_tugas_tambahan'     : task_obj.suggest_rl_gubernur_tugas_tambahan,
                                    'appeal_rl_presiden_tugas_tambahan'     : task_obj.suggest_rl_presiden_tugas_tambahan,
                                    'appeal_nilai_kreatifitas'     : task_obj.suggest_nilai_kreatifitas,
                                    'appeal_uraian_kreatifitas'     : task_obj.suggest_uraian_kreatifitas,
                                    'appeal_tupoksi_kreatifitas'     : task_obj.suggest_tupoksi_kreatifitas,
                                    'appeal_rl_opd_kreatifitas'     : task_obj.suggest_rl_opd_kreatifitas,
                                    'appeal_rl_gubernur_kreatifitas'     : task_obj.suggest_rl_gubernur_kreatifitas,
                                    'appeal_rl_presiden_kreatifitas'     : task_obj.suggest_rl_presiden_kreatifitas,
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'appeal_jumlah_konsumen_pelayanan'       : task_obj.suggest_jumlah_konsumen_pelayanan,
                                'appeal_satuan_jumlah_konsumen_pelayanan': task_obj.suggest_satuan_jumlah_konsumen_pelayanan.id or None,
                                'appeal_jumlah_tidakpuas_pelayanan'      : task_obj.suggest_jumlah_tidakpuas_pelayanan,
                                'appeal_ketepatan_laporan_spj'           : task_obj.suggest_ketepatan_laporan_spj.id or None,
                                'appeal_ketepatan_laporan_ukp4'          : task_obj.suggest_ketepatan_laporan_ukp4.id or None,
                                'appeal_efisiensi_biaya_operasional'     : task_obj.suggest_efisiensi_biaya_operasional.id or None,
                                
                                'appeal_apel_pagi'     : task_obj.suggest_apel_pagi,
                                'appeal_upacara_hari_besar': task_obj.suggest_upacara_hari_besar,
                                'appeal_hadir_upacara_hari_besar': task_obj.suggest_hadir_upacara_hari_besar,
                                'appeal_jumlah_hari_kerja'     : task_obj.suggest_jumlah_hari_kerja,
                                'appeal_jumlah_jam_kerja': task_obj.suggest_jumlah_jam_kerja,
                                'appeal_hadir_hari_kerja'     : task_obj.suggest_hadir_hari_kerja,
                                'appeal_hadir_jam_kerja': task_obj.suggest_hadir_jam_kerja,
                                'appeal_hadir_apel_pagi': task_obj.suggest_hadir_apel_pagi,
                                
                                'appeal_integritas_presiden': task_obj.suggest_integritas_presiden,
                                'appeal_integritas_gubernur': task_obj.suggest_integritas_gubernur,
                                'appeal_integritas_kepalaopd': task_obj.suggest_integritas_kepalaopd,
                                'appeal_integritas_atasan': task_obj.suggest_integritas_atasan,
                                'appeal_integritas_es1': task_obj.suggest_integritas_es1,
                                'appeal_integritas_es2': task_obj.suggest_integritas_es2,
                                'appeal_integritas_es3': task_obj.suggest_integritas_es3,
                                'appeal_integritas_es4': task_obj.suggest_integritas_es4,
                                
                                'appeal_integritas_hukuman': task_obj.suggest_integritas_hukuman,
                                'appeal_integritas_hukuman_ringan': task_obj.suggest_integritas_hukuman_ringan,
                                'appeal_integritas_hukuman_sedang': task_obj.suggest_integritas_hukuman_sedang,
                                'appeal_integritas_hukuman_berat': task_obj.suggest_integritas_hukuman_berat,
                                
                                'appeal_kerjasama_nasional': task_obj.suggest_kerjasama_nasional,
                                'appeal_kerjasama_gubernur': task_obj.suggest_kerjasama_gubernur,
                                'appeal_kerjasama_kepalaopd': task_obj.suggest_kerjasama_kepalaopd,
                                'appeal_kerjasama_atasan':task_obj.suggest_kerjasama_atasan,
                                'appeal_kerjasama_rapat_nasional': task_obj.suggest_kerjasama_rapat_nasional,
                                'appeal_kerjasama_rapat_provinsi': task_obj.suggest_kerjasama_rapat_provinsi,
                                'appeal_kerjasama_rapat_perangkat_daerah': task_obj.suggest_kerjasama_rapat_perangkat_daerah,
                                'appeal_kerjasama_rapat_atasan': task_obj.suggest_kerjasama_rapat_atasan,
                                
                                'appeal_kepemimpinan_nasional': task_obj.suggest_kepemimpinan_nasional,
                                'appeal_kepemimpinan_gubernur': task_obj.suggest_kepemimpinan_gubernur,
                                'appeal_kepemimpinan_kepalaopd': task_obj.suggest_kepemimpinan_kepalaopd,
                                'appeal_kepemimpinan_atasan':  task_obj.suggest_kepemimpinan_atasan,
                                'appeal_kepemimpinan_narsum_nasional': task_obj.suggest_kepemimpinan_narsum_nasional,
                                'appeal_kepemimpinan_narsum_provinsi': task_obj.suggest_kepemimpinan_narsum_provinsi,
                                'appeal_kepemimpinan_narsum_perangkat_daerah': task_obj.suggest_kepemimpinan_narsum_perangkat_daerah,
                                'appeal_kepemimpinan_narsum_unitkerja': task_obj.suggest_kepemimpinan_narsum_unitkerja,
                                })                     
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    def fill_suggest_automatically_with_task(self, cr, uid, ids, context=None):
        """ Default Suggest di isi task"""
        # = Not Use : appeal diisi oleh suggest
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            
            if task_obj.is_suggest:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'appeal_jumlah_kuantitas_output'     : task_obj.suggest_jumlah_kuantitas_output,
                                    'appeal_satuan_kuantitas_output'     : task_obj.suggest_satuan_kuantitas_output.id or None,
                                    'appeal_angka_kredit'     : task_obj.suggest_angka_kredit,
                                    'appeal_kualitas'     : task_obj.suggest_kualitas,
                                    'appeal_waktu'     : task_obj.suggest_waktu,
                                    'appeal_satuan_waktu'     : task_obj.suggest_satuan_waktu,
                                    'appeal_biaya'     : task_obj.suggest_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'appeal_lainlain'     : task_obj.suggest_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                    'appeal_tugas_tambahan'     : task_obj.suggest_tugas_tambahan,
                                    'appeal_uraian_tugas_tambahan'     : task_obj.suggest_uraian_tugas_tambahan,
                                    'appeal_rl_opd_tugas_tambahan'     : task_obj.suggest_rl_opd_tugas_tambahan,
                                    'appeal_rl_gubernur_tugas_tambahan'     : task_obj.suggest_rl_gubernur_tugas_tambahan,
                                    'appeal_rl_presiden_tugas_tambahan'     : task_obj.suggest_rl_presiden_tugas_tambahan,
                                    'appeal_nilai_kreatifitas'     : task_obj.suggest_nilai_kreatifitas,
                                    'appeal_uraian_kreatifitas'     : task_obj.suggest_uraian_kreatifitas,
                                    'appeal_tupoksi_kreatifitas'     : task_obj.suggest_tupoksi_kreatifitas,
                                    'appeal_rl_opd_kreatifitas'     : task_obj.suggest_rl_opd_kreatifitas,
                                    'appeal_rl_gubernur_kreatifitas'     : task_obj.suggest_rl_gubernur_kreatifitas,
                                    'appeal_rl_presiden_kreatifitas'     : task_obj.suggest_rl_presiden_kreatifitas,
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'appeal_jumlah_konsumen_pelayanan'       : task_obj.suggest_jumlah_konsumen_pelayanan,
                                'appeal_satuan_jumlah_konsumen_pelayanan': task_obj.suggest_satuan_jumlah_konsumen_pelayanan.id or None,
                                'appeal_jumlah_tidakpuas_pelayanan'      : task_obj.suggest_jumlah_tidakpuas_pelayanan,
                                'appeal_ketepatan_laporan_spj'           : task_obj.suggest_ketepatan_laporan_spj.id or None,
                                'appeal_ketepatan_laporan_ukp4'          : task_obj.suggest_ketepatan_laporan_ukp4.id or None,
                                'appeal_efisiensi_biaya_operasional'     : task_obj.suggest_efisiensi_biaya_operasional.id or None,
                                
                                'appeal_apel_pagi'     : task_obj.suggest_apel_pagi,
                                'appeal_upacara_hari_besar': task_obj.suggest_upacara_hari_besar,
                                'appeal_hadir_upacara_hari_besar': task_obj.suggest_hadir_upacara_hari_besar,
                                'appeal_jumlah_hari_kerja'     : task_obj.suggest_jumlah_hari_kerja,
                                'appeal_jumlah_jam_kerja': task_obj.suggest_jumlah_jam_kerja,
                                'appeal_hadir_hari_kerja'     : task_obj.suggest_hadir_hari_kerja,
                                'appeal_hadir_jam_kerja': task_obj.suggest_hadir_jam_kerja,
                                'appeal_hadir_apel_pagi': task_obj.suggest_hadir_apel_pagi,
                                
                                'appeal_integritas_presiden': task_obj.suggest_integritas_presiden,
                                'appeal_integritas_gubernur': task_obj.suggest_integritas_gubernur,
                                'appeal_integritas_kepalaopd': task_obj.suggest_integritas_kepalaopd,
                                'appeal_integritas_atasan': task_obj.suggest_integritas_atasan,
                                'appeal_integritas_es1': task_obj.suggest_integritas_es1,
                                'appeal_integritas_es2': task_obj.suggest_integritas_es2,
                                'appeal_integritas_es3': task_obj.suggest_integritas_es3,
                                'appeal_integritas_es4': task_obj.suggest_integritas_es4,
                                
                                'appeal_integritas_hukuman': task_obj.suggest_integritas_hukuman,
                                'appeal_integritas_hukuman_ringan': task_obj.suggest_integritas_hukuman_ringan,
                                'appeal_integritas_hukuman_sedang': task_obj.suggest_integritas_hukuman_sedang,
                                'appeal_integritas_hukuman_berat': task_obj.suggest_integritas_hukuman_berat,
                                
                                'appeal_kerjasama_nasional': task_obj.suggest_kerjasama_nasional,
                                'appeal_kerjasama_gubernur': task_obj.suggest_kerjasama_gubernur,
                                'appeal_kerjasama_kepalaopd': task_obj.suggest_kerjasama_kepalaopd,
                                'appeal_kerjasama_atasan':task_obj.suggest_kerjasama_atasan,
                                'appeal_kerjasama_rapat_nasional': task_obj.suggest_kerjasama_rapat_nasional,
                                'appeal_kerjasama_rapat_provinsi': task_obj.suggest_kerjasama_rapat_provinsi,
                                'appeal_kerjasama_rapat_perangkat_daerah': task_obj.suggest_kerjasama_rapat_perangkat_daerah,
                                'appeal_kerjasama_rapat_atasan': task_obj.suggest_kerjasama_rapat_atasan,
                                
                                'appeal_kepemimpinan_nasional': task_obj.suggest_kepemimpinan_nasional,
                                'appeal_kepemimpinan_gubernur': task_obj.suggest_kepemimpinan_gubernur,
                                'appeal_kepemimpinan_kepalaopd': task_obj.suggest_kepemimpinan_kepalaopd,
                                'appeal_kepemimpinan_atasan':  task_obj.suggest_kepemimpinan_atasan,
                                'appeal_kepemimpinan_narsum_nasional': task_obj.suggest_kepemimpinan_narsum_nasional,
                                'appeal_kepemimpinan_narsum_provinsi': task_obj.suggest_kepemimpinan_narsum_provinsi,
                                'appeal_kepemimpinan_narsum_perangkat_daerah': task_obj.suggest_kepemimpinan_narsum_perangkat_daerah,
                                'appeal_kepemimpinan_narsum_unitkerja': task_obj.suggest_kepemimpinan_narsum_unitkerja,
                                })               
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    def fill_control_automatically_with_task(self, cr, uid, ids, context=None):
        """ Default Suggest di isi task"""
        # = Not Use : appeal diisi oleh suggest
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            
            if task_obj.is_suggest:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'control_jumlah_kuantitas_output'     : task_obj.realisasi_jumlah_kuantitas_output,
                                    'control_satuan_kuantitas_output'     : task_obj.realisasi_satuan_kuantitas_output.id or None,
                                    'control_angka_kredit'     : task_obj.realisasi_angka_kredit,
                                    'control_kualitas'     : task_obj.realisasi_kualitas,
                                    'control_waktu'     : task_obj.realisasi_waktu,
                                    'control_satuan_waktu'     : task_obj.realisasi_satuan_waktu,
                                    'control_biaya'     : task_obj.realisasi_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'control_lainlain'     : task_obj.realisasi_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                    'control_tugas_tambahan'     : task_obj.realisasi_tugas_tambahan,
                                    'control_uraian_tugas_tambahan'     : task_obj.realisasi_uraian_tugas_tambahan,
                                    'control_rl_opd_tugas_tambahan'     : task_obj.realisasi_rl_opd_tugas_tambahan,
                                    'control_rl_gubernur_tugas_tambahan'     : task_obj.realisasi_rl_gubernur_tugas_tambahan,
                                    'control_rl_presiden_tugas_tambahan'     : task_obj.realisasi_rl_presiden_tugas_tambahan,
                                    'control_nilai_kreatifitas'     : task_obj.realisasi_nilai_kreatifitas,
                                    'control_uraian_kreatifitas'     : task_obj.realisasi_uraian_kreatifitas,
                                    'control_tupoksi_kreatifitas'     : task_obj.realisasi_tupoksi_kreatifitas,
                                    'control_rl_opd_kreatifitas'     : task_obj.realisasi_rl_opd_kreatifitas,
                                    'control_rl_gubernur_kreatifitas'     : task_obj.realisasi_rl_gubernur_kreatifitas,
                                    'control_rl_presiden_kreatifitas'     : task_obj.realisasi_rl_presiden_kreatifitas,
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'control_jumlah_konsumen_pelayanan'       : task_obj.realisasi_jumlah_konsumen_pelayanan,
                                'control_satuan_jumlah_konsumen_pelayanan': task_obj.realisasi_satuan_jumlah_konsumen_pelayanan.id or None,
                                'control_jumlah_tidakpuas_pelayanan'      : task_obj.realisasi_jumlah_tidakpuas_pelayanan,
                                'control_ketepatan_laporan_spj'           : task_obj.realisasi_ketepatan_laporan_spj.id or None,
                                'control_ketepatan_laporan_ukp4'          : task_obj.realisasi_ketepatan_laporan_ukp4.id or None,
                                'control_efisiensi_biaya_operasional'     : task_obj.realisasi_efisiensi_biaya_operasional.id or None,
                                
                                'control_apel_pagi'     : task_obj.realisasi_apel_pagi,
                                'control_upacara_hari_besar': task_obj.realisasi_upacara_hari_besar,
                                'control_hadir_upacara_hari_besar': task_obj.realisasi_hadir_upacara_hari_besar,
                                'control_jumlah_hari_kerja'     : task_obj.realisasi_jumlah_hari_kerja,
                                'control_jumlah_jam_kerja': task_obj.realisasi_jumlah_jam_kerja,
                                'control_hadir_hari_kerja'     : task_obj.realisasi_hadir_hari_kerja,
                                'control_hadir_jam_kerja': task_obj.realisasi_hadir_jam_kerja,
                                'control_hadir_apel_pagi': task_obj.realisasi_hadir_apel_pagi,
                                
                                'control_integritas_presiden': task_obj.realisasi_integritas_presiden,
                                'control_integritas_gubernur': task_obj.realisasi_integritas_gubernur,
                                'control_integritas_kepalaopd': task_obj.realisasi_integritas_kepalaopd,
                                'control_integritas_atasan': task_obj.realisasi_integritas_atasan,
                                'control_integritas_es1': task_obj.realisasi_integritas_es1,
                                'control_integritas_es2': task_obj.realisasi_integritas_es2,
                                'control_integritas_es3': task_obj.realisasi_integritas_es3,
                                'control_integritas_es4': task_obj.realisasi_integritas_es4,
                                
                                'control_integritas_hukuman': task_obj.realisasi_integritas_hukuman,
                                'control_integritas_hukuman_ringan': task_obj.realisasi_integritas_hukuman_ringan,
                                'control_integritas_hukuman_sedang': task_obj.realisasi_integritas_hukuman_sedang,
                                'control_integritas_hukuman_berat': task_obj.realisasi_integritas_hukuman_berat,
                                
                                'control_kerjasama_nasional': task_obj.realisasi_kerjasama_nasional,
                                'control_kerjasama_gubernur': task_obj.realisasi_kerjasama_gubernur,
                                'control_kerjasama_kepalaopd': task_obj.realisasi_kerjasama_kepalaopd,
                                'control_kerjasama_atasan':task_obj.realisasi_kerjasama_atasan,
                                'control_kerjasama_rapat_nasional': task_obj.realisasi_kerjasama_rapat_nasional,
                                'control_kerjasama_rapat_provinsi': task_obj.realisasi_kerjasama_rapat_provinsi,
                                'control_kerjasama_rapat_perangkat_daerah': task_obj.realisasi_kerjasama_rapat_perangkat_daerah,
                                'control_kerjasama_rapat_atasan': task_obj.realisasi_kerjasama_rapat_atasan,
                                
                                'control_kepemimpinan_nasional': task_obj.realisasi_kepemimpinan_nasional,
                                'control_kepemimpinan_gubernur': task_obj.realisasi_kepemimpinan_gubernur,
                                'control_kepemimpinan_kepalaopd': task_obj.realisasi_kepemimpinan_kepalaopd,
                                'control_kepemimpinan_atasan':  task_obj.realisasi_kepemimpinan_atasan,
                                'control_kepemimpinan_narsum_nasional': task_obj.realisasi_kepemimpinan_narsum_nasional,
                                'control_kepemimpinan_narsum_provinsi': task_obj.realisasi_kepemimpinan_narsum_provinsi,
                                'control_kepemimpinan_narsum_perangkat_daerah': task_obj.realisasi_kepemimpinan_narsum_perangkat_daerah,
                                'control_kepemimpinan_narsum_unitkerja': task_obj.realisasi_kepemimpinan_narsum_unitkerja,
                                })               
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    def fill_target_automatically_with_task(self, cr, uid, ids, context=None):
        """ Default Target di isi task"""
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
                vals = {}
            
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    vals.update({
                                    'suggest_jumlah_kuantitas_output'     : task_obj.realisasi_jumlah_kuantitas_output,
                                    'suggest_satuan_kuantitas_output'     : task_obj.realisasi_satuan_kuantitas_output.id or None,
                                    'suggest_angka_kredit'     : task_obj.realisasi_angka_kredit,
                                    'suggest_kualitas'     : task_obj.realisasi_kualitas,
                                    'suggest_waktu'     : task_obj.realisasi_waktu,
                                    'suggest_satuan_waktu'     : task_obj.realisasi_satuan_waktu,
                                    'suggest_biaya'     : task_obj.realisasi_biaya,
                                })
                if task_obj.target_type_id in ('lain_lain'):
                     vals.update({
                                    'suggest_lainlain'     : task_obj.realisasi_lainlain,
                                })
                if task_obj.target_type_id in ('tambahan'):
                     vals.update({
                                    'suggest_tugas_tambahan'     : task_obj.realisasi_tugas_tambahan,
                                    'suggest_uraian_tugas_tambahan'     : task_obj.realisasi_uraian_tugas_tambahan,
                                    'suggest_rl_opd_tugas_tambahan'     : task_obj.realisasi_rl_opd_tugas_tambahan,
                                    'suggest_rl_gubernur_tugas_tambahan'     : task_obj.realisasi_rl_gubernur_tugas_tambahan,
                                    'suggest_rl_presiden_tugas_tambahan'     : task_obj.realisasi_rl_presiden_tugas_tambahan,
                                    'suggest_nilai_kreatifitas'     : task_obj.realisasi_nilai_kreatifitas,
                                    'suggest_uraian_kreatifitas'     : task_obj.realisasi_uraian_kreatifitas,
                                    'suggest_tupoksi_kreatifitas'     : task_obj.realisasi_tupoksi_kreatifitas,
                                    'suggest_rl_opd_kreatifitas'     : task_obj.realisasi_rl_opd_kreatifitas,
                                    'suggest_rl_gubernur_kreatifitas'     : task_obj.realisasi_rl_gubernur_kreatifitas,
                                    'suggest_rl_presiden_kreatifitas'     : task_obj.realisasi_rl_presiden_kreatifitas,
                                })
                if task_obj.target_type_id in ('perilaku'):
                     vals.update({
                                'suggest_jumlah_konsumen_pelayanan'       : task_obj.realisasi_jumlah_konsumen_pelayanan,
                                'suggest_satuan_jumlah_konsumen_pelayanan': task_obj.realisasi_satuan_jumlah_konsumen_pelayanan.id or None,
                                'suggest_jumlah_tidakpuas_pelayanan'      : task_obj.realisasi_jumlah_tidakpuas_pelayanan,
                                'suggest_ketepatan_laporan_spj'           : task_obj.realisasi_ketepatan_laporan_spj.id or None,
                                'suggest_ketepatan_laporan_ukp4'          : task_obj.realisasi_ketepatan_laporan_ukp4.id or None,
                                'suggest_efisiensi_biaya_operasional'     : task_obj.realisasi_efisiensi_biaya_operasional.id or None,
                                
                                'suggest_apel_pagi'     : task_obj.realisasi_apel_pagi,
                                'suggest_upacara_hari_besar': task_obj.realisasi_upacara_hari_besar,
                                'suggest_hadir_upacara_hari_besar': task_obj.realisasi_hadir_upacara_hari_besar,
                                'suggest_jumlah_hari_kerja'     : task_obj.realisasi_jumlah_hari_kerja,
                                'suggest_jumlah_jam_kerja': task_obj.realisasi_jumlah_jam_kerja,
                                'suggest_hadir_hari_kerja'     : task_obj.realisasi_hadir_hari_kerja,
                                'suggest_hadir_jam_kerja': task_obj.realisasi_hadir_jam_kerja,
                                'suggest_hadir_apel_pagi': task_obj.realisasi_hadir_apel_pagi,
                                
                                'suggest_integritas_presiden': task_obj.realisasi_integritas_presiden,
                                'suggest_integritas_gubernur': task_obj.realisasi_integritas_gubernur,
                                'suggest_integritas_kepalaopd': task_obj.realisasi_integritas_kepalaopd,
                                'suggest_integritas_atasan': task_obj.realisasi_integritas_atasan,
                                'suggest_integritas_es1': task_obj.realisasi_integritas_es1,
                                'suggest_integritas_es2': task_obj.realisasi_integritas_es2,
                                'suggest_integritas_es3': task_obj.realisasi_integritas_es3,
                                'suggest_integritas_es4': task_obj.realisasi_integritas_es4,
                                
                                'suggest_integritas_hukuman': task_obj.realisasi_integritas_hukuman,
                                'suggest_integritas_hukuman_ringan': task_obj.realisasi_integritas_hukuman_ringan,
                                'suggest_integritas_hukuman_sedang': task_obj.realisasi_integritas_hukuman_sedang,
                                'suggest_integritas_hukuman_berat': task_obj.realisasi_integritas_hukuman_berat,
                                
                                'suggest_kerjasama_nasional': task_obj.realisasi_kerjasama_nasional,
                                'suggest_kerjasama_gubernur': task_obj.realisasi_kerjasama_gubernur,
                                'suggest_kerjasama_kepalaopd': task_obj.realisasi_kerjasama_kepalaopd,
                                'suggest_kerjasama_atasan':task_obj.realisasi_kerjasama_atasan,
                                'suggest_kerjasama_rapat_nasional': task_obj.realisasi_kerjasama_rapat_nasional,
                                'suggest_kerjasama_rapat_provinsi': task_obj.realisasi_kerjasama_rapat_provinsi,
                                'suggest_kerjasama_rapat_perangkat_daerah': task_obj.realisasi_kerjasama_rapat_perangkat_daerah,
                                'suggest_kerjasama_rapat_atasan': task_obj.realisasi_kerjasama_rapat_atasan,
                                
                                'suggest_kepemimpinan_nasional': task_obj.realisasi_kepemimpinan_nasional,
                                'suggest_kepemimpinan_gubernur': task_obj.realisasi_kepemimpinan_gubernur,
                                'suggest_kepemimpinan_kepalaopd': task_obj.realisasi_kepemimpinan_kepalaopd,
                                'suggest_kepemimpinan_atasan':  task_obj.realisasi_kepemimpinan_atasan,
                                'suggest_kepemimpinan_narsum_nasional': task_obj.realisasi_kepemimpinan_narsum_nasional,
                                'suggest_kepemimpinan_narsum_provinsi': task_obj.realisasi_kepemimpinan_narsum_provinsi,
                                'suggest_kepemimpinan_narsum_perangkat_daerah': task_obj.realisasi_kepemimpinan_narsum_perangkat_daerah,
                                'suggest_kepemimpinan_narsum_unitkerja': task_obj.realisasi_kepemimpinan_narsum_unitkerja,
                                })               
                # end if               
                self.write(cr, uid, [task_obj.id], vals, context)
        # end for
        return True
    def fill_target_perilaku(self, cr, uid, ids, context=None):
        """ Lookup ke objek hari_kerja_bulanan untuk isi data perilaku kategori komitment"""
        if not isinstance(ids, list): ids = [ids]
        komitmen_pool = self.pool.get('hari.kerja.bulanan')
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj:
                if task_obj.target_type_id == 'perilaku':
                    komitmen_ids = komitmen_pool.search(cr, uid, [('target_period_year', '=', task_obj.target_period_year), ('target_period_month', '=', task_obj.target_period_month)], context=None)
                    komitmen_objs = komitmen_pool.browse(cr, uid, komitmen_ids, context=context)
                    komitmen_obj = komitmen_objs and komitmen_objs[0] or False
                    if komitmen_obj:
                        #print "komitmen_obj : ", komitmen_obj.jumlah_apel_pagi
                        vals = {
                                        'realisasi_apel_pagi'     : komitmen_obj.jumlah_apel_pagi or 0,
                                        'realisasi_jumlah_hari_kerja'     : komitmen_obj.jumlah_hari_kerja or 0,
                                        'realisasi_jumlah_jam_kerja'     : komitmen_obj.jumlah_jam_kerja or 0,
                                        'realisasi_upacara_hari_besar'     : komitmen_obj.jumlah_upacara_hari_besar or 0,
                                    }
                        self.write(cr, uid, [task_obj.id], vals, context)
                # end if               
                    
        # end for
        return True
    def fill_lookup_perilaku_komitmen(self, cr, uid, ids, context=None):
        """ Lookup ke objek verifikasi_absen_pegawai  untuk isi data perilaku kategori komitmen"""
        if not isinstance(ids, list): ids = [ids]
        lookup_pool = self.pool.get('verifikasi.absen.pegawai')
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj:
                if task_obj.target_type_id == 'perilaku':
                    lookup_ids = lookup_pool.search(cr, uid, [('employee_id', '=', task_obj.employee_id.id), ('target_period_year', '=', task_obj.target_period_year), ('target_period_month', '=', task_obj.target_period_month)], context=None)
                    lookup_objs = lookup_pool.browse(cr, uid, lookup_ids, context=context)
                    lookup_obj = lookup_objs and lookup_objs[0] or False
                    if lookup_obj:
                        vals = {
                                        'lookup_apel_pagi'     : lookup_obj.jumlah_apel_pagi or 0,
                                        'lookup_jumlah_hari_kerja'     : lookup_obj.jumlah_hari_kerja or 0,
                                        'lookup_jumlah_jam_kerja'     : lookup_obj.jumlah_jam_kerja or 0,
                                        'lookup_upacara_hari_besar'     : lookup_obj.jumlah_upacara_hari_besar or 0,
                                    }
                        self.write(cr, uid, [task_obj.id], vals, context)
                # end if               
                    
        # end for
        return True
    def fill_lookup_inisiasi_perilaku_komitmen(self, cr, uid, ids, context=None):
        """ Lookup ke objek verifikasi_absen_pegawai  untuk isi data perilaku kategori komitmen"""
        if not isinstance(ids, list): ids = [ids]
        lookup_pool = self.pool.get('hari.kerja.bulanan')
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj:
                if task_obj.target_type_id == 'perilaku':
                    lookup_ids = lookup_pool.search(cr, uid, [ ('target_period_year', '=', task_obj.target_period_year), ('target_period_month', '=', task_obj.target_period_month)], context=None)
                    lookup_objs = lookup_pool.browse(cr, uid, lookup_ids, context=context)
                    lookup_obj = lookup_objs and lookup_objs[0] or False
                    if lookup_obj:
                        vals = {
                                        'realisasi_apel_pagi'     : lookup_obj.jumlah_apel_pagi or 0,
                                        'realisasi_jumlah_hari_kerja'     : lookup_obj.jumlah_hari_kerja or 0,
                                        'realisasi_jumlah_jam_kerja'     : lookup_obj.jumlah_jam_kerja or 0,
                                        'realisasi_upacara_hari_besar'     : lookup_obj.jumlah_upacara_hari_besar or 0,
                                    }
                        self.write(cr, uid, [task_obj.id], vals, context)
                # end if               
                    
        # end for
        return True
    def fill_lookup_verifikasi_biaya(self, cr, uid, ids, context=None):
        """ Lookup ke objek Data Kegiatan  untuk isi data verifikasi Biaya"""
        if not isinstance(ids, list): ids = [ids]
        lookup_pool = self.pool.get('kegiatan.pemprov')
        for task_obj in self.browse(cr, uid, ids, context=context):
            vals = {}
            if task_obj:
                if task_obj.target_type_id in ('dipa_apbn', 'dpa_opd_biro', 'sotk', 'lain_lain'):
                    code = task_obj.code;
                    # print task_obj.code, " - ",task_obj.target_type_id," - ", task_obj.target_period_month,task_obj.target_period_year
                    if code and len(code) > 0 :
                        lookup_ids = lookup_pool.search(cr, uid, [('code', '=', task_obj.code),
                                                              ('target_category', '=', task_obj.target_category),  # ('target_type_id','=',task_obj.target_period_year)
                                                              ('period_year', '=', task_obj.target_period_year),
                                                              ('period_month', '=', task_obj.target_period_month),
                                                              ('active', '=', True)], context=None)
                    elif not code :
                        lookup_ids = lookup_pool.search(cr, uid, [('name', '=', task_obj.name),
                                                              ('target_category', '=', task_obj.target_category),  # ('target_type_id','=',task_obj.target_period_year)
                                                              ('period_year', '=', task_obj.target_period_year),
                                                              ('period_month', '=', task_obj.target_period_month),
                                                              ('active', '=', True)], context=None)
                    else :
                        lookup_ids = lookup_pool.search(cr, uid, [('code', '=', task_obj.code), ('name', '=', task_obj.name),
                                                                  ('target_category', '=', task_obj.target_category),  # ('target_type_id','=',task_obj.target_period_year)
                                                                  ('period_year', '=', task_obj.target_period_year),
                                                                  ('period_month', '=', task_obj.target_period_month),
                                                                  ('active', '=', True)], context=None)
                    lookup_objs = lookup_pool.browse(cr, uid, lookup_ids, context=context)
                    lookup_obj = lookup_objs and lookup_objs[0] or False
                    if lookup_obj:
                        vals = {
                                        'lookup_biaya'     : lookup_obj.control_biaya or 0,
                                    }
                        self.write(cr, uid, [task_obj.id], vals, context)
                # end if               
        # end for
        return True
    def delete_realisasi(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for task_obj in self.browse(cr, uid, ids, context=context):
            if task_obj.project_id:
                raise osv.except_osv(_('Invalid Action!'),
                                             _('Data Realisasi Tidak Bisa Dihapus.'))
            
        self.unlink(cr, uid, ids, context=None) 
        
        return {
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'notification.delete.task',
                    'target': 'new',
                    'context': context,  # ['notif_booking'],
                }
        return True;
task()



