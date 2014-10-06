from osv import fields, osv


class employee_realisasi_summary_report(osv.osv_memory):
    
    _name = "employee.realisasi.summary.report"
    _columns = {
        'company_id'        : fields.many2one('res.company', 'OPD'),
        'period_year'       : fields.char('Periode Tahun', size=4, required=True),
        'period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')], 'Periode Bulan'
                                                     , required=True),
        'type'          : fields.selection([('xls','Excel')],'File Type',required=True),
    }
    
    def get_employee_realisasi_summary_report(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'employee.realisasi.summary.report',
            'form': value
        }
	
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'employee.realisasi.summary.xls',
            'report_type': 'webkit',
            'datas': datas,
        }
    
employee_realisasi_summary_report()
