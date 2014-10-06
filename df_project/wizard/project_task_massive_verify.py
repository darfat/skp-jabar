from openerp.osv import osv
from osv import fields
from openerp.tools.translate import _
from openerp import netsvc
from openerp import pooler


class project_task_massive_verify(osv.osv):
    _name = "project.task.massive.verify"
    _description = "project.task.massive.verify"
    _columns = {
        'notes'     : fields.text('Catatan',required=True,help='Isi Dengan Catatan Bahwa Kegiatan Akan Diajukan Ke BKD Bukan Oleh Atasan Langsung. Catatan ini akan menjadi bahan evaluasi untuk kegiatan berikutnya.'),
    }
    def ajukan_bkd_all_task(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        task_ids = pool_obj.get('project.task').read(cr, uid, context['active_ids'], ['work_state','target_type_id'], context=context)
        task_pool = pool_obj.get('project.task')
        update_task_ids=[]
        for to_evaluated_obj in self.browse(cr, uid, ids):
            for record in task_ids:
                if record['work_state'] not in ('propose'):
                    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Proses Ini Berlaku Hanya Jika Kegiatan Sedang Dalam Proses Penilaian Atasan."))
                if task_pool.get_auth_id(cr, uid, record['id'], 'user_id_bkd', context=context):
                    update_task_ids.append(record['id'])
                
            
            
            if update_task_ids:
               for task_id in update_task_ids:
                    task_pool.do_propose(cr, 1, task_id, context=context)
                    task_pool.write(cr, 1, task_id, {'notes_from_bkd':to_evaluated_obj.notes}, context=context)
                    #task_pool.set_status_pengajuan_bkd(cr,1,task_id,True,context=context)
                
                
        return {'type': 'ir.actions.act_window_close'}
   

project_task_massive_verify()