from openerp.osv import fields, osv
from datetime import datetime,timedelta
import time
from mx import DateTime

# ====================== Popup Class Object ================================= #

class project_task_propose_rejected(osv.Model):
    _name = 'project.task.propose.rejected'
    _description = 'SKP Ditolak Atasan'
    _columns = {
        'is_suggest': fields.boolean('Tambahkan Koreski Penilaian'),
        'notes'      : fields.text('Catatan Koreksi',required=True),
        'jumlah_kuantitas_output'     : fields.integer('Kuantitas Output', required=True),
        'satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output', required=True),
        'angka_kredit'     : fields.float('Angka Kredit', readonly=False),
        'kualitas'     : fields.float('Kualitas', required=True),
        'waktu'     : fields.integer('Waktu', required=True),
        'satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1, required=True),
        'biaya'     : fields.float('Biaya', readonly=False),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
       
    }
    def action_propose_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        
        vals.update({  'suggest_jumlah_kuantitas_output'     : task_obj.jumlah_kuantitas_output,
                                    'suggest_satuan_kuantitas_output'     : task_obj.satuan_kuantitas_output.id or None,
                                    'suggest_angka_kredit'     : task_obj.angka_kredit,
                                    'suggest_kualitas'     : task_obj.kualitas,
                                    'suggest_waktu'     : task_obj.waktu,
                                    'suggest_satuan_waktu'     : task_obj.satuan_waktu,
                                    'suggest_biaya'     : task_obj.biaya,
                                    'is_suggest' : True,
                                    'notes_atasan' : task_obj.notes,
                                    'work_state':'rejected_manager',
                                     })
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        
    
project_task_propose_rejected()

class project_task_appeal_rejected(osv.Model):
    _name = 'project.task.appeal.rejected'
    _description = 'SKP, Ditolak Banding'
    _columns = {
        'is_appeal': fields.boolean('Tambahkan Koreski Penilaian'),
        'notes'      : fields.text('Catatan Koreksi',required=True),
        'jumlah_kuantitas_output'     : fields.integer('Kuantitas Output', required=True),
        'satuan_kuantitas_output'     : fields.many2one('satuan.hitung', 'Jenis Kuantitas Output', required=True),
        'angka_kredit'     : fields.float('Angka Kredit', readonly=False),
        'kualitas'     : fields.float('Kualitas', required=True),
        'waktu'     : fields.integer('Waktu', required=True),
        'satuan_waktu'     : fields.selection([('hari', 'Hari')], 'Satuan Waktu', select=1, required=True),
        'biaya'     : fields.float('Biaya', readonly=False),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
       
    }
    def action_appeal_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        vals.update({  'appeal_jumlah_kuantitas_output'     : task_obj.jumlah_kuantitas_output,
                                    'appeal_satuan_kuantitas_output'     : task_obj.satuan_kuantitas_output.id or None,
                                    'appeal_angka_kredit'     : task_obj.angka_kredit,
                                    'appeal_kualitas'     : task_obj.kualitas,
                                    'appeal_waktu'     : task_obj.waktu,
                                    'appeal_satuan_waktu'     : task_obj.satuan_waktu,
                                    'appeal_biaya'     : task_obj.biaya,
                                    'is_appeal' : True,
                                    'notes_atasan_banding' : task_obj.notes,
                                    #'work_state':'evaluated',
                                     })
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        task_pool.fill_task_automatically_with_appeal(cr, uid, [task_obj.task_id.id], context);
        task_pool.write(cr, uid, [task_obj.task_id.id],  {'work_state': 'evaluated'}, context)
    
project_task_appeal_rejected()

