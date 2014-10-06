from osv import fields, osv
import time

class target_tahunan_report(osv.osv_memory):
    
    _name = "target.tahunan.report"
    _columns = {
        'company_id'        : fields.many2one('res.company', 'OPD'),
        'period_year'       : fields.char('Periode Tahun', size=4, required=True),
        'draft'       : fields.boolean('Draft'),
        'new'       : fields.boolean('Baru'),
        'propose'       : fields.boolean('Pengajuan Atasan'),
        'evaluated'       : fields.boolean('Verifikasi BKD'),
        'confirm'       : fields.boolean('Target Di Terima'),
        'deleted'       : fields.boolean('Batal'),
    }
    _defaults = {
        'period_year':lambda *args: time.strftime('%Y'),
        'confirm':True
        
    }
    
    def get_target_tahunan_report(self, cr, uid, ids, context={}):
        value = self.read(cr, uid, ids)[0]
        datas = {
            'ids': context.get('active_ids',[]),
            'model': 'target.tahunan.report',
            'form': value
        }
	
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'target.tahunan.xls',
            'report_type': 'webkit',
            'datas': datas,
        }
    
target_tahunan_report()
