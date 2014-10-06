from osv import fields, osv
import time


class employee_target_summary_report(osv.osv_memory):
    
    _name = "employee.target.summary.report"
    _columns = {
        'company_id'        : fields.many2one('res.company', 'OPD', required=True),
        'period_year'          : fields.char('Periode',size=4,required=True),
    }
    _defaults = {
        'period_year':lambda *args: time.strftime('%Y'),
        
    }
    def get_employee_target_summary_report(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'employee.target.summary.report',
            'form': value
        }
	
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'employee.target.summary.xls',
            'report_type': 'webkit',
            'datas': datas,
        }
    
employee_target_summary_report()
