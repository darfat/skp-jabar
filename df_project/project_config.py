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
# ====================== config ================================= #

class satuan_hitung(osv.osv):
    _name = "satuan.hitung"
    _description    ="Satuan Hitung SKP"
   
    _columns = {
        'name'     : fields.char('Satuan',size=22,required=True),  
        'type'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('unit', 'Unit/Dinas'),
                                       ('waktu', 'Waktu')],'Tipe',required=True),
        'active'     : fields.boolean('Aktif'),
    }
   # _sql_constraints = [
   #      ('name_uniq', 'unique (name,type)',
   #          'Data Tidak Bisa Dimasukan, Satuan Hitung Dengan Nama Ini Sudah Tersedia')
   #  ]
satuan_hitung()
class project_type(osv.osv):
    _name = "project.type"
    _description    ="Jenis Kegiatan SKP"
   
    _columns = {
        'name'     : fields.char('Nama',size=79,required=True),  
        'code'     : fields.char('Kode',size=12),  
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name,code)',
             'Data Tidak Bisa Dimasukan, Satuan Hitung Dengan Nama Ini Sudah Tersedia')
     ]
project_type()

class config_skp(osv.osv):
    _name = "config.skp"
    _description    ="Konfigurasi SKP"
   
    _columns = {
        'name'     : fields.text('Nama',required=True),
        'code'     : fields.char('Kode',size=8,required=True),    
        'type'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('nilai', 'Penilaian'),
                                       ],'Tipe',required=True),
        'config_value_int'             : fields.integer('Nilai Integer'),
        'config_value_float'           : fields.float('Nilai Float'),
        'config_value_string'          : fields.char('Nilai String',size=256),
        'active'     : fields.boolean('Aktif'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name,code,type)',
             'Data Tidak Bisa Dimasukan, Satuan Hitung Dengan Nama Ini Sudah Tersedia')
     ]
config_skp()
class config_poin_index(osv.osv):
    _name = "config.poin.index"
    _description    ="Konversi Nilai"
   
    _columns = {
       
        'name'     : fields.char('Nama',size=25,required=True),    
        'type'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('nilai', 'Penilaian'),
                                       ],'Tipe',required=True),
        'value_from'             : fields.integer('Batas Nilai Bawah',required=True),
        'value_to'             : fields.float('Batas Nilai Atas',required=True),
        'value_result'          : fields.char('Hasil',size=256),
        'image_path'          : fields.char('Gambar',size=256),
        'Description'     : fields.text('Deskripsi'),
        'active'     : fields.boolean('Aktif'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (name,type)',
             'Data Tidak Bisa Dimasukan, Satuan Hitung Dengan Nama Ini Sudah Tersedia')
     ]
config_poin_index()
class kegiatan_pemprov(osv.osv):
    _name = "kegiatan.pemprov"
    _description    ="Kegiatan.Pemprov"
   
    _columns = {
        'code'     : fields.char('Kode Kegiatan',size=30,required=False),
        'name'     : fields.char('Nama Kegiatan',size=400,required=True),    
        'target_category': fields.selection([('bulanan', 'Bulanan'), ('tahunan', 'Tahunan')], 'Kategori',required=True,),
        'target_type_id': fields.selection([          ('dpa_opd_biro', 'Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro'),        
                                                      ('dipa_apbn', 'Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN'),  
                                                      ('sotk', 'Uraian Tugas Sesuai Peraturan Gubernur Tentang SOTK OPD/Biro'), 
                                                      ('lain_lain', 'Lain-Lain'), 
                                                      ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                                      ('perilaku', 'Perilaku Kerja')
                                                      ],
                                                      'Jenis Kegiatan', 
                                                     ),
        'control_biaya'             : fields.float('Verifikasi Biaya'),
        #'control_absen'             : fields.integer('Verfikasi Absen'),
        'period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')],'Periode Bulan' ,required=True, 
                                                     ),
        'period_year'     : fields.char('Periode Tahun',size=4, required=True, ),
        'description'     : fields.text('Deskripsi'),
        'active'     : fields.boolean('Aktif'),
    }
kegiatan_pemprov()
class res_company(osv.osv):
    _inherit = 'res.company'
    _columns = {
        'user_id_bkd': fields.many2one('res.users', 'Pejabat Pengevaluasi (BKD)', 
            help='Staff dari BKD yang akan memverifikasi SKP',
        ),
        'head_of_comp_employee_id': fields.many2one('res.partner', 'Kepala OPD/Dinas', 
            help='Kepala OPD',
        ),
    }
res_company()

class verifikasi_absen_pegawai(osv.osv):
    _name = "verifikasi.absen.pegawai"
    _description    ="Lookup Absensi Pegawai"
   
    _columns = {
        'employee_id': fields.many2one('res.partner', 'Pegawai'),
        'nip': fields.related('employee_id', 'nip', type='char', string="NIP",size=20, readonly=True),
        'target_period_year'     : fields.char('Periode Tahun',size=4, required=True),
        'target_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')],'Periode Bulan'
                                                     , required=True),
        'jumlah_apel_pagi'     : fields.integer('Jumlah Apel Pagi'),
        'jumlah_upacara_hari_besar': fields.integer( 'Jumlah Upacara Hari Besar'), 
        'jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja (Hari)' ),   
        'jumlah_jam_kerja': fields.integer( 'Jumlah Jam Kerja (Jam)'),
        'notes'     : fields.text('Catatan'),
                
    }
    _sql_constraints = [
         ('name_uniq', 'unique (employee_id,target_period_year,target_period_month)',
             'Data verifikasi pegawai untuk  bulan dan tahun yang sama tidak boleh duplikat')
     ]
verifikasi_absen_pegawai()