class project_task_perilaku_propose_rejected(osv.Model):
    _name = 'project.task.perilaku.propose.rejected'
    _description = 'Perilaku Ditolak Atasan'
    _columns = {
        'is_suggest': fields.boolean('Tambahkan Koreski Penilaian'),
        'notes'      : fields.text('Catatan Koreksi',required=True),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
        'target_type_id': fields.selection([ ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),
                                            ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang Sotk Opd/Biro'),
                                                      ('lain_lain', 'Lain-Lain'),
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')], 'Jenis Kegiatan', readonly=True
                                                     ),
      
        'jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Pelayanan',required=True),
        'jumlah_tidakpuas_pelayanan'     : fields.integer('Jumlah Ketidakpuasan Pelayanan',required=True),
        'satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen',required=True),
        'ketepatan_laporan_spj'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan SPJ', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_spj'),('active', '=', True)] ),
        'ketepatan_laporan_ukp4'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan UKP4', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_ukp4'),('active', '=', True)] ), 
        'efisiensi_biaya_operasional'     : fields.many2one('acuan.penailaian', 'Efisiensi Biaya Operasional Kantor', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'efisiensi_biaya_operasional'),('active', '=', True)] ),
        
        'integritas_presiden': fields.boolean('Presiden'),
        'integritas_gubernur': fields.boolean('Gubernur'),
        'integritas_kepalaopd': fields.boolean('Kepala OPD'),
        'integritas_atasan': fields.boolean('Atasan Langsung'),
        'integritas_lainlain': fields.boolean('Lain Lain'),
        'integritas_es1': fields.boolean('Pejabat Eselon I'),
        'integritas_es2': fields.boolean('Pejabat Eselon II'),
        'integritas_es3': fields.boolean('Pejabat Eselon III'),
        'integritas_es4': fields.boolean('Pejabat Eselon IV'),
        'integritas_hukuman': fields.selection([('ya', 'Terkena Hukuman Disiplin'), ('tidak', 'Tidak Terkena Hukuman Disiplin')],'Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Atau Tidak " ,required=True),
        'integritas_hukuman_ringan': fields.boolean('Ringan'),
        'integritas_hukuman_sedang': fields.boolean('Sedang'),
        'integritas_hukuman_berat': fields.boolean('Berat'),
        'hadir_apel_pagi'     : fields.integer('Kehadiran Apel Pagi',required=True),
        'hadir_hari_kerja'     : fields.integer('Kehadiran Hari Kerja',required=True),
        'hadir_jam_kerja': fields.integer('Kehadiran Jam Kerja',required=True),
        'hadir_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar',required=True),
        'kerjasama_nasional': fields.boolean('Nasional'),
        'kerjasama_gubernur': fields.boolean('Provinsi'),
        'kerjasama_kepalaopd': fields.boolean('OPD'),
        'kerjasama_atasan': fields.boolean('Atasan Langsung'),
        'kerjasama_lainlain': fields.boolean('Lain Lain'),
        'kerjasama_rapat_atasan': fields.boolean('Rapat Atasan Langsung'),
        'kerjasama_rapat_perangkat_daerah': fields.boolean('Rapat Perangkat Daerah'),
        'kerjasama_rapat_provinsi': fields.boolean('Rapat Provinsi'),
        'kerjasama_rapat_nasional': fields.boolean('Rapat Nasional'),
        'kepemimpinan_nasional': fields.boolean('Nasional'),
        'kepemimpinan_gubernur': fields.boolean('Provinsi'),
        'kepemimpinan_kepalaopd': fields.boolean('OPD'),
        'kepemimpinan_atasan': fields.boolean('Atasan Langsung'),
        'kepemimpinan_lainlain': fields.boolean('Lain Lain'),
        'kepemimpinan_narsum_unitkerja': fields.boolean('Narasumber Kerja Atasan Langsung'),
        'kepemimpinan_narsum_perangkat_daerah': fields.boolean('Narasumber Perangkat Daerah'),
        'kepemimpinan_narsum_provinsi': fields.boolean('Narasumber Provinsi'),
        'kepemimpinan_narsum_nasional': fields.boolean('Narasumber Nasional'),
        'is_kepala_opd': fields.boolean('Kepala OPD'),
        'employee_job_type':fields.char('Jenis Jabatan',size=50)
       
    }
    def action_perilaku_propose_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        vals.update({
                                'suggest_jumlah_konsumen_pelayanan'       : task_obj.jumlah_konsumen_pelayanan,
                                'suggest_satuan_jumlah_konsumen_pelayanan': task_obj.satuan_jumlah_konsumen_pelayanan.id or None,
                                'suggest_jumlah_tidakpuas_pelayanan'      : task_obj.jumlah_tidakpuas_pelayanan,
                                'suggest_ketepatan_laporan_spj'           : task_obj.ketepatan_laporan_spj.id or None,
                                'suggest_ketepatan_laporan_ukp4'          : task_obj.ketepatan_laporan_ukp4.id or None,
                                'suggest_efisiensi_biaya_operasional'     : task_obj.efisiensi_biaya_operasional.id or None,
                                
                                'suggest_hadir_upacara_hari_besar': task_obj.hadir_upacara_hari_besar,
                                'suggest_hadir_hari_kerja'     : task_obj.hadir_hari_kerja,
                                'suggest_hadir_jam_kerja': task_obj.hadir_jam_kerja,
                                'suggest_hadir_apel_pagi': task_obj.hadir_apel_pagi,
                                
                                'suggest_integritas_presiden': task_obj.integritas_presiden,
                                'suggest_integritas_gubernur': task_obj.integritas_gubernur,
                                'suggest_integritas_kepalaopd': task_obj.integritas_kepalaopd,
                                'suggest_integritas_atasan': task_obj.integritas_atasan,
                                'suggest_integritas_es1': task_obj.integritas_es1,
                                'suggest_integritas_es2': task_obj.integritas_es2,
                                'suggest_integritas_es3': task_obj.integritas_es3,
                                'suggest_integritas_es4': task_obj.integritas_es4,
                                
                                'suggest_integritas_hukuman': task_obj.integritas_hukuman,
                                'suggest_integritas_hukuman_ringan': task_obj.integritas_hukuman_ringan,
                                'suggest_integritas_hukuman_sedang': task_obj.integritas_hukuman_sedang,
                                'suggest_integritas_hukuman_berat': task_obj.integritas_hukuman_berat,
                                
                                'suggest_kerjasama_nasional': task_obj.kerjasama_nasional,
                                'suggest_kerjasama_gubernur': task_obj.kerjasama_gubernur,
                                'suggest_kerjasama_kepalaopd': task_obj.kerjasama_kepalaopd,
                                'suggest_kerjasama_atasan':task_obj.kerjasama_atasan,
                                'suggest_kerjasama_rapat_nasional': task_obj.kerjasama_rapat_nasional,
                                'suggest_kerjasama_rapat_provinsi': task_obj.kerjasama_rapat_provinsi,
                                'suggest_kerjasama_rapat_perangkat_daerah': task_obj.kerjasama_rapat_perangkat_daerah,
                                'suggest_kerjasama_rapat_atasan': task_obj.kerjasama_rapat_atasan,
                                
                                'suggest_kepemimpinan_nasional': task_obj.kepemimpinan_nasional,
                                'suggest_kepemimpinan_gubernur': task_obj.kepemimpinan_gubernur,
                                'suggest_kepemimpinan_kepalaopd': task_obj.kepemimpinan_kepalaopd,
                                'suggest_kepemimpinan_atasan':  task_obj.kepemimpinan_atasan,
                                'suggest_kepemimpinan_narsum_nasional': task_obj.kepemimpinan_narsum_nasional,
                                'suggest_kepemimpinan_narsum_provinsi': task_obj.kepemimpinan_narsum_provinsi,
                                'suggest_kepemimpinan_narsum_perangkat_daerah': task_obj.kepemimpinan_narsum_perangkat_daerah,
                                'suggest_kepemimpinan_narsum_unitkerja': task_obj.kepemimpinan_narsum_unitkerja,
                                
                                'is_suggest' : True,
                                'notes_atasan' : task_obj.notes,
                                'work_state':'rejected_manager',
                                })               
                # end if           
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        
    
