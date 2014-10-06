import time
import xlwt
import cStringIO
from xlwt import Workbook, Formula
from report_engine_xls import report_xls
import skp_recap_yearly_report_xls_generator
import skp_recap_yearly_report_parser
from skp_recap_yearly_report_parser import skp_recap_yearly_report_parser



class skp_recap_yearly_report_xls_generator(report_xls):
	
    def generate_xls_report(self, parser, filters, obj, workbook):
	ws_summary = workbook.add_sheet(('Laporan Tahunan'))
	worksheet = workbook.add_sheet(('Laporan SKP Tahunan'))
	
	
        worksheet.panes_frozen = True
        worksheet.remove_splits = True
        worksheet.portrait = False # Landscape
        worksheet.fit_wiresult_datah_to_pages = 1
        worksheet.col(1).wiresult_datah = len("ABCDEFG")*1024
        ws_summary.panes_frozen = True
        ws_summary.remove_splits = True
        ws_summary.portrait = False # Landscape
        ws_summary.fit_wiresult_datah_to_pages = 1
        ws_summary.col(1).wiresult_datah = len("ABCDEFG")*1024
        
        int_number_style=  xlwt.easyxf("borders: top thin, bottom thin, left thin, right thin;",num_format_str='#,##0;(#,##0)')
        row_normal_style_align_right=  xlwt.easyxf("borders: top thin, bottom thin, left thin, right thin;align: wrap 1, vert centre,horiz right;",num_format_str='#,##0.00;(#,##0.00)')
        big_point_with_border_style = xlwt.easyxf('font: height 250, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_color dark_teal;borders: top thin, bottom thin, left thin, right thin;', num_format_str='#,##0.00;(#,##0.00)')
		# Specifying columns, the order doesn't matter
		# lamda d,f,p: is a function who has filter,data,parser as the parameters it is expected to the value of the column
        cols_specs = [
	    # ('header', column_span, column_type, lamda function)
	    
	    # Infos
	    
	    ('Title_1', 5, 200, 'text', lambda x, d, p: 'PENILAIAN SASARAN KERJA'),
	    ('Title_2',  5, 200, 'text', lambda x, d, p: 'PEGAWAI NEGERI SIPIL'),
	    
	    ('fix_period', 3, 200, 'text', lambda x, d, p:  'Jangka Waktu Penilaian 1 Januari sd 31 Desember '+filters['form']['period_year']),
	    #Atribut Kepegawaian
	    ('no_', 1, 30, 'text', lambda x, d, p:  'NO'),
	    ('no_1', 1, 10, 'number', lambda x, d, p: 1,xlwt.Row.set_cell_number,int_number_style),
	    ('no_2', 1, 10, 'number', lambda x, d, p: 2,xlwt.Row.set_cell_number,int_number_style),
	    ('no_3', 1, 10, 'number', lambda x, d, p: 3,xlwt.Row.set_cell_number,int_number_style),
	    ('no_4', 1, 10, 'number', lambda x, d, p: 4,xlwt.Row.set_cell_number,int_number_style),
	    ('no_5', 1, 10, 'number', lambda x, d, p: 5,xlwt.Row.set_cell_number,int_number_style),
	    ('no_6', 1, 10, 'number', lambda x, d, p: 6,xlwt.Row.set_cell_number,int_number_style),
	    ('PEJABAT PENILAI', 2, 400, 'text', lambda x, d, p:  'I. PEJABAT PENILAI'),
	    ('PEGAWAI NEGERI SIPIL YANG DINILAI', 2, 400, 'text', lambda x, d, p:  'II. PEGAWAI NEGERI SIPIL YANG DINILAI'),
	    ('nama', 1, 80, 'text', lambda x, d, p:  'Nama'),
	    ('nip', 1, 80, 'text', lambda x, d, p:  'NIP'),
	    ('pangkat_gol', 1, 80, 'text', lambda x, d, p:  'Pangkat/Gol.Ruang'),
	    ('jabatan', 1, 80, 'text', lambda x, d, p:  'Jabatan'),
	    ('unit_kerja', 1, 80, 'text', lambda x, d, p:  'Unit Kerja'),
	    
	    
	    ('nama_atasan', 1, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.name or '' ),
	    ('nama_pegawai', 1, 200, 'text', lambda x, d, p:  d and d.name or '' ),
	    ('nip_atasan', 1, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.nip or '' ),
	    ('nip_pegawai', 1, 200, 'text', lambda x, d, p:  d and d.nip or '' ),
	    ('golongan_atasan', 1, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.golongan_id and d.user_id_atasan.golongan_id.name or '' ),
	    ('golongan_pegawai', 1, 200, 'text', lambda x, d, p:  d and d.golongan_id and d.golongan_id.name or '' ),
	    ('jabatan_atasan', 1, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.job_id and d.user_id_atasan.job_id.name or '' ),
	    ('jabatan_pegawai', 1, 200, 'text', lambda x, d, p:  d and d.job_id and d.job_id.name or '' ),
	    ('unit_kerja_atasan', 1, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.department_id and d.user_id_atasan.department_id.name or '' ),
	    ('unit_kerja_pegawai', 1, 200, 'text', lambda x, d, p:  d and d.department_id and d.department_id.name or '' ),
	    ('company_pegawai', 1, 200, 'text', lambda x, d, p:  d and d.company_id and d.company_id.name or '' ),
	    ('nama_banding', 1, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.name or '' ),
	    ('nip_banding', 1, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.nip or '' ),
	    ('golongan_banding', 1, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.golongan_id and d.user_id_banding.golongan_id.name or '' ),
	    ('jabatan_banding', 1, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.job_id and d.user_id_banding.job_id.name or '' ),
	    ('unit_kerja_banding', 1, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.department_id and d.user_id_banding.department_id.name or '' ),
	    
	    
	    # Header Atribut Kegiatan
	    ('NO', 1, 30, 'text', lambda x, d, p:  'NO'),
	    ('III.KEGIATAN TUGAS POKOK JABATAN', 3, 400, 'text', lambda x, d, p:  'III.KEGIATAN TUGAS POKOK JABATAN'),
	    ('I.KEGIATAN TUGAS POKOK JABATAN', 3, 400, 'text', lambda x, d, p:  'III.KEGIATAN TUGAS POKOK JABATAN'),
	    ('II.TUGAS TAMBAHAN DAN KREATIFITAS / UNSUR PENUNJANG', 3, 400, 'text', lambda x, d, p:  'II.TUGAS TAMBAHAN DAN KREATIFITAS / UNSUR PENUNJANG'),
	    ('a.Tugas Tambahan', 3, 200, 'text', lambda x, d, p:  'a.Tugas Tambahan'),
	    ('b.Kreatifitas', 3, 200, 'text', lambda x, d, p:  'b.Kreatifitas'),
	    ('TARGET', 5, 100, 'text', lambda x, d, p:  'TARGET'),
	    ('REALISASI', 5, 100, 'text', lambda x, d, p:  'REALISASI'),
	    ('ANGKA KREDIT', 1, 40, 'text', lambda x, d, p:  'AK'),
	    ('KUANT / OUTPUT', 2, 100, 'text', lambda x, d, p:  'KUANT / OUTPUT'),
	    ('KUAL / MUTU', 1, 100, 'text', lambda x, d, p:  'KUAL / MUTU'),
	    ('WAKTU', 1, 100, 'text', lambda x, d, p:  'WAKTU'),
	    ('BIAYA', 1, 100, 'text', lambda x, d, p:  'BIAYA'),
	    ('PERHITUNGAN', 1, 100, 'text', lambda x, d, p:  'PERHITUNGAN'),
	    ('NILAI CAPAIAN SKP', 1, 100, 'text', lambda x, d, p:  'NILAI CAPAIAN SKP'),
	    ('TOTAL NILAI CAPAIAN SKP', 17, 200, 'text', lambda x, d, p:  'TOTAL NILAI CAPAIAN SKP'),
	    ('1', 1, 15, 'text', lambda x, d, p:  'NO'),
	    ('2', 3, 70, 'text', lambda x, d, p:  'III.KEGIATAN TUGAS POKOK JABATAN'),
	    ('3', 1, 25, 'text', lambda x, d, p:  'ANGKA KREDIT'),
	    ('4', 2, 20, 'text', lambda x, d, p:  'KUANT / OUTPUT'),
	    ('5', 1, 25, 'text', lambda x, d, p:  'KUAL / MUTU'),
	    ('6', 1, 25, 'text', lambda x, d, p:  'WAKTU'),
	    ('7', 1, 70, 'text', lambda x, d, p:  'BIAYA'),
	    ('8', 1, 25, 'text', lambda x, d, p:  'ANGKA KREDIT'),
	    ('9', 2, 30, 'text', lambda x, d, p:  'KUANT / OUTPUT'),
	    ('10', 1, 25, 'text', lambda x, d, p:  'KUAL / MUTU'),
	    ('11', 1, 25, 'text', lambda x, d, p:  'WAKTU'),
	    ('12', 1, 50, 'text', lambda x, d, p:  'BIAYA'),
	    ('13', 1, 25, 'text', lambda x, d, p:  'PERHITUNGAN'),
	    ('14', 1, 25, 'text', lambda x, d, p:  'NILAI CAPAIAN SKP'),
	    #Data Atribut Kegiatan
	    ('seq', 1, 20, 'number', lambda x, d, p: d.sequence,xlwt.Row.set_cell_number,int_number_style),
	    ('nama_kegiatan', 3, 200, 'text', lambda x, d, p:  d.name),
	    ('target_ak', 1, 100, 'number', lambda x, d, p:  d.total_target_angka_kredit),
	    ('target_kuantitas', 1, 100, 'number', lambda x, d, p: d.total_target_jumlah_kuantitas_output),
	    ('target_satuan_kuantitas', 1, 100, 'text', lambda x, d, p:  d.target_satuan_kuantitas_output and d.target_satuan_kuantitas_output.name or ''),
	    ('target_kualitas', 1, 100, 'number', lambda x, d, p:  d.total_target_kualitas),
	    ('target_waktu', 1, 100, 'number', lambda x, d, p:  d.total_target_waktu),
	    ('target_biaya', 1, 200, 'number', lambda x, d, p:  d.total_target_biaya),
	    ('realisasi_ak', 1, 100, 'number', lambda x, d, p:  d.total_realisasi_angka_kredit),
	    ('realisasi_kuantitas', 1, 100, 'number', lambda x, d, p:  d.total_realisasi_jumlah_kuantitas_output),
	    ('realisasi_satuan_kuantitas', 1, 100, 'text', lambda x, d, p:  d.target_satuan_kuantitas_output and d.target_satuan_kuantitas_output.name or ''),
	    ('realisasi_kualitas', 1, 100, 'number', lambda x, d, p:  d.total_realisasi_kualitas),
	    ('realisasi_waktu', 1, 100, 'number', lambda x, d, p:  d.total_realisasi_waktu),
	    ('realisasi_biaya', 1, 200, 'number', lambda x, d, p:  d.total_realisasi_biaya),
	    ('total_nilai_target_skp', 1, 200, 'number', lambda x, d, p:  d.total_nilai_target_skp),
	    ('total_capaian_target_skp', 1, 200, 'number', lambda x, d, p:  d.total_capaian_target_skp),
	    ('nilai_tugas_tambahan', 1, 200, 'number', lambda x, d, p:  d.fn_nilai_tambahan),
	    ('nilai_kreatifitas', 1, 200, 'number', lambda x, d, p:  d.fn_nilai_kreatifitas),
	    ('sum_nilai_capaian_skp', 1, 100, 'number', lambda x, d, p: d.nilai_skp_tambahan_percent),
	    
	    #Footer
	    ('footer_tanggal', 5, 100, 'text', lambda x, d, p:  p.get_concat_with_format_date('Bandung, ',filters)),
	    ('footer_pejabat_penilai', 5, 300, 'text', lambda x, d, p:  'Pejabat Penilai'),
	    ('footer_nama_atasan', 5, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.name or '' ),
	    ('footer_nip_atasan', 5, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.nip or '' ),
	    # Misc
	    ('single_empty_column', 1, 0, 'text', lambda x, d, p: ''),
	    ('double_empty_column', 2, 0, 'text', lambda x, d, p: ''),
	    ('triple_empty_column', 3, 0, 'text', lambda x, d, p: ''),
	    ('quadruple_empty_column', 4, 0, 'text', lambda x, d, p: ''),
	    ('12_empty_column', 12, 0, 'text', lambda x, d, p: ''),
	    
	    # Header Atribut Perilaku
	    # No
	    ('no_1', 1, 20, 'number', lambda x, d, p: 1,xlwt.Row.set_cell_number,int_number_style),
	    ('no_2', 1, 20, 'number', lambda x, d, p: 2,xlwt.Row.set_cell_number,int_number_style),
	    ('no_3', 1, 20, 'number', lambda x, d, p: 3,xlwt.Row.set_cell_number,int_number_style),
	    ('no_4', 1, 20, 'number', lambda x, d, p: 4,xlwt.Row.set_cell_number,int_number_style),
	    ('no_5', 1, 20, 'number', lambda x, d, p: 5,xlwt.Row.set_cell_number,int_number_style),
	    ('no_6', 1, 20, 'number', lambda x, d, p: 6,xlwt.Row.set_cell_number,int_number_style),
	    ('UNSUR PENILAIAN', 2, 200, 'text', lambda x, d, p:  'UNSUR PENILAIAN'),
	    ('NILAI', 2, 200, 'text', lambda x, d, p:  'UNSUR NILAI'),
	    ('KETERANGAN', 3, 300, 'text', lambda x, d, p:  'KETERANGAN'),
	    ('Orientasi Pelayanan', 2, 200, 'text', lambda x, d, p:  'Orientasi Pelayanan'),
	    ('Integritas', 2, 200, 'text', lambda x, d, p:  'Integritas'),
	    ('Komitmen', 2, 200, 'text', lambda x, d, p:  'Komitmen'),
	    ('Disiplin', 2, 200, 'text', lambda x, d, p:  'Disiplin'),
	    ('Kerjasama', 2, 200, 'text', lambda x, d, p:  'Kerjasama'),
	    ('Kepemimpinan',2, 200, 'text', lambda x, d, p:  'Kepemimpinan'),
	    
	    ('nilai_orientasi_pelayanan', 2, 200, 'number', lambda x, d, p:  d.nilai_pelayanan),
	    ('nilai_integritas', 2, 200, 'number', lambda x, d, p:  d.nilai_integritas),
	    ('nilai_komitmen', 2, 200, 'number', lambda x, d, p:  d.nilai_komitmen),
	    ('nilai_disiplin', 2, 200, 'number', lambda x, d, p:  d.nilai_disiplin),
	    ('nilai_kerjasama', 2, 200, 'number', lambda x, d, p:  d.nilai_kerjasama),
	    ('nilai_kepemimpinan', 2, 200, 'number', lambda x, d, p:  d.nilai_kepemimpinan),
	    ('indeks_nilai_perilaku', 3, 300, 'text', lambda x, d, p:  ''),
	    ('b. Perilaku Kerja', 1, 100, 'text', lambda x, d, p:  'b. Perilaku Kerja'),
	    
	    
	    
		]
        
        
        row_spec_value = ['seq','nama_kegiatan','target_ak','target_kuantitas','target_satuan_kuantitas','target_kualitas','target_waktu','target_biaya',
						  'realisasi_ak','realisasi_kuantitas','realisasi_satuan_kuantitas','realisasi_kualitas','realisasi_waktu','realisasi_biaya',
						  'total_nilai_target_skp','total_capaian_target_skp']
        target_spec_value = ['seq','nama_kegiatan','target_ak','target_kuantitas','target_satuan_kuantitas','target_kualitas','target_waktu','target_biaya']				
        
        # Row templates (Order Matters, this joins the columns that are specified in the second parameter)
        
        title_1_template = self.xls_row_template(cols_specs, ['triple_empty_column','Title_1','triple_empty_column','triple_empty_column','triple_empty_column','single_empty_column'])
        title_2_template = self.xls_row_template(cols_specs, ['triple_empty_column','Title_2','triple_empty_column','triple_empty_column','triple_empty_column','single_empty_column'])
        jangka_waktu_template = self.xls_row_template(cols_specs, ['single_empty_column','fix_period',])
        #KEPEGAWAIAN
        header_pegawai_template = self.xls_row_template(cols_specs, ['NO','PEJABAT PENILAI','NO','PEGAWAI NEGERI SIPIL YANG DINILAI'])
        header_nama_pegawai_template = self.xls_row_template(cols_specs, ['no_1','nama','nama_atasan','no_1','nama','nama_pegawai'])
        header_nip_pegawai_template = self.xls_row_template(cols_specs, ['no_2','nip','nip_atasan','no_2','nip','nip_pegawai'])
        header_golongan_pegawai_template = self.xls_row_template(cols_specs, ['no_3','pangkat_gol','golongan_atasan','no_3','pangkat_gol','golongan_pegawai'])
        header_jabatan_pegawai_template = self.xls_row_template(cols_specs, ['no_4','jabatan','jabatan_atasan','no_4','jabatan','jabatan_pegawai'])
        header_unit_kerja_pegawai_template = self.xls_row_template(cols_specs, ['no_5','unit_kerja','unit_kerja_atasan','no_5','unit_kerja','unit_kerja_pegawai'])
        #KTARGET REALISASI
        target_header_info_top_template = self.xls_row_template(cols_specs, ['quadruple_empty_column','TARGET',])
        target_header_info_template = self.xls_row_template(cols_specs,['NO','III.KEGIATAN TUGAS POKOK JABATAN','ANGKA KREDIT','KUANT / OUTPUT','KUAL / MUTU','WAKTU','BIAYA'])
        target_realisasi_header_info_top_template = self.xls_row_template(cols_specs, ['quadruple_empty_column','TARGET','REALISASI','double_empty_column','double_empty_column'])
        target_realisasi_header_info_template = self.xls_row_template(cols_specs,['NO','I.KEGIATAN TUGAS POKOK JABATAN','ANGKA KREDIT','KUANT / OUTPUT','KUAL / MUTU','WAKTU','BIAYA','ANGKA KREDIT','KUANT / OUTPUT','KUAL / MUTU','WAKTU','BIAYA','PERHITUNGAN','NILAI CAPAIAN SKP'])
        sub_target_realisasi_header_info_template = self.xls_row_template(cols_specs, ['1','2','3','4','5','6','7','8','9','10','11','12','13','14'])
        tambahan_kreatifitas_header_info_template = self.xls_row_template(cols_specs,['single_empty_column','II.TUGAS TAMBAHAN DAN KREATIFITAS / UNSUR PENUNJANG','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column'])
        tugas_tambahan_template = self.xls_row_template(cols_specs,['single_empty_column','a.Tugas Tambahan','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','nilai_tugas_tambahan'])
        kreatifitas_template = self.xls_row_template(cols_specs,['single_empty_column','b.Kreatifitas','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','single_empty_column','nilai_kreatifitas'])
        nilai_capaian_skp_template = self.xls_row_template(cols_specs,['TOTAL NILAI CAPAIAN SKP','sum_nilai_capaian_skp'])
        row_template = self.xls_row_template(cols_specs,row_spec_value)
        target_template = self.xls_row_template(cols_specs,target_spec_value)
        # Footer
        footer_tanggal_template = self.xls_row_template(cols_specs, ['12_empty_column','footer_tanggal',])
        footer_pejabat_penilai_template = self.xls_row_template(cols_specs, ['12_empty_column','footer_pejabat_penilai',])
        footer_nama_atasan_template = self.xls_row_template(cols_specs, ['12_empty_column','footer_nama_atasan',])
        footer_nip_atasan_template = self.xls_row_template(cols_specs, ['12_empty_column','footer_nip_atasan',])
        #sums_template = self.xls_row_template(cols_specs, ['triple_empty_column','saldo_awal_sum','penjualan_sum','penjualan_jm_sum','pelunasan_sum','pelunasan_jm_sum','saldo_akhir_sum'])
        empty_row_template = self.xls_row_template(cols_specs, ['single_empty_column'])
        
		
        # Styles (It's used for writing rows / headers)
        invisible_style=  xlwt.easyxf("align: wrap 1, vert centre;",num_format_str='#,##0.00;(#,##0.00)')
        row_normal_style=  xlwt.easyxf("borders: top thin, bottom thin, left thin, right thin;align: wrap 1, vert centre;",num_format_str='#,##0.00;(#,##0.00)')
        row_normal_without_border_style=  xlwt.easyxf("align: wrap 1, vert centre;",num_format_str='#,##0.00;(#,##0.00)')
        row_normal_without_border_center_style=  xlwt.easyxf("align: wrap 1, vert centre,horiz centre;",num_format_str='#,##0.00;(#,##0.00)')
        header_normal_style=  xlwt.easyxf('align: wrap on,  vert centre, horiz left;borders: top thin, bottom thin, left thin, right thin;',num_format_str='#,##0.00;(#,##0.00)')
        bold_normal_style=  xlwt.easyxf('font: bold on;',num_format_str='#,##0;(#,##0)')
        bold_normal_with_border_style=  xlwt.easyxf('font: bold on;borders: top thin, bottom thin, left thin, right thin;align: wrap 1, vert centre;',num_format_str='#,##0;(#,##0)')
        title_with_border_style = xlwt.easyxf('font: height 220, name Arial,  bold on, italic off; align: wrap on, vert centre,horiz centre;pattern: pattern solid, fore_color white;borders: top thin, bottom thin, left thin, right thin;', num_format_str='#,##0.00;(#,##0.00)')
        title_style = xlwt.easyxf('font: height 220, name Arial,  bold on, italic off; align: wrap on, vert centre,horiz centre;pattern: pattern solid, fore_color white;', num_format_str='#,##0.00;(#,##0.00)')
        header_with_border_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_color Teal;borders: top thin, bottom thin, left thin, right thin;', num_format_str='#,##0.00;(#,##0.00)')
        header_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap 1, vert centre, horiz center;pattern: pattern solid, fore_color Teal;', num_format_str='#,##0.00;(#,##0.00)')
        sub_header_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_color gray50;', num_format_str='#,##0.00;(#,##0.00)')
        sum_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color gray50;', num_format_str='#,##0.00;(#,##0.00)')

 
 #Get Data
        data_rekap_tahunan_pegawai = parser.get_recap_yearly_report_raw(filters);
        data_pegawai = parser.get_atribut_kepegawaian(filters);
               
 #SKP ===========================================================================================================
        row_count = 0
        self.xls_write_row(worksheet, filters, None, parser, row_count, title_1_template, title_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, None, parser, row_count, title_2_template, title_style)
        
        row_count+=1
        self.xls_write_row(worksheet, filters, data_rekap_tahunan_pegawai, parser, row_count, jangka_waktu_template, bold_normal_style)
 # Write DATA KEPEGAWAIAN
        row_count+=1
        self.xls_write_row(worksheet, filters, None, parser, row_count, header_pegawai_template, header_style)
        #row_count+=1
        #self.xls_write_row_header(worksheet, row_count, header_pegawai_template,header_style, set_column_size=False)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, header_nama_pegawai_template, header_normal_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, header_nip_pegawai_template, header_normal_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, header_golongan_pegawai_template, header_normal_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, header_jabatan_pegawai_template, header_normal_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, header_unit_kerja_pegawai_template, header_normal_style)
