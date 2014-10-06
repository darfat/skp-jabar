from openerp.osv import fields, osv
import time
from mx import DateTime


class skp_recap_yearly_report(osv.osv_memory):
    
    _name = "skp.recap.yearly.report"
    _columns = {
        'period_year'       : fields.char('Periode Tahun', size=4, required=True),
        'print_date'       : fields.date('Tanggal Pengesahan',  required=True),
        'company_id'        : fields.many2one('res.company', 'OPD',),
        'user_id'        : fields.many2one('res.users', 'Penanggung Jawab'),
        
    }
    _defaults = {
        'period_year':lambda *args: time.strftime('%Y'),
        'print_date': lambda *args: time.strftime('%Y-%m-%d'),
        'user_id': lambda self, cr, uid, ctx: uid,
    }
    def get_skp_recap_yearly_report(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'skp.recap.yearly.report',
            'form': value
        }
	
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'skp.recap.yearly.xls',
            'report_type': 'webkit',
            'datas': datas,
        }
    
skp_recap_yearly_report()
