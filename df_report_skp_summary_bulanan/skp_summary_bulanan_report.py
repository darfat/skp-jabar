

import time
import netsvc
from tools.translate import _
import tools
from datetime import datetime, timedelta
from osv import fields, osv
from dateutil.relativedelta import relativedelta


import decimal_precision as dp

class skp_summary_bulanan_report(osv.osv_memory):
    _name = "skp.summary.bulanan.report"
    
    _columns = {
        'target_period_month'     : fields.selection([('01', 'Januari'), ('02', 'Februari'),
                                                      ('03', 'Maret'), ('04', 'April'),
                                                      ('05', 'Mei'), ('06', 'Juni'),
                                                      ('07', 'Juli'), ('08', 'Agustus'),
                                                      ('09', 'September'), ('10', 'Oktober'),
                                                      ('11', 'November'), ('12', 'Desember')],'Periode Bulan', 
                                                     ),
        'target_period_year'     : fields.char('Periode Tahun',size=4, required=True),
        'paging_data'     : fields.integer('Data per Halaman',required=True),
        'company_id' : fields.many2one('res.company', 'Unit Kerja / OPD', ),
        'biro_id'        : fields.many2one('hr.employee.biro', 'Biro'),
        'is_kepala_opd'       : fields.boolean('Hanya Kepala OPD'),
        #'employee_id' : fields.many2one('hr.employee', 'PNS Yang Dinilai', ),
    } 
    _defaults = {
                 'paging_data'     :20
                 }
    def compute_rep(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        
        datas = {
             'ids': context.get('active_ids',[]),
             'model': 'skp.summary.bulanan.report',
             'form': value
                 }
        
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'skp.summary.bulanan.report.form',
            #'report_type': 'webkit',
            'datas': datas,
            }
skp_summary_bulanan_report()