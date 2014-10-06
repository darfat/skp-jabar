import time
import xlwt
import cStringIO
from xlwt import Workbook, Formula
from report_engine_xls import report_xls
import target_tahunan_report_xls_generator
import target_tahunan_report_parser
from target_tahunan_report_parser import target_tahunan_report_parser

class target_tahunan_report_xls_generator(report_xls):
	
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
	    ('Company', 9, 0, 'text', lambda x, d, p: p.get_title('',filters)),
	    ('Title',  9, 0, 'text', lambda x, d, p: 'Laporan Target Tahunan Pegawai'),
	    ('Period',  9, 0, 'text', lambda x, d, p: p.get_period(filters)),
	    
	    # Top Headers
	    # ('Penambahan', 2, 100, 'text', lambda x, d, p: 'Penambahan'),
	    

	    # Main Headers / Rows
	    
	    ('No', 1, 50, 'text', lambda x, d, p:  ''),
	    ('Nama Pegawai', 1, 250, 'text', lambda x, d, p:  d['employee_id']['name']),
	    ('NIP', 1, 100, 'text', lambda x, d, p:  d['employee_id']['nip']),
	    ('Jabatan', 1, 250, 'text', lambda x, d, p:  d['employee_id']['job_id']['name']),
	    ('Nama OPD', 1, 250, 'text', lambda x, d, p:  d['employee_id']['company_id']['name']),
	    ('Kode Kegiatan', 1, 80, 'text', lambda x, d, p:  d['code']),
	    ('Nama Kegiatan', 1, 90, 'text', lambda x, d, p:  d['name']),
	    ('Lama Kegiatan', 1, 90, 'number', lambda x, d, p:  d['lama_kegiatan']),
	    ('Jenis', 1, 90, 'text', lambda x, d, p:  p.get_lookup_target_type( d['target_type_id']) ),
	    ('Kuantitas Output', 1, 80, 'number', lambda x, d, p:  d['target_jumlah_kuantitas_output']),
	    ('Kualitas', 1, 80, 'number', lambda x, d, p:  d['target_kualitas']),
	    ('Biaya', 1, 100, 'number', lambda x, d, p:  d['target_biaya']),
	    ('Angka Kredit', 1, 80, 'number', lambda x, d, p:  d['target_angka_kredit']),
	    ('Status', 1, 80, 'text', lambda x, d, p: p.get_lookup_state( d['state'] ) ),
	    # Sums
	    ('sum_biaya', 1, 100, 'number', lambda x, d, p: d['sum_biaya']),
	    ('sum_kuantitas_output', 1, 80, 'number', lambda x, d, p: d['sum_kuantitas_output']),
	    ('sum_kualitas', 1, 80, 'number', lambda x, d, p: d['sum_kualitas']),
	    ('sum_angka_kredit', 1, 80, 'number', lambda x, d, p: d['sum_angka_kredit']),
        # Misc
	    ('single_empty_column', 1, 0, 'text', lambda x, d, p: ''),
	    ('triple_empty_column', 3, 0, 'text', lambda x, d, p: ''),
	    ('quadruple_empty_column', 4, 0, 'text', lambda x, d, p: ''),
	    ('sembilan_empty_column', 9, 0, 'text', lambda x, d, p: ''),
	]
    

        row_spec_value = ['Nama Pegawai','NIP','Jabatan','Nama OPD',
						 'Kode Kegiatan','Nama Kegiatan','Jenis','Lama Kegiatan',
						 'Kuantitas Output','Kualitas','Biaya','Angka Kredit','Status']
        # Row templates (Order Matters, this joins the columns that are specified in the second parameter)
        company_template = self.xls_row_template(cols_specs, ['single_empty_column','Company'])
        title_template = self.xls_row_template(cols_specs, ['single_empty_column','Title'])
        period_template = self.xls_row_template(cols_specs, ['single_empty_column','Period'])
        #top_header_template = self.xls_row_template(cols_specs, ['quadruple_empty_column','Penambahan','Pengurangan','single_empty_column'])
        row_template = self.xls_row_template(cols_specs,row_spec_value)
        sums_template = self.xls_row_template(cols_specs, ['sum_kuantitas_output','sum_kualitas','sum_biaya','sum_angka_kredit',])
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
        self.xls_write_row(worksheet, filters, None, parser, 1, company_template, info_style)
        self.xls_write_row(worksheet, filters, None, parser, 2, title_template, info_style)
        self.xls_write_row(worksheet, filters, None, parser, 3, period_template, info_style)
        self.xls_write_row(worksheet, filters, None, parser, 4, empty_row_template, row_normal_style)

        # Write top header
        #self.xls_write_row(worksheet, filters, None, parser, 5, top_header_template, top_style)

            # Write headers (It uses the first parameter of cols_specs)
        self.xls_write_row_header(worksheet, 6, row_template, header_style, set_column_size=True)

        row_count = 7
        sum_biaya=sum_kuantitas_output=sum_kualitas=sum_angka_kredit=0
        result = parser.get_target_tahunan_report_raw(filters);
        size_of_result  = row_count+len(result)
       
        for target_tahunan_data in result:
            # Write Rows
                style = row_normal_style
                if(row_count % 2 == 0):
                    style = row_normal_odd_style;
                self.xls_write_row(worksheet, filters, target_tahunan_data, parser, row_count, row_template, style)
                row_count+=1
                sum_biaya+=target_tahunan_data.target_biaya
                

        # Write Totals
		sums = {}
		sums['sum_biaya'] = sum_biaya
		sums['sum_kuantitas_output'] = sum_kuantitas_output
		sums['sum_kualitas'] = sum_kualitas
		sums['sum_angka_kredit'] = sum_angka_kredit
		
		#self.xls_write_row(worksheet, filters, sums, parser, (size_of_result+20), sums_template, sum_style)
		
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
target_tahunan_report_xls_generator(
    #name (will be referred from target_tahunan_report.py, must add "report." as prefix)
    'report.target.tahunan.xls',
    #model
    'target.tahunan.report',
    #file
    'addons/df_report_target_tahunan/report/target_tahunan_report.xls',
    #parser
    parser=target_tahunan_report_parser,
    #header
    header=True
)