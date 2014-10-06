import time
import xlwt
import cStringIO
from xlwt import Workbook, Formula
from report_engine_xls import report_xls
import employee_realisasi_summary_report_xls_generator
import employee_realisasi_summary_report_parser
from employee_realisasi_summary_report_parser import employee_realisasi_summary_report_parser

class employee_realisasi_summary_report_xls_generator(report_xls):
	
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
	    
	    ('ID', 1, 50, 'text', lambda x, d, p:  d['employee_id']),
	    ('NIP', 1, 100, 'text', lambda x, d, p:  d['employee_nip']),
	    ('Nama Pegawai', 1, 250, 'text', lambda x, d, p:  d['employee_name']),
	    ('Jabatan', 1, 250, 'text', lambda x, d, p:  d['jabatan']),
	    ('Bidang', 1, 250, 'text', lambda x, d, p:  d['bidang']),
	    ('Nama OPD', 1, 250, 'text', lambda x, d, p:  d['company_name']),
	    ('User ID', 1, 100, 'text', lambda x, d, p:  d['user_id']),
	    ('Petugas Verifikasi', 1, 100, 'text', lambda x, d, p:  d['verificator_login']),
	    ('Periode', 1, 100, 'text', lambda x, d, p:  p.get_period( d['target_period_month'],d['target_period_year']) ),
	    ('Jenis Kegiatan', 1, 100, 'text', lambda x, d, p: p.get_lookup_target_type( d['target_type_id']) ) ,
	    ('Status', 1, 100, 'text', lambda x, d, p:  p.get_lookup_state( d['status'] )),
	    ('Jumlah Realisasi', 1, 50, 'number', lambda x, d, p:  d['count_of_task']),
	    
        # Misc
	    ('single_empty_column', 1, 0, 'text', lambda x, d, p: ''),
	    ('triple_empty_column', 3, 0, 'text', lambda x, d, p: ''),
	    ('quadruple_empty_column', 4, 0, 'text', lambda x, d, p: ''),
	]
    

        row_spec_value = ['ID','NIP','Nama Pegawai','Jabatan','Nama OPD','User ID','Petugas Verifikasi','Periode','Jenis Kegiatan','Status','Jumlah Realisasi']
        # Row templates (Order Matters, this joins the columns that are specified in the second parameter)
        company_template = self.xls_row_template(cols_specs, ['single_empty_column','Company'])
        title_template = self.xls_row_template(cols_specs, ['single_empty_column','Title'])
        #period_template = self.xls_row_template(cols_specs, ['single_empty_column','Period'])
        #top_header_template = self.xls_row_template(cols_specs, ['quadruple_empty_column','Penambahan','Pengurangan','single_empty_column'])
        row_template = self.xls_row_template(cols_specs,row_spec_value)
        #sums_template = self.xls_row_template(cols_specs, ['triple_empty_column','saldo_awal_sum','penjualan_sum','penjualan_jm_sum','pelunasan_sum','pelunasan_jm_sum','saldo_akhir_sum'])
        empty_row_template = self.xls_row_template(cols_specs, ['single_empty_column'])

        # Styles (It's used for writing rows / headers)
        row_normal_style=  xlwt.easyxf(num_format_str='#,##0.00;(#,##0.00)')
        row_normal_odd_style=  xlwt.easyxf('pattern: pattern solid, fore_color silver_ega;',num_format_str='#,##0.00;(#,##0.00)')
        info_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color gray50;', num_format_str='#,##0.00;(#,##0.00)')
        top_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre, horiz center;pattern: pattern solid, fore_color orange;', num_format_str='#,##0.00;(#,##0.00)')
        header_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color green;', num_format_str='#,##0.00;(#,##0.00)')
        sum_style = xlwt.easyxf('font: height 200, name Arial, colour_index white, bold on, italic off; align: wrap on, vert centre;pattern: pattern solid, fore_color gray50;', num_format_str='#,##0.00;(#,##0.00)')

        # Write infos
        # xls_write_row(worksheet, filters, data parser, row_number, template, style)
        self.xls_write_row(worksheet, filters, None, parser, 0, empty_row_template, row_normal_style)
        #self.xls_write_row(worksheet, filters, None, parser, 1, company_template, info_style)
        #self.xls_write_row(worksheet, filters, None, parser, 2, title_template, info_style)
        #self.xls_write_row(worksheet, filters, None, parser, 3, period_template, info_style)
        self.xls_write_row(worksheet, filters, None, parser, 4, empty_row_template, row_normal_style)

        # Write top header
        #self.xls_write_row(worksheet, filters, None, parser, 5, top_header_template, top_style)

            # Write headers (It uses the first parameter of cols_specs)
        self.xls_write_row_header(worksheet, 6, row_template, header_style, set_column_size=True)

        row_count = 8
        result = parser.get_employee_realisasi_summary_report_raw(filters);
        for employee_realisasi_summary_data in result:
            # Write Rows
                style = row_normal_style
                if(row_count % 2 == 0):
                    style = row_normal_odd_style;
                self.xls_write_row(worksheet, filters, employee_realisasi_summary_data, parser, row_count, row_template, style)

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
employee_realisasi_summary_report_xls_generator(
    #name (will be referred from employee_realisasi_summary_report.py, must add "report." as prefix)
    'report.employee.realisasi.summary.xls',
    #model
    'employee.realisasi.summary.report',
    #file
    'addons/df_report_employee_realisasi/report/employee_realisasi_summary_report.xls',
    #parser
    parser=employee_realisasi_summary_report_parser,
    #header
    header=True
)