project_task_perilaku_propose_rejected()
class project_task_perilaku_appeal_rejected(osv.Model):
    _name = 'project.task.perilaku.appeal.rejected'
    _description = 'Perilaku Ditolak Banding'
    _columns = {
        'is_appeal': fields.boolean('Tambahkan Koreski Penilaian'),
        'notes'      : fields.text('Catatan Koreksi',required=True),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
        'target_type_id': fields.selection([ ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),
                                            ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang Sotk Opd/Biro'),
                                                      ('lain_lain', 'Lain-Lain'),
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')], 'Jenis Kegiatan', readonly=True
                                                     ),
      
        'jumlah_konsumen_pelayanan'     : fields.integer('Jumlah Pelayanan',required=True),
        'jumlah_tidakpuas_pelayanan'     : fields.integer('Jumlah Ketidakpuasan Pelayanan',required=True),
        'satuan_jumlah_konsumen_pelayanan': fields.many2one('satuan.hitung', 'Satuan Nilai Konsumen',required=True),
        'ketepatan_laporan_spj'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan SPJ', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_spj'),('active', '=', True)] ),
        'ketepatan_laporan_ukp4'     : fields.many2one('acuan.penailaian', 'Ketepatan Laporan UKP4', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'ketepatan_laporan_ukp4'),('active', '=', True)] ), 
        'efisiensi_biaya_operasional'     : fields.many2one('acuan.penailaian', 'Efisiensi Biaya Operasional Kantor', domain=[('type', '=', 'orientasi'),('kategori_orientasi', '=', 'efisiensi_biaya_operasional'),('active', '=', True)] ),
        
        'integritas_presiden': fields.boolean('Presiden'),
        'integritas_gubernur': fields.boolean('Gubernur'),
        'integritas_kepalaopd': fields.boolean('Kepala OPD'),
        'integritas_atasan': fields.boolean('Atasan Langsung'),
        'integritas_lainlain': fields.boolean('Lain Lain'),
        'integritas_es1': fields.boolean('Pejabat Eselon I'),
        'integritas_es2': fields.boolean('Pejabat Eselon II'),
        'integritas_es3': fields.boolean('Pejabat Eselon III'),
        'integritas_es4': fields.boolean('Pejabat Eselon IV'),
        'integritas_hukuman': fields.selection([('ya', 'Terkena Hukuman Disiplin'), ('tidak', 'Tidak Terkena Hukuman Disiplin')],'Ada Hukuman Disiplin',help="Jika Ada Hukuman Disiplin, Atau Tidak " ,required=True),
        'integritas_hukuman_ringan': fields.boolean('Ringan'),
        'integritas_hukuman_sedang': fields.boolean('Sedang'),
        'integritas_hukuman_berat': fields.boolean('Berat'),
        'hadir_apel_pagi'     : fields.integer('Kehadiran Apel Pagi',required=True),
        'hadir_hari_kerja'     : fields.integer('Kehadiran Hari Kerja',required=True),
        'hadir_jam_kerja': fields.integer('Kehadiran Jam Kerja',required=True),
        'hadir_upacara_hari_besar': fields.integer('Kehadiran Upacara Hari Besar',required=True),
        'kerjasama_nasional': fields.boolean('Nasional'),
        'kerjasama_gubernur': fields.boolean('Provinsi'),
        'kerjasama_kepalaopd': fields.boolean('OPD'),
        'kerjasama_atasan': fields.boolean('Atasan Langsung'),
        'kerjasama_lainlain': fields.boolean('Lain Lain'),
        'kerjasama_rapat_atasan': fields.boolean('Rapat Atasan Langsung'),
        'kerjasama_rapat_perangkat_daerah': fields.boolean('Rapat Perangkat Daerah'),
        'kerjasama_rapat_provinsi': fields.boolean('Rapat Provinsi'),
        'kerjasama_rapat_nasional': fields.boolean('Rapat Nasional'),
        'kepemimpinan_nasional': fields.boolean('Nasional'),
        'kepemimpinan_gubernur': fields.boolean('Provinsi'),
        'kepemimpinan_kepalaopd': fields.boolean('OPD'),
        'kepemimpinan_atasan': fields.boolean('Atasan Langsung'),
        'kepemimpinan_lainlain': fields.boolean('Lain Lain'),
        'kepemimpinan_narsum_unitkerja': fields.boolean('Narasumber Kerja Atasan Langsung'),
        'kepemimpinan_narsum_perangkat_daerah': fields.boolean('Narasumber Perangkat Daerah'),
        'kepemimpinan_narsum_provinsi': fields.boolean('Narasumber Provinsi'),
        'kepemimpinan_narsum_nasional': fields.boolean('Narasumber Nasional'),
        'is_kepala_opd': fields.boolean('Kepala OPD'),
        'employee_job_type':fields.char('Jenis Jabatan',size=50)
       
    }
    def action_perilaku_appeal_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Banding Perilaku Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        vals.update({
                                'appeal_jumlah_konsumen_pelayanan'       : task_obj.jumlah_konsumen_pelayanan,
                                'appeal_satuan_jumlah_konsumen_pelayanan': task_obj.satuan_jumlah_konsumen_pelayanan.id or None,
                                'appeal_jumlah_tidakpuas_pelayanan'      : task_obj.jumlah_tidakpuas_pelayanan,
                                'appeal_ketepatan_laporan_spj'           : task_obj.ketepatan_laporan_spj.id or None,
                                'appeal_ketepatan_laporan_ukp4'          : task_obj.ketepatan_laporan_ukp4.id or None,
                                'appeal_efisiensi_biaya_operasional'     : task_obj.efisiensi_biaya_operasional.id or None,
                                
                                'appeal_hadir_upacara_hari_besar': task_obj.hadir_upacara_hari_besar,
                                'appeal_hadir_hari_kerja'     : task_obj.hadir_hari_kerja,
                                'appeal_hadir_jam_kerja': task_obj.hadir_jam_kerja,
                                'appeal_hadir_apel_pagi': task_obj.hadir_apel_pagi,
                                
                                'appeal_integritas_presiden': task_obj.integritas_presiden,
                                'appeal_integritas_gubernur': task_obj.integritas_gubernur,
                                'appeal_integritas_kepalaopd': task_obj.integritas_kepalaopd,
                                'appeal_integritas_atasan': task_obj.integritas_atasan,
                                'appeal_integritas_es1': task_obj.integritas_es1,
                                'appeal_integritas_es2': task_obj.integritas_es2,
                                'appeal_integritas_es3': task_obj.integritas_es3,
                                'appeal_integritas_es4': task_obj.integritas_es4,
                                
                                'appeal_integritas_hukuman': task_obj.integritas_hukuman,
                                'appeal_integritas_hukuman_ringan': task_obj.integritas_hukuman_ringan,
                                'appeal_integritas_hukuman_sedang': task_obj.integritas_hukuman_sedang,
                                'appeal_integritas_hukuman_berat': task_obj.integritas_hukuman_berat,
                                
                                'appeal_kerjasama_nasional': task_obj.kerjasama_nasional,
                                'appeal_kerjasama_gubernur': task_obj.kerjasama_gubernur,
                                'appeal_kerjasama_kepalaopd': task_obj.kerjasama_kepalaopd,
                                'appeal_kerjasama_atasan':task_obj.kerjasama_atasan,
                                'appeal_kerjasama_rapat_nasional': task_obj.kerjasama_rapat_nasional,
                                'appeal_kerjasama_rapat_provinsi': task_obj.kerjasama_rapat_provinsi,
                                'appeal_kerjasama_rapat_perangkat_daerah': task_obj.kerjasama_rapat_perangkat_daerah,
                                'appeal_kerjasama_rapat_atasan': task_obj.kerjasama_rapat_atasan,
                                
                                'appeal_kepemimpinan_nasional': task_obj.kepemimpinan_nasional,
                                'appeal_kepemimpinan_gubernur': task_obj.kepemimpinan_gubernur,
                                'appeal_kepemimpinan_kepalaopd': task_obj.kepemimpinan_kepalaopd,
                                'appeal_kepemimpinan_atasan':  task_obj.kepemimpinan_atasan,
                                'appeal_kepemimpinan_narsum_nasional': task_obj.kepemimpinan_narsum_nasional,
                                'appeal_kepemimpinan_narsum_provinsi': task_obj.kepemimpinan_narsum_provinsi,
                                'appeal_kepemimpinan_narsum_perangkat_daerah': task_obj.kepemimpinan_narsum_perangkat_daerah,
                                'appeal_kepemimpinan_narsum_unitkerja': task_obj.kepemimpinan_narsum_unitkerja,
                                
                                'is_appeal' : True,
                                'notes_atasan_banding' : task_obj.notes,
                                #'work_state':'evaluated',
                                })               
                # end if           
        
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        task_pool.fill_task_automatically_with_appeal(cr, uid, [task_obj.task_id.id], context);
        task_pool.write(cr, uid, [task_obj.task_id.id],  {'work_state': 'evaluated'}, context)
