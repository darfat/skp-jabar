import time
import xlwt
import cStringIO
from xlwt import Workbook, Formula
from report_engine_xls import report_xls
import skp_monthly_recapitulation_report_xls_generator
import skp_monthly_recapitulation_report_parser
from skp_monthly_recapitulation_report_parser import skp_monthly_recapitulation_report_parser

class skp_monthly_recapitulation_report_xls_generator(report_xls):
	
    def generate_xls_report(self, parser, filters, obj, workbook):
	worksheet = workbook.add_sheet(('Laporan Summary Pegawai'))
        worksheet.panes_frozen = True
        worksheet.remove_splits = True
        worksheet.portrait = True # Landscape
        worksheet.fit_wiresult_datah_to_pages = 1
        worksheet.col(1).wiresult_datah = len("ABCDEFG")*1024

	# Specifying columns, the order doesn't matter
	# lamda d,f,p: is a function who has filter,data,parser as the parameters it is expected to the value of the column
        cols_specs = [
	    # ('header', column_span, column_type, lamda function)
	    
	    # Infos
	    ('Company', 2, 200, 'text', lambda x, d, p: 'Badan Kepegawaian Daerah Jawa Barat'),
	    ('Title',  2, 0, 'text', lambda x, d, p: p.get_title('Kepegawaian',filters)),
	    
	    # Top Headers
	   # ('Penambahan', 2, 100, 'text', lambda x, d, p: 'Penambahan'),
	    

	    # Main Headers / Rows
	    
	    ('NO', 1, 30, 'number', lambda x, d, p:  d['no_idx']),
	    ('NIP', 1, 100, 'text', lambda x, d, p:  d['employee_nip']),
	    ('Nama Pegawai', 1, 250, 'text', lambda x, d, p:  d['employee_name']),
	    ('Nama OPD', 1, 250, 'text', lambda x, d, p:  d['company_name']),
	    ('Status SKP', 1, 100, 'text', lambda x, d, p:  p.get_status_skp( d['skp_obj'] ) ),
	    ('Jumlah SKP', 1, 50, 'number', lambda x, d, p:  p.get_jml_skp( d['skp_obj'] ) ),
	    ('Nilai SKP', 1, 50, 'number', lambda x, d, p:  p.get_nilai_skp_percent( d['skp_obj'] ) ),
	    ('Jumlah Perilaku', 1, 50, 'number', lambda x, d, p:  p.get_jml_perilaku( d['skp_obj'] ) ),
	    ('Nilai Perilaku', 1, 50, 'number', lambda x, d, p:  p.get_nilai_perilaku_percent( d['skp_obj'] ) ),
	    ('Nilai Tugas Tambahan', 1, 50, 'number', lambda x, d, p:  p.get_nilai_tambahan( d['skp_obj'] ) ),
	    ('Nilai Kreatifitas', 1, 50, 'number', lambda x, d, p:  p.get_nilai_kreatifitas( d['skp_obj'] ) ),
	    ('Nilai Total', 1, 50, 'number', lambda x, d, p:  p.get_nilai_total( d['skp_obj'] ) ),
	    ('Nilai Toleransi', 1, 50, 'number', lambda x, d, p:  p.get_nilai_toleransi( d['skp_obj'],d ) ),
	    ('Kategori Penilaian', 1, 50, 'text', lambda x, d, p:  p.get_kategori_penilaian( d['skp_obj'] ,d ) ),
	    ('Jml Draft', 1, 50, 'number', lambda x, d, p:  d['count_draft']),
	    ('Jml Realisasi', 1, 50, 'number', lambda x, d, p:  d['count_realisasi']),
	    ('Jml Realisasi Keseluruhan', 1, 50, 'number', lambda x, d, p:  d['count_realisasi_all'] ),
	    #('Total Target', 1, 50, 'number', lambda x, d, p:  d['count_target_all']),
	    ('Eselon', 1, 50, 'text', lambda x, d, p:  d['eselon']),
	    ('Tipe Jabatan', 1, 50, 'text', lambda x, d, p:  d['tipe_jabatan']),
	    ('Golongan', 1, 20, 'text', lambda x, d, p:  d['golongan']),
	    ('Bidang', 1, 200, 'text', lambda x, d, p:  d['bidang']),
	    ('Biro', 1, 200, 'text', lambda x, d, p:  d['biro_name']),
	    ('Jabatan', 1, 200, 'text', lambda x, d, p:  d['jabatan']),
	   
	    
	    ('Status', 1, 100, 'text', lambda x, d, p:  d['user_id']),
	    
	    
        # Misc
	    ('single_empty_column', 1, 0, 'text', lambda x, d, p: ''),
	    ('triple_empty_column', 3, 0, 'text', lambda x, d, p: ''),
	    ('quadruple_empty_column', 4, 0, 'text', lambda x, d, p: ''),
	]
    

        row_spec_value = ['NO','Nama OPD','NIP','Nama Pegawai',
						  'Status SKP','Jumlah SKP','Nilai SKP','Nilai Perilaku','Nilai Tugas Tambahan','Nilai Kreatifitas','Nilai Total','Nilai Toleransi',
						  'Kategori Penilaian','Jml Realisasi','Jml Draft','Jml Realisasi Keseluruhan',
						 'Eselon','Tipe Jabatan','Golongan','Biro','Bidang','Jabatan']
						# 'NIP Atasan','Nama Atasan','NIP Atasan Banding','Nama Atasan Banding',
						#'Nama Sekolah','Jurusan','Diklat Kepemimpinan','Diklat Fungsional','Tempat Lahir','Tanggal Lahir','Agama','Status']
        # Row templates (Order Matters, this joins the columns that are specified in the second parameter)
        company_template = self.xls_row_template(cols_specs, ['single_empty_column','Company'])
        title_template = self.xls_row_template(cols_specs, ['single_empty_column','Title'])
        #period_template = self.xls_row_template(cols_specs, ['single_empty_column','Period'])
        #top_header_template = self.xls_row_template(cols_specs, ['quadruple_empty_column','Penambahan','Pengurangan','single_empty_column'])
        row_template = self.xls_row_template(cols_specs,row_spec_value)
        #sums_template = self.xls_row_template(cols_specs, ['triple_empty_column','saldo_awal_sum','penjualan_sum','penjualan_jm_sum','pelunasan_sum','pelunasan_jm_sum','saldo_akhir_sum'])
        empty_row_template = self.xls_row_template(cols_specs, ['single_empty_column'])

        # Styles (It's used for writing rows / headers)
        row_normal_style=  xlwt.easyxf(num_format_str='#,##0;(#,##0)')
        row_normal_odd_style=  xlwt.easyxf('pattern: pattern solid, fore_color silver_ega;',num_format_str='#,##0;(#,##0)')
        info_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color gray50;', num_format_str='#,##0.00;(#,##0.00)')
        top_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_color orange;', num_format_str='#,##0.00;(#,##0.00)')
        header_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color green;', num_format_str='#,##0.00;(#,##0.00)')
        sum_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color gray50;', num_format_str='#,##0.00;(#,##0.00)')

        # Write infos
        # xls_write_row(worksheet, filters, data parser, row_number, template, style)
        #self.xls_write_row(worksheet, filters, None, parser, 0, empty_row_template, row_normal_style)
        #self.xls_write_row(worksheet, filters, None, parser, 1, company_template, info_style)
        #self.xls_write_row(worksheet, filters, None, parser, 2, title_template, info_style)
        #self.xls_write_row(worksheet, filters, None, parser, 3, period_template, info_style)
        #self.xls_write_row(worksheet, filters, None, parser, 4, empty_row_template, row_normal_style)

        # Write top header
        #self.xls_write_row(worksheet, filters, None, parser, 5, top_header_template, top_style)

            # Write headers (It uses the first parameter of cols_specs)
        self.xls_write_row_header(worksheet, 0, row_template, header_style, set_column_size=True)

        row_count = 1
        result = parser.get_skp_monthly_recapitulation_report_raw(filters);
        for employee_data_summary_data in result:
            # Write Rows
                style = row_normal_style
                if(row_count % 2 == 0):
                    style = row_normal_odd_style;
                self.xls_write_row(worksheet, filters, employee_data_summary_data, parser, row_count, row_template, style)

                row_count+=1

        # Write Totals

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
skp_monthly_recapitulation_report_xls_generator(
    #name (will be referred from skp_monthly_recapitulation_report.py, must add "report." as prefix)
    'report.skp.monthly.recapitulation.xls',
    #model
    'skp.monthly.recapitulation.report',
    #file
    'addons/df_report_skp_rekapitulasi_bulanan/report/skp_monthly_recapitulation_report.xls',
    #parser
    parser=skp_monthly_recapitulation_report_parser,
    #header
    header=True
)