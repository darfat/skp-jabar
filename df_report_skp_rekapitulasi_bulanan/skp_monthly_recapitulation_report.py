from osv import fields, osv


class skp_monthly_recapitulation_report(osv.osv_memory):
    
    _name = "skp.monthly.recapitulation.report"
    _columns = {
        'company_id'        : fields.many2one('res.company', 'OPD', required=True),
        'biro_id'        : fields.many2one('hr.employee.biro', 'Biro'),
        'period_year'       : fields.char('Periode Tahun', size=4, required=True),
        'period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')], 'Periode Bulan'
                                                     , required=True),
        'is_kepala_opd'       : fields.boolean('Hanya Kepala OPD'),
    }
    
    def get_skp_monthly_recapitulation_report(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'skp.monthly.recapitulation.report',
            'form': value
        }
	
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'skp.monthly.recapitulation.xls',
            'report_type': 'webkit',
            'datas': datas,
        }
    
skp_monthly_recapitulation_report()