class hari_kerja_bulanan(osv.osv):
    _name = "hari.kerja.bulanan"
    _description    ="Lookup Komitmen"
   
    _columns = {
        'target_period_year'     : fields.char('Periode Tahun',size=4, required=True),
        'target_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')],'Periode Bulan'
                                                     , required=True),
        'jumlah_apel_pagi'     : fields.integer('Jumlah Apel Pagi'),
        'jumlah_upacara_hari_besar': fields.integer( 'Jumlah Upacara Hari Besar'), 
        'jumlah_hari_kerja'     : fields.integer('Jumlah Hari Kerja (Hari)' ),   
        'jumlah_jam_kerja': fields.integer( 'Jumlah Jam Kerja (Jam)'),  
        'notes'     : fields.text('Catatan'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (target_period_year,target_period_month)',
             'Data periode bulan dan tahun tidak boleh duplikat')
     ]
hari_kerja_bulanan()


class acuan_penilaian(osv.osv):
    _name = "acuan.penailaian"
    _description    ="Acuan"
   
    _columns = {
        'name'     : fields.char('Satuan',size=62,required=True),
        'code'     : fields.char('kode',size=32,required=True),    
        'kategori_nilai'     : fields.selection([('fix', 'Fix'),('threshold', 'Threshold')],"Kategori Penilaian"),
        'type'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('orientasi', 'Penilaian Perilaku Dari Sisi Orientasi'),
                                       ('integritas', 'Penilaian Perilaku Dari Sisi Integritas'),
                                       ('kerjasama', 'Penilaian Perilaku Dari Sisi Kerjasama'),
                                       ('kepemimpinan', 'Penilaian Perilaku Dari Sisi Kepemimpinan'),
                                       ('tugas_tambahan', 'Penilaian Perilaku Dari Sisi Tugas Tambahan'),
                                       ('kreatifitas', 'Penilaian Perilaku Dari Sisi Kreatifitas'),
                                       ],'Tipe',required=True),
        'kategori_integritas'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('presiden', 'Presiden'),
                                       ('gubernur', 'Gubernur'),
                                       ('kepalaopd', 'Kepala Daerah'),
                                       ('atasan', 'Atasan Langsung'),
                                       ('pejabat_es1', 'Pejabat Eselon I'),
                                       ('pejabat_es2', 'Pejabat Eselon II'),
                                       ('pejabat_es3', 'Pejabat Eselon III'),
                                       ('pejabat_es4', 'Pejabat Eselon IV'),
                                        ('tidak_hukuman', 'Tidak Ada Hukuman'),
                                       ('hukuman_berat', 'Hukuman Berat'),
                                       ('hukuman_sedang', 'Hukuman Sedang'),
                                       ('hukuman_ringan', 'Hukuman Ringan'),
                                       ],'Kategori Penilaian Integritas'),
        'kategori_kerjasama'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('nasional', 'Panitia/tim/pokja Nasional'),
                                       ('provinsi', 'Panitia/tim/pokja Provinsi'),
                                       ('perangkat_daerah', 'Panitia/tim/pokja Perangkat Daerah'),
                                       ('atasan', 'Panitia/tim/pokja Unit Kerja Atasan Langsung'),
                                       ('rapat_atasan', 'Rapat kerja/brefing Unit Kerja Atasan langsung'),
                                       ('rapat_perangkat_daerah', 'Rapat kerja/brefing Perangkat Daerah'),
                                       ('rapat_provinsi', 'Rapat kerja/brefing Provinsi'),
                                       ('rapat_nasional', 'Rapat kerja/brefing Nasional'),
                                       ],'Kategori Penilaian Kerjasama'),
        'kategori_kepemimpinan'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('nasional', 'Panitia/tim/pokja Nasional'),
                                       ('provinsi', 'Panitia/tim/pokja Provinsi'),
                                       ('perangkat_daerah', 'Panitia/tim/pokja Perangkat Daerah'),
                                       ('unitkerja', 'Panitia/tim/pokja Unit Kerja'),
                                       ('narsum_unitkerja', 'Narasumber Kerja Atasan langsung'),
                                       ('narsum_perangkat_daerah', 'Narasumber Perangkat Daerah'),
                                       ('narsum_provinsi', 'Narasumber Provinsi'),
                                       ('narsum_nasional', 'Narasumber Nasional'),
                                       ],'Kategori Penilaian Kepemimpinan'),
        'kategori_kreatifitas'     : fields.selection([('lain_lain', 'Lain-Lain'),
                                       ('presiden', 'Presiden'),
                                       ('gubernur', 'Gubernur'),
                                       ('kepalaopd', 'Kepala Daerah')],'Kategori Penilaian Kreatifitas'),
        'kategori_orientasi'     : fields.selection([('ketepatan_laporan_spj', 'Ketepatan Laporan SPJ'),
                                       ('ketepatan_laporan_ukp4', 'Ketepatan Laporan UKP4'),
                                       ('efisiensi_biaya_operasional', 'Efisiensi Biaya Operasional'),
                                       ],'Kategori Penilaian Orientasi'),
        'nilai_tunggal'     : fields.integer('Nilai Tunggal'),
        'nilai_tambahan'     : fields.integer('Nilai Tambahan'),
        'nilai_atas'     : fields.integer('Nilai Batas Atas'),
        'nilai_bawah'     : fields.integer('Nilai Batas Bawah'),
        'active'     : fields.boolean('Aktif'),
    }
    _sql_constraints = [
         ('name_uniq', 'unique (code,type)',
             'Data Tidak Bisa Dimasukan, Satuan Hitung Dengan Nama Ini Sudah Tersedia')
     ]
acuan_penilaian()