project_task_perilaku_appeal_rejected()

class project_task_tambahan_propose_rejected(osv.Model):
    _name = 'project.task.tambahan.propose.rejected'
    _description = 'Tugas Tambahan Ditolak Atasan'
    _columns = {
        'is_suggest': fields.boolean('Tambahkan Koreski Penilaian'),
        'notes'      : fields.text('Catatan Koreksi',required=True),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
        'target_type_id': fields.selection([ ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),
                                            ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang Sotk Opd/Biro'),
                                                      ('lain_lain', 'Lain-Lain'),
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')], 'Jenis Kegiatan', readonly=True
                                                     ),
      
       'tugas_tambahan'     : fields.integer('Jumlah Tugas Tambahan'),
        'uraian_tugas_tambahan'     : fields.text('Uraian Tugas Tambahan'),
        'rl_presiden_tugas_tambahan'     : fields.boolean('Presiden'),
        'rl_gubernur_tugas_tambahan'     : fields.boolean('Gubernur'),
        'rl_opd_tugas_tambahan'     : fields.boolean('Kepala OPD'),
        'attach_tugas_tambahan'              : fields.binary('SK/SP/ST'),
        'nilai_kreatifitas'     : fields.integer('Jumlah Kreatifitas'),
        'uraian_kreatifitas'     : fields.text('Uraian Kreatifitas'),
        'attach_kreatifitas'              : fields.binary('Bukti Pengakuan'),
        'tupoksi_kreatifitas': fields.boolean('Tupoksi'),
        'rl_presiden_kreatifitas'     : fields.boolean('Presiden'),
        'rl_gubernur_kreatifitas'     : fields.boolean('Gubernur'),
        'rl_opd_kreatifitas'     : fields.boolean('Kepala OPD'),
       
    }
    def action_tambahan_propose_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        vals.update({             
                                 'suggest_tugas_tambahan'              : task_obj.tugas_tambahan,
                                 'suggest_uraian_tugas_tambahan'       : task_obj.uraian_tugas_tambahan,
                                'suggest_rl_opd_tugas_tambahan'       : task_obj.rl_opd_tugas_tambahan,
                                'suggest_rl_gubernur_tugas_tambahan'  : task_obj.rl_gubernur_tugas_tambahan,
                                'suggest_rl_presiden_tugas_tambahan'  : task_obj.rl_presiden_tugas_tambahan,
                                'suggest_nilai_kreatifitas'           : task_obj.nilai_kreatifitas,
                                'suggest_uraian_kreatifitas'          : task_obj.uraian_kreatifitas,
                                'suggest_tupoksi_kreatifitas'         : task_obj.tupoksi_kreatifitas,
                                'suggest_rl_opd_kreatifitas'          : task_obj.rl_opd_kreatifitas,
                                'suggest_rl_gubernur_kreatifitas'     : task_obj.rl_gubernur_kreatifitas,
                                'suggest_rl_presiden_kreatifitas'     : task_obj.rl_presiden_kreatifitas,
                                
                                'is_suggest' : True,
                                'notes_atasan' : task_obj.notes,
                                'work_state':'rejected_manager',
                                })               
                # end if           
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        
    
