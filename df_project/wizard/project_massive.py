from openerp.osv import osv
from osv import fields
from openerp.tools.translate import _
from openerp import netsvc
from openerp import pooler

class project_massive(osv.osv):
    _name = "project.massive"
    _description = "project.massive"
    def verify_all_target(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        target_ids = pool_obj.get('project.project').read(cr, uid, context['active_ids'], ['state'], context=context)
        update_target_ids=[]
        for record in target_ids:
            if record['state'] != 'evaluated':
                raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Status Kegiatan Harus Dalam Status Verifikasi BKD."))
           
            update_target_ids.append(record['id'])
        
        if update_target_ids:
            pool_obj.get('project.project').set_confirm(cr,uid,update_target_ids,context=context);
            
        return {'type': 'ir.actions.act_window_close'}
   

project_massive()
class project_massive_evaluate_bkd(osv.osv):
    _name = "project.massive.evaluate.bkd"
    _description = "project.massive.evaluate.bkd"
    _columns = {
        'notes'     : fields.text('Catatan',required=True,help='Silahkan isi alasan kenapa proses ini dilakukan'),
    }
    def to_evalate_all_target(self, cr, uid, ids, context):
        
        if context is None:
            context = {}
        else :
            ctx = context.copy()
        
        ctx.update({'bypass_auth': True});
        pool_obj = pooler.get_pool(cr.dbname)
        for to_evaluated_obj in self.browse(cr, uid, ids):
            target_ids = pool_obj.get('project.project').read(cr, uid, context['active_ids'], ['state'], context=context)
            update_target_ids=[]
            for record in target_ids:
                if record['state'] != 'propose':
                    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Status Kegiatan Harus Dalam Status Penilaian Atasan."))
               
                update_target_ids.append(record['id'])
            
            if update_target_ids:
                pool_obj.get('project.project').set_evaluated(cr,uid,update_target_ids,context=ctx);
                pool_obj.get('project.project').write(cr, uid, update_target_ids, {'notes':to_evaluated_obj.notes}, context=ctx)
            
            
        return {'type': 'ir.actions.act_window_close'}
   

project_massive_evaluate_bkd()
class project_massive_accept_revision(osv.osv):
    _name = "project.massive.accept.revision"
    _description = "project.massive.accept.revision"
   
    def accept_all_revision(self, cr, uid, ids, context):
        
        if context is None:
            context = {}
        else :
            ctx = context.copy()
        
        ctx.update({'bypass_auth': True});
        pool_obj = pooler.get_pool(cr.dbname)
        for to_evaluated_obj in self.browse(cr, uid, ids):
            target_ids = pool_obj.get('project.project').read(cr, uid, context['active_ids'], ['state'], context=context)
            update_target_ids=[]
            for record in target_ids:
                if record['state'] != 'propose_correction':
                    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Status Kegiatan Harus Dalam Status Pengajuan Revisi Target."))
               
                update_target_ids.append(record['id'])
            
            if update_target_ids:
                for target_id in  update_target_ids :
                    pool_obj.get('project.project').set_correction_approve(cr,uid,[target_id],context=ctx);
                
            
            
        return {'type': 'ir.actions.act_window_close'}
   

project_massive_accept_revision()