#HEADER TARGET REALISASI        
        row_count+=1
        self.xls_write_row(worksheet,filters,None,parser, row_count, target_realisasi_header_info_top_template, header_style,)
        row_count+=1
        self.xls_write_row_header(worksheet, row_count, target_realisasi_header_info_template, header_style, set_column_size=False)
        row_count+=1
        self.xls_write_row_header(worksheet, row_count, sub_target_realisasi_header_info_template, sub_header_style, set_column_size=True)
        
		#REALISASI
        row_count+=1
        row_data=row_count
        idx=1
        total_capaian_skp=jumlah_capaian_skp=0
        result = parser.get_skp_recap_yearly_report_raw(filters);
        for employee_data_summary_data in result:
            # Write Rows
                #employee_data_summary_data.sequence=1
                self.xls_write_row_with_indeks(worksheet, filters, employee_data_summary_data, parser, row_data, row_template, row_normal_style,idx)
                row_data+=1
                total_capaian_skp+=employee_data_summary_data.total_capaian_target_skp
                jumlah_capaian_skp+=1
                idx+=1
                
		
		#Tambahan Dan Kreatifitas
		
		row_count=row_data
        self.xls_write_row(worksheet, filters, None, parser, row_count, tambahan_kreatifitas_header_info_template, row_normal_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_rekap_tahunan_pegawai, parser, row_count, tugas_tambahan_template, row_normal_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_rekap_tahunan_pegawai, parser, row_count, kreatifitas_template, row_normal_style)
        
        # Write Totals
        #sums = {}
        #sum_jumlah =0
        #if jumlah_capaian_skp > 0 :
        #	sum_jumlah = total_capaian_skp/jumlah_capaian_skp
        #if data_tb_kreatifitas : 
        # 	sum_jumlah = sum_jumlah + data_tb_kreatifitas['sum_nilai_tambahan'] + data_tb_kreatifitas['sum_nilai_kreatifitas']
        
        #sums['sum_nilai_capaian_skp'] = sum_jumlah
        row_count+=1
        self.xls_write_row(worksheet, filters, data_rekap_tahunan_pegawai, parser, row_count, nilai_capaian_skp_template, title_with_border_style)
        
        #write footer
        row_count+=3
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, footer_tanggal_template, row_normal_without_border_center_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, footer_pejabat_penilai_template, row_normal_without_border_center_style)
        row_count+=5
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, footer_nama_atasan_template, row_normal_without_border_center_style)
        row_count+=1
        self.xls_write_row(worksheet, filters, data_pegawai, parser, row_count, footer_nip_atasan_template, row_normal_without_border_center_style)
        
        
 #end OF LAporan SKP ===========================================================================================================
 
        
       

        #SUMMARY TAHUNAN ===========================================================================================================
        summary_skp_cols_specs = [
		('Title_Formulir', 6, 600, 'text', lambda x, d, p: 'FORMULIR PENILAIAN PRESTASI KERJA'),
		('Title_PNS',  6, 600, 'text', lambda x, d, p: 'PEGAWAI NEGERI SIPIL'),
		('JANGKA WAKTU PENILAIAN', 3, 200, 'text', lambda x, d, p:  'JANGKA WAKTU PENILAIAN'),
		('fix_period', 3, 200, 'text', lambda x, d, p:  '1 Januari sd 31 Desember '+filters['form']['period_year']),
		#konten summary
	    ('1', 1, 20, 'number', lambda x, d, p: 1,xlwt.Row.set_cell_number,int_number_style),
	    ('2', 1, 20, 'number', lambda x, d, p: 2,xlwt.Row.set_cell_number,int_number_style),
	    ('3', 1, 20, 'number', lambda x, d, p: 3,xlwt.Row.set_cell_number,int_number_style),
	    ('4', 1, 20, 'number', lambda x, d, p: 4,xlwt.Row.set_cell_number,int_number_style),
	    ('YANG DINILAI', 5, 300, 'text', lambda x, d, p:  'YANG DINILAI'),
	    ('PEJABAT PENILAI', 5, 300, 'text', lambda x, d, p:  'PEJABAT PENILAI'),
	    ('ATASAN PEJABAT PENILAI', 5, 300, 'text', lambda x, d, p:  'ATASAN PEJABAT PENILAI'),
	    #konten summary
	    ('a. Nama', 1, 50, 'text', lambda x, d, p:  'a. Nama'),
	    ('b. NIP', 1, 50, 'text', lambda x, d, p:  'b. NIP'),
	    ('c. Pangkat, golongan ruang', 1, 50, 'text', lambda x, d, p:  'c. Pangkat / Golongan'),
	    ('d. Jabatan / Pekerjaan', 1, 50, 'text', lambda x, d, p:  'd. Jabatan / Pekerjaan'),
	    ('e. Unit Kerja', 1, 50, 'text', lambda x, d, p:  'e. Unit Kerja'),
	    
	    ('b. Perilaku Kerja', 1, 100, 'text', lambda x, d, p:  'b. Perilaku Kerja'),
	    ('a. Sasaran Kerja PNS (SKP)', 1, 100, 'text', lambda x, d, p:  'a. Sasaran Kerja PNS (SKP)'),
	    #Atribut Kepegawaian
	    ('company_pegawai', 2, 200, 'text', lambda x, d, p:  d and d.company_id and d.company_id.name or '' ),
	    ('nama_atasan', 4, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.name or '' ),
	    ('nama_pegawai', 4, 200, 'text', lambda x, d, p:  d and d.name or '' ),
	    ('nip_atasan', 4, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.nip or '' ),
	    ('nip_pegawai', 4, 200, 'text', lambda x, d, p:  d and d.nip or '' ),
	    ('golongan_atasan', 4, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.golongan_id and d.user_id_atasan.golongan_id.name or '' ),
	    ('golongan_pegawai', 4, 200, 'text', lambda x, d, p:  d and d.golongan_id and d.golongan_id.name or '' ),
	    ('jabatan_atasan', 4, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.job_id and d.user_id_atasan.job_id.name or '' ),
	    ('jabatan_pegawai', 4, 200, 'text', lambda x, d, p:  d and d.job_id and d.job_id.name or '' ),
	    ('unit_kerja_atasan', 4, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.department_id and d.user_id_atasan.department_id.name or '' ),
	    ('unit_kerja_pegawai', 4, 200, 'text', lambda x, d, p:  d and d.department_id and d.department_id.name or '' ),
	    ('company_pegawai', 4, 200, 'text', lambda x, d, p:  d and d.company_id and d.company_id.name or '' ),
	    ('nama_banding', 4, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.name or '' ),
	    ('nip_banding', 4, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.nip or '' ),
	    ('golongan_banding', 4, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.golongan_id and d.user_id_banding.golongan_id.name or '' ),
	    ('jabatan_banding', 4, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.job_id and d.user_id_banding.job_id.name or '' ),
	    ('unit_kerja_banding', 4, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.department_id and d.user_id_banding.department_id.name or '' ),
	    ('nilai_skp_str', 3, 200, 'text', lambda x, d, p:  p.get_concat_nilai_skp(d and d.nilai_skp,'60%',d and d.fn_nilai_tambahan, d and d.fn_nilai_kreatifitas) ,xlwt.Row.set_cell_text,row_normal_style_align_right),
	    ('nilai_skp_percent_total', 1, 200, 'number', lambda x, d, p:  d.nilai_skp_tambahan_percent,xlwt.Row.set_cell_number,big_point_with_border_style),
	    ('UNSUR YANG DINILAI', 4, 200, 'text', lambda x, d, p:  'UNSUR YANG DINILAI'),
	    ('JUMLAH', 1, 100, 'text', lambda x, d, p:  'JUMLAH'),
	     
	    #PERILAKU
	    ('1.Orientasi Pelayanan', 1, 200, 'text', lambda x, d, p:  '1.Orientasi Pelayanan'),
	    ('2.Integritas', 1, 200, 'text', lambda x, d, p:  '2.Integritas'),
	    ('3.Komitmen', 1, 200, 'text', lambda x, d, p:  '3.Komitmen'),
	    ('4.Disiplin', 1, 200, 'text', lambda x, d, p:  '4.Disiplin'),
	    ('5.Kerjasama', 1, 200, 'text', lambda x, d, p:  '5.Kerjasama'),
	    ('6.Kepemimpinan',1, 200, 'text', lambda x, d, p:  '6.Kepemimpinan'),
	    
	    ('nilai_orientasi_pelayanan', 1, 200, 'number', lambda x, d, p:  d.nilai_pelayanan),
	    ('nilai_integritas', 1, 200, 'number', lambda x, d, p:  d.nilai_integritas),
	    ('nilai_komitmen', 1, 200, 'number', lambda x, d, p:  d.nilai_komitmen),
	    ('nilai_disiplin', 1, 200, 'number', lambda x, d, p:  d.nilai_disiplin),
	    ('nilai_kerjasama', 1, 200, 'number', lambda x, d, p:  d.nilai_kerjasama),
	    ('nilai_kepemimpinan', 1, 200, 'number', lambda x, d, p:  d.nilai_kepemimpinan),
	    ('indeks_nilai_orientasi_pelayanan', 1, 200, 'text', lambda x, d, p:  d.indeks_nilai_pelayanan),
	    ('indeks_nilai_integritas', 1, 200, 'text', lambda x, d, p:  d.indeks_nilai_integritas),
	    ('indeks_nilai_komitmen', 1, 200, 'text', lambda x, d, p:  d.indeks_nilai_komitmen),
	    ('indeks_nilai_disiplin', 1, 200, 'text', lambda x, d, p:  d.indeks_nilai_disiplin),
	    ('indeks_nilai_kerjasama', 1, 200, 'text', lambda x, d, p:  d.indeks_nilai_kerjasama),
	    ('indeks_nilai_kepemimpinan', 1, 200, 'text', lambda x, d, p:  d.indeks_nilai_kepemimpinan),
	    ('total_perilaku', 1, 200, 'number', lambda x, d, p:  d.total_perilaku),
	    ('nilai_perilaku', 1, 200, 'number', lambda x, d, p:  d.nilai_perilaku),
	    ('nilai_perilaku_percent', 1, 200, 'number', lambda x, d, p:  d.nilai_perilaku_percent,xlwt.Row.set_cell_number,big_point_with_border_style),
	    
	    ('nilai_perilaku_percent_str', 2, 200, 'text', lambda x, d, p:  p.get_concat_nilai_perilaku(d and d.nilai_perilaku,'40%') ,xlwt.Row.set_cell_text,row_normal_style_align_right),
	    ('nilai_total', 1, 200, 'number', lambda x, d, p:  d.nilai_total,xlwt.Row.set_cell_number,big_point_with_border_style),
	    ('b. Perilaku Kerja', 1, 100, 'text', lambda x, d, p:  'b. Perilaku Kerja'),
	    ('Jumlah', 1, 100, 'text', lambda x, d, p:  'Jumlah'),
	    ('Rata-Rata', 1, 100, 'text', lambda x, d, p:  'Rata-Rata'),
	    ('Nilai Perilaku Kerja (%)', 1, 100, 'text', lambda x, d, p:  'Nilai Perilaku Kerja (%)'),
	    ('Nilai Prestasi Kerja', 5, 100, 'text', lambda x, d, p:  'Nilai Prestasi Kerja'),
	    
	    #Footer
	    ('5. KEBERATAN DARI PEGAWAI NEGERI SIPIL YANG DINILAI', 3, 100, 'text', lambda x, d, p:  '5. KEBERATAN DARI PEGAWAI NEGERI SIPIL YANG DINILAI'),
	    ('(APABILA ADA)', 2, 100, 'text', lambda x, d, p:  '(APABILA ADA)'),
	    ('Tanggal,..............', 2, 100, 'text', lambda x, d, p:  'Tanggal,..............'),
	    ('6.TANGGAPAN PEJABAT PENILAI ATAS KEBERATAN', 3, 100, 'text', lambda x, d, p:  '6.TANGGAPAN PEJABAT PENILAI ATAS KEBERATAN'),
	    ('7. KEPUTUSAN ATASAN PEJABAT PENILAI ATAS KEBERATAN', 3, 100, 'text', lambda x, d, p:  '7. KEPUTUSAN ATASAN PEJABAT PENILAI ATAS KEBERATAN'),
	    ('8. REKOMENDASI', 3, 100, 'text', lambda x, d, p:  '8. REKOMENDASI'),
	    ('9. DIBUAT TANGGAL,', 3, 100, 'text', lambda x, d, p:  p.get_concat_with_format_date('9.Dibuat Tanggal,',filters)),
	    ('10. DITERIMA TANGGAL,', 2, 100, 'text', lambda x, d, p:  p.get_concat_with_format_date('10.Diterima Tanggal,',filters)),
	    ('11. DITERIMA TANGGAL,', 3, 100, 'text', lambda x, d, p:   p.get_concat_with_format_date('11.Diterima Tanggal,',filters)),
	    ('9.Pejabat Penilai', 3, 300, 'text', lambda x, d, p:  'Pejabat Penilai'),
	    ('10.Pegawai Negeri Sipil Yang Dinilai',2, 300, 'text', lambda x, d, p:  '     Pegawai Negeri Sipil Yang Dinilai'),
	    ('11.Atasan Pejabat Penilai', 3, 300, 'text', lambda x, d, p:  'Atasan Pejabat Penilai'),
	    ('footer_nama_atasan', 3, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.name or '' ),
	    ('footer_nama_pegawai', 2, 200, 'text', lambda x, d, p:  d and d.name or '' ),
	    ('footer_nip_atasan', 3, 200, 'text', lambda x, d, p:  d and d.user_id_atasan and d.user_id_atasan.nip or '' ),
	    ('footer_nip_pegawai', 2, 200, 'text', lambda x, d, p:  d and d.nip or '' ),
	    ('footer_nama_banding', 3, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.name or '' ),
	    ('footer_nip_banding', 3, 200, 'text', lambda x, d, p:  d and d.user_id_banding and d.user_id_banding.nip or '' ),
	    ('single_empty_column', 1, 0, 'text', lambda x, d, p: ''),
	    ('double_empty_column', 2, 0, 'text', lambda x, d, p: ''),
	    ('triple_empty_column', 3, 0, 'text', lambda x, d, p: ''),
	    ('quadruple_empty_column', 4, 0, 'text', lambda x, d, p: ''),
	    
		]
    	settings_cols_specs = [
		#konten summary
	  
	    ('1', 1, 10, 'text', lambda x, d, p:  '1'),
	    ('2', 1, 150, 'text', lambda x, d, p:  '2'),
	    ('3', 1, 350, 'text', lambda x, d, p:  '3'),
	    ('4', 1, 200, 'text', lambda x, d, p:  '3'),
	    ('5', 1, 200, 'text', lambda x, d, p:  '3'),
	    ('6', 1, 200, 'text', lambda x, d, p:  '3'),
	    ('7', 1, 200, 'text', lambda x, d, p:  '3'),
		]
    	
    	
        
        title_2_template = self.xls_row_template(summary_skp_cols_specs, ['Title_PNS'])
        title_1_template = self.xls_row_template(summary_skp_cols_specs, ['Title_Formulir'])
        jangka_waktu_template = self.xls_row_template(summary_skp_cols_specs, ['triple_empty_column','JANGKA WAKTU PENILAIAN',])
        company_and_period_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','company_pegawai','fix_period'])
        col_settings_template = self.xls_row_template(settings_cols_specs, ['1','2','3'])
        
        header_pegawai_yg_dinilai_template = self.xls_row_template(summary_skp_cols_specs, ['1','YANG DINILAI'])
        nama_pns_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','a. Nama','nama_pegawai'])
        nip_pns_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','b. NIP','nip_pegawai'])
        pangkat_pns_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','c. Pangkat, golongan ruang','golongan_pegawai'])
        jabatan_pns_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','d. Jabatan / Pekerjaan','jabatan_pegawai'])
        unit_kerja_pns_template = self.xls_row_template(summary_skp_cols_specs,['single_empty_column','e. Unit Kerja','unit_kerja_pegawai'])
        atasan_pegawai_yg_dinilai_template = self.xls_row_template(summary_skp_cols_specs, ['2','PEJABAT PENILAI'])
        nama_atasan_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','a. Nama','nama_atasan'])
        nip_atasan_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','b. NIP','nip_atasan'])
        pangkat_atasan_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','c. Pangkat, golongan ruang','golongan_atasan'])
        jabatan_atasan_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','d. Jabatan / Pekerjaan','jabatan_atasan'])
        unit_kerja_atasan_template = self.xls_row_template(summary_skp_cols_specs,['single_empty_column','e. Unit Kerja','unit_kerja_atasan'])
        banding_pegawai_yg_dinilai_template = self.xls_row_template(summary_skp_cols_specs, ['3','ATASAN PEJABAT PENILAI'])
        nama_banding_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','a. Nama','nama_banding'])
        nip_banding_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','b. NIP','nip_banding'])
        pangkat_banding_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','c. Pangkat, golongan ruang','golongan_banding'])
        jabatan_banding_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','d. Jabatan / Pekerjaan','jabatan_banding'])
        unit_kerja_banding_template = self.xls_row_template(summary_skp_cols_specs,['single_empty_column','e. Unit Kerja','unit_kerja_banding'])
        skp_header_unsur_template = self.xls_row_template(summary_skp_cols_specs, ['4','UNSUR YANG DINILAI','JUMLAH'])
        skp_total_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','a. Sasaran Kerja PNS (SKP)','nilai_skp_str','nilai_skp_percent_total'])
        perilaku_pelayanan_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','b. Perilaku Kerja','1.Orientasi Pelayanan','nilai_orientasi_pelayanan','indeks_nilai_orientasi_pelayanan','single_empty_column'])
        perilaku_integritas_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','2.Integritas','nilai_integritas','indeks_nilai_integritas','single_empty_column'])
        perilaku_komitmen_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','3.Komitmen','nilai_komitmen','indeks_nilai_komitmen','single_empty_column'])
        perilaku_disiplin_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','4.Disiplin','nilai_disiplin','indeks_nilai_disiplin','single_empty_column'])
        perilaku_kerjasama_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','5.Kerjasama','nilai_kerjasama','indeks_nilai_kerjasama','single_empty_column'])
        perilaku_kepemimpinan_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','6.Kepemimpinan','nilai_kepemimpinan','indeks_nilai_kepemimpinan','single_empty_column'])
        jumlah_perilaku_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','Jumlah','total_perilaku','single_empty_column','single_empty_column'])
        nilai_perilaku_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','Rata-Rata','nilai_perilaku','single_empty_column','single_empty_column'])
        nilai_perilaku_percent_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','Nilai Perilaku Kerja (%)','nilai_perilaku_percent_str','nilai_perilaku_percent'])
        nilai_total_kinerja_template = self.xls_row_template(summary_skp_cols_specs, ['Nilai Prestasi Kerja','nilai_total'])
        #footer
        keberatan_template = self.xls_row_template(summary_skp_cols_specs, ['5. KEBERATAN DARI PEGAWAI NEGERI SIPIL YANG DINILAI',])
        keberatan_2_template = self.xls_row_template(summary_skp_cols_specs, ['(APABILA ADA)',])
        tanggal_template=self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','Tanggal,..............',])
        tanggal_kanan_template=self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','single_empty_column','Tanggal,..............',])
        footer_6_template = self.xls_row_template(summary_skp_cols_specs, ['6.TANGGAPAN PEJABAT PENILAI ATAS KEBERATAN',])
    	footer_7_template = self.xls_row_template(summary_skp_cols_specs, ['7. KEPUTUSAN ATASAN PEJABAT PENILAI ATAS KEBERATAN',])
    	footer_8_template = self.xls_row_template(summary_skp_cols_specs, ['8. REKOMENDASI',])
    	footer_9_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','9. DIBUAT TANGGAL,'])
        footer_10_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','10. DITERIMA TANGGAL,'])
    	footer_11_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','11. DITERIMA TANGGAL,'])
    	footer_9a_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','9.Pejabat Penilai'])
        footer_10a_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','10.Pegawai Negeri Sipil Yang Dinilai'])
        footer_11a_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','11.Atasan Pejabat Penilai'])
    	footer_9b_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','footer_nama_atasan'])
    	footer_9c_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','footer_nip_atasan'])
        footer_10b_template = self.xls_row_template(summary_skp_cols_specs, ['footer_nama_pegawai'])
    	footer_10c_template = self.xls_row_template(summary_skp_cols_specs, ['footer_nip_pegawai'])
    	footer_11b_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','footer_nama_banding'])
    	footer_11c_template = self.xls_row_template(summary_skp_cols_specs, ['single_empty_column','single_empty_column','single_empty_column','footer_nip_banding'])
    	
        row_count = 0
        self.xls_write_row(ws_summary, filters, None, parser, row_count, title_1_template, title_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, None, parser, row_count, title_2_template, title_style)     
        row_count+=1
        self.xls_write_row_header_settings(ws_summary, row_count, col_settings_template, invisible_style, set_column_size=True)
        row_count+=1
        self.xls_write_row(ws_summary, filters, None, parser, row_count, jangka_waktu_template, bold_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, company_and_period_template, bold_normal_style)
        