project_task_tambahan_propose_rejected()

class project_task_tambahan_appeal_rejected(osv.Model):
    _name = 'project.task.tambahan.appeal.rejected'
    _description = 'Tugas Tambahan Ditolak Banding'
    _columns = {
        'is_appeal': fields.boolean('Tambahkan Koreski Penilaian'),
        'notes'      : fields.text('Catatan Koreksi',required=True),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
        'target_type_id': fields.selection([ ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),
                                            ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang Sotk Opd/Biro'),
                                                      ('lain_lain', 'Lain-Lain'),
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')], 'Jenis Kegiatan', readonly=True
                                                     ),
      
       'tugas_tambahan'     : fields.integer('Jumlah Tugas Tambahan'),
        'uraian_tugas_tambahan'     : fields.text('Uraian Tugas Tambahan'),
        'rl_presiden_tugas_tambahan'     : fields.boolean('Presiden'),
        'rl_gubernur_tugas_tambahan'     : fields.boolean('Gubernur'),
        'rl_opd_tugas_tambahan'     : fields.boolean('Kepala OPD'),
        'attach_tugas_tambahan'              : fields.binary('SK/SP/ST'),
        'nilai_kreatifitas'     : fields.integer('Jumlah Kreatifitas'),
        'uraian_kreatifitas'     : fields.text('Uraian Kreatifitas'),
        'attach_kreatifitas'              : fields.binary('Bukti Pengakuan'),
        'tupoksi_kreatifitas': fields.boolean('Tupoksi'),
        'rl_presiden_kreatifitas'     : fields.boolean('Presiden'),
        'rl_gubernur_kreatifitas'     : fields.boolean('Gubernur'),
        'rl_opd_kreatifitas'     : fields.boolean('Kepala OPD'),
       
    }
    def action_tambahan_appeal_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        vals.update({             
                                 'appeal_tugas_tambahan'              : task_obj.tugas_tambahan,
                                 'appeal_uraian_tugas_tambahan'       : task_obj.uraian_tugas_tambahan,
                                'appeal_rl_opd_tugas_tambahan'       : task_obj.rl_opd_tugas_tambahan,
                                'appeal_rl_gubernur_tugas_tambahan'  : task_obj.rl_gubernur_tugas_tambahan,
                                'appeal_rl_presiden_tugas_tambahan'  : task_obj.rl_presiden_tugas_tambahan,
                                'appeal_nilai_kreatifitas'           : task_obj.nilai_kreatifitas,
                                'appeal_uraian_kreatifitas'          : task_obj.uraian_kreatifitas,
                                'appeal_tupoksi_kreatifitas'         : task_obj.tupoksi_kreatifitas,
                                'appeal_rl_opd_kreatifitas'          : task_obj.rl_opd_kreatifitas,
                                'appeal_rl_gubernur_kreatifitas'     : task_obj.rl_gubernur_kreatifitas,
                                'appeal_rl_presiden_kreatifitas'     : task_obj.rl_presiden_kreatifitas,
                                
                                'is_appeal' : True,
                                'notes_atasan_banding' : task_obj.notes,
                                #'work_state':'evaluated',
                                })               
                # end if           
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        task_pool.fill_task_automatically_with_appeal(cr, uid, [task_obj.task_id.id], context);
        task_pool.write(cr, uid, [task_obj.task_id.id],  {'work_state': 'evaluated'}, context)
project_task_tambahan_appeal_rejected()


class project_task_verificate_rejected(osv.Model):
    _name = 'project.task.verificate.rejected'
    _description = 'SKP-Non SKP, Ditolak Verifikasi'
    _columns = {
        'is_control': fields.boolean('Tambahkan Koreski Verifikasi'),
        'notes'      : fields.text('Kesimpulan Catatan Koreksi',required=True),
        'control_count': fields.integer('Jumlah Koreksi Verifikasi', readonly=True),
        'task_id'     : fields.many2one('project.task', 'Realisasi', readonly=True),
       
    }
    def action_verificate_rejected(self, cr, uid, ids, context=None):
        """  Pengajuan Di tolak
        """
        vals = {}
        task_pool = self.pool.get('project.task')
        task_obj = self.browse(cr, uid, ids[0], context=context)
        vals.update({               'control_count'     : task_obj.control_count+1,
                                    'is_control' : True,
                                    'is_suggest' : True,
                                    'notes_from_bkd' : task_obj.notes,
                                    'work_state':'rejected_bkd',
                                     })
        task_pool.write(cr, uid, [task_obj.task_id.id], vals, context)
        
    
project_task_verificate_rejected()