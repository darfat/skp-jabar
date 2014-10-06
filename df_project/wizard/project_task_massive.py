from openerp.osv import osv
from osv import fields
from openerp.tools.translate import _
from openerp import netsvc
from openerp import pooler

class project_task_massive(osv.osv):
    _name = "project.task.massive"
    _description = "project.task.massive"
    def verify_all_task(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        task_ids = pool_obj.get('project.task').read(cr, uid, context['active_ids'], ['work_state','target_type_id','target_realiasi_notsame','biaya_verifikasi_notsame','komitmen_verifikasi_notsame','nilai_sementara'], context=context)
        task_pool = pool_obj.get('project.task')
        update_task_ids=[]
        for record in task_ids:
            if record['work_state'] not in ('evaluated'):
                raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Status Kegiatan Harus Dalam Keadaan Verifikasi BKD."))
            if record['target_type_id'] in ('dipa_apbn','dpa_opd_biro','sotk','lain_lain'):
                #if record['biaya_verifikasi_notsame']:
                #    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Realisasi Biaya Tidak Sama Dengan Data Verifikasi."))
                if record['nilai_sementara'] < 100 :
                    if record['target_realiasi_notsame']:
                        raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Realisasi Tidak Sama Dengan Target. Harap Cek 1 Persatu."))
                    
            if record['target_type_id'] in ('perilaku'):
                if record['komitmen_verifikasi_notsame']:
                    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Realisasi Penilaian Komitmen Tidak Sama Dengan Data Verifikasi."))
            if task_pool.get_auth_id(cr, uid, record['id'], 'user_id_bkd', context=context):
                update_task_ids.append(record['id'])
            
        
        
        if update_task_ids:
           for task_id in update_task_ids:
                task_pool.do_work_done(cr, uid, task_id, context=context)
                task_pool.do_task_poin_calculation(cr, uid, task_id, context=context)
                task_pool.do_task_summary_calculation(cr, uid, task_id, 1, context=context)
                
        return {'type': 'ir.actions.act_window_close'}
   

project_task_massive()

class project_task_recalculate_massive(osv.osv):
    _name = "project.task.recalculate.massive"
    _description = "project.task.recalculate.massive"
    def recalculate_all_task(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        task_ids = pool_obj.get('project.task').read(cr, uid, context['active_ids'], ['work_state','target_type_id','target_realiasi_notsame','biaya_verifikasi_notsame','komitmen_verifikasi_notsame'], context=context)
        task_pool = pool_obj.get('project.task')
        update_task_ids=[]
        for record in task_ids:
            if record['work_state'] not in ('done'):
                raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Proses Ini Berlaku Hanya Jika Kegiatan Sudah selesai dilakukan perhitungan Oleh BKD."))
            if task_pool.get_auth_id(cr, uid, record['id'], 'user_id_bkd', context=context):
                update_task_ids.append(record['id'])
            
        
        
        if update_task_ids:
           for task_id in update_task_ids:
                task_pool.do_work_done(cr, uid, task_id, context=context)
                task_pool.do_task_poin_calculation(cr, uid, task_id, context=context)
                task_pool.do_task_summary_calculation(cr, uid, task_id, 1, context=context)
                
        return {'type': 'ir.actions.act_window_close'}
   

project_task_recalculate_massive()
class project_task_reject_notarget(osv.osv):
    _name = "project.task.reject.notarget"
    _description = "project.task.reject.notarget"
    _columns = {
        'notes'     : fields.text('Catatan',required=True,help='Isi Dengan Catatan Bahwa Realisasi Harus Dibatalkan Karena Tidak Memiliki Target Tahunan'),
    }
    def reject_notarget(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        task_ids = pool_obj.get('project.task').read(cr, uid, context['active_ids'], ['work_state','target_type_id','project_id'], context=context)
        task_pool = pool_obj.get('project.task')
        update_task_ids=[]
        for to_evaluated_obj in self.browse(cr, uid, ids):
            for record in task_ids:
     
                
                if record['target_type_id'] not in ('dipa_apbn','dpa_opd_biro','sotk','lain_lain'):
                    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Terdapat Kegiatan Selain SKP Yang Akan Ditolak."))
                if record['target_type_id'] in ('dipa_apbn','dpa_opd_biro','sotk','lain_lain'):
                    if  record['project_id']:
                        raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Terdapat Kegiatan Yang Sudah Memiliki Target Yang Akan Ditolak."))
                if task_pool.get_auth_id(cr, uid, record['id'], 'user_id_bkd', context=context):
                    update_task_ids.append(record['id'])
                
            
            
            if update_task_ids:
               for task_id in update_task_ids:
                    task_pool.do_target_done(cr, 1, task_id, context=context)
                    task_pool.write(cr, 1, task_id, {'notes_from_bkd':to_evaluated_obj.notes}, context=context)
                
        return {'type': 'ir.actions.act_window_close'}
   

project_task_reject_notarget()
class project_task_calculate_temp_poin(osv.osv):
    _name = "project.task.calculate.temp.poin"
    _description = "project.task.calculate.temp.poin"
    
    def calculate_nilai_sementara(self, cr, uid, ids, context=None):
        
        if context is None:
            context = {}
        pool_obj = pooler.get_pool(cr.dbname)
        task_ids = pool_obj.get('project.task').read(cr, uid, context['active_ids'], ['work_state','target_type_id','project_id'], context=context)
        task_pool = pool_obj.get('project.task')
        update_task_ids=[]
        for to_evaluated_obj in self.browse(cr, uid, ids):
            for record in task_ids:
     
                
                if record['work_state'] in ('done'):
                    raise osv.except_osv(_('Warning!'), _("Proses Tidak Bisa Dilanjutkan, Karena Terdapat Kegiatan Sudah Selesai Dinilai."))
                
                if task_pool.get_auth_id(cr, uid, record['id'], 'user_id_bkd', context=context):
                    update_task_ids.append(record['id'])
                
            
            
            if update_task_ids:
               for task_id in update_task_ids:
                    task_pool.do_task_temp_poin_calculation(cr, uid, task_id, context=context)
                    
                
        return {'type': 'ir.actions.act_window_close'}
   

project_task_calculate_temp_poin()