# Write DATA KEPEGAWAIAN
        row_count+=1
        self.xls_write_row_header(ws_summary, row_count, header_pegawai_yg_dinilai_template,header_with_border_style, set_column_size=False)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, nama_pns_template, header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,nip_pns_template , header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, pangkat_pns_template, header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,jabatan_pns_template , header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,unit_kerja_pns_template , header_normal_style)
        
        row_count+=1
        self.xls_write_row_header(ws_summary, row_count, atasan_pegawai_yg_dinilai_template,header_with_border_style, set_column_size=False)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, nama_atasan_template, header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,nip_atasan_template , header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, pangkat_atasan_template, header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,jabatan_atasan_template , header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,unit_kerja_atasan_template , header_normal_style)
        
        row_count+=1
        self.xls_write_row_header(ws_summary, row_count, banding_pegawai_yg_dinilai_template,header_with_border_style, set_column_size=False)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, nama_banding_template, header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,nip_banding_template , header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, pangkat_banding_template, header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,jabatan_banding_template , header_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count,unit_kerja_banding_template , header_normal_style)
        
        #PENILAIAN
        row_count+=1
        self.xls_write_row_header(ws_summary, row_count, skp_header_unsur_template,header_with_border_style, set_column_size=False)
        #SKP
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, skp_total_template, row_normal_style)
        #PERILAKU
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, perilaku_pelayanan_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, perilaku_integritas_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, perilaku_komitmen_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, perilaku_disiplin_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, perilaku_kerjasama_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, perilaku_kepemimpinan_template, row_normal_style)
        
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, jumlah_perilaku_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, nilai_perilaku_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, nilai_perilaku_percent_template, row_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, nilai_total_kinerja_template, title_with_border_style)
        
        #footer
        
        row_count+=6
        self.xls_write_row(ws_summary, filters, None, parser, row_count, keberatan_template, bold_normal_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, None, parser, row_count, keberatan_2_template, bold_normal_style)
        row_count+=6
        self.xls_write_row(ws_summary, filters, None, parser, row_count, tanggal_template, row_normal_without_border_style)
        row_count+=2
        self.xls_write_row(ws_summary, filters, None, parser, row_count, footer_6_template, bold_normal_style)
        row_count+=6
        self.xls_write_row(ws_summary, filters, None, parser, row_count, tanggal_kanan_template, row_normal_without_border_style)
        row_count+=2
        self.xls_write_row(ws_summary, filters, None, parser, row_count, footer_7_template, bold_normal_style)
        row_count+=5
        self.xls_write_row(ws_summary, filters, None, parser, row_count, tanggal_kanan_template, row_normal_without_border_style)
        row_count+=2
        self.xls_write_row(ws_summary, filters, None, parser, row_count, footer_8_template, bold_normal_style)
        row_count+=6
        self.xls_write_row(ws_summary, filters, None, parser, row_count, tanggal_kanan_template, row_normal_without_border_style)
        
        #footer ttd
        row_count+=10
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, footer_9_template, row_normal_without_border_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, footer_9a_template, row_normal_without_border_center_style)
        row_count+=5
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, footer_9b_template, row_normal_without_border_center_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, footer_9c_template, row_normal_without_border_center_style)
        row_count+=2
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, footer_10_template, row_normal_without_border_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, footer_10a_template, row_normal_without_border_style)
        row_count+=5
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, footer_10b_template, row_normal_without_border_center_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, footer_10c_template, row_normal_without_border_center_style)
        row_count+=2
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, footer_11_template, row_normal_without_border_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_rekap_tahunan_pegawai, parser, row_count, footer_11a_template, row_normal_without_border_center_style)
        row_count+=5
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, footer_11b_template, row_normal_without_border_center_style)
        row_count+=1
        self.xls_write_row(ws_summary, filters, data_pegawai, parser, row_count, footer_11c_template, row_normal_without_border_center_style)
  
    # Override from report_engine_xls.py	
    def create_source_xls(self, cr, uid, ids, filters, report_xml, context=None): 
        if not context: context = {}
	
	# Avoiding context's values change
        context_clone = context.copy()
	
        rml_parser = self.parser(cr, uid, self.name2, context=context_clone)
        objects = self.getObjects(cr, uid, ids, context=context_clone)
        rml_parser.set_context(objects, filters, ids, 'xls')
        io = cStringIO.StringIO()
        workbook = xlwt.Workbook(encoding='utf-8')
        self.generate_xls_report(rml_parser, filters, rml_parser.localcontext['objects'], workbook)
        workbook.save(io)
        io.seek(0)
        return (io.read(), 'xls')

#Start the reporting service
skp_recap_yearly_report_xls_generator(
    #name (will be referred from skp_recap_yearly_report.py, must add "report." as prefix)
    'report.skp.recap.yearly.xls',
    #model
    'skp.recap.yearly.report',
    #file
    'addons/df_skp_recap_yearly_report/report/skp_recap_yearly_report.xls',
    #parser
    parser=skp_recap_yearly_report_parser,
    #header
    header=True
)