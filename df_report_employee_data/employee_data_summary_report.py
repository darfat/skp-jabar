from osv import fields, osv


class employee_data_summary_report(osv.osv_memory):
    
    _name = "employee.data.summary.report"
    _columns = {
        'type'          : fields.selection([('xls','Excel')],'File Type'),
    }
    
    def get_employee_data_summary_report(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'employee.data.summary.report',
            'form': value
        }
	
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'employee.data.summary.xls',
            'report_type': 'webkit',
            'datas': datas,
        }
    
employee_data_summary_report()
