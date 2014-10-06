from osv import osv
from osv import fields
from tools.translate import _
from openerp import netsvc
from openerp import pooler
from datetime import datetime,timedelta
import time
from mx import DateTime

class project_task_generate(osv.osv):
    _name = "project.task.generate"
    _description = "project.task.generate"
    def get_employee_from_user_id(self, cr, uid, task_generate, context=None):
        user_id  = task_generate.user_id
        if user_id : 
            return user_id.partner_id
        return False
    _columns = {
        'name'     : fields.char('Nama Kegiatan', size=128, required=True),
        'target_type_id': fields.selection([ ('tambahan', 'Tugas Tambahan Dan Kreativitas'),
                                             ('perilaku', 'Perilaku Kerja')], 'Jenis Kegiatan', required=True
                                           ),
        'lama_kegiatan'     : fields.integer('Lama Kegiatan',readonly=True),
        'user_id': fields.many2one('res.users', 'Penanggung Jawab', ),
        'user_id_atasan': fields.many2one('res.users', 'Pejabat Penilai', ),
        'user_id_banding': fields.many2one('res.users', 'Atasan Pejabat Penilai', ),
        'user_id_bkd': fields.many2one('res.users', 'Pejabat Pengevaluasi (BKD)', ),
        'satuan_lama_kegiatan'     : fields.selection([('bulan', 'Bulan')],'Satuan Waktu Lama Kegiatan',readonly=True),
        'date_start'     : fields.date('Periode Awal Generate'),
        'target_period_year'     : fields.char('Periode Tahun', size=4, required=True),
        
        }
    _defaults = {
        'name' : "Realisasi Bulan ",
        'lama_kegiatan' : 12,
        'satuan_lama_kegiatan':'bulan',
        'target_period_year':lambda *args: time.strftime('%Y'),
        'user_id': lambda self, cr, uid, ctx: uid,
       
        }
    def generate_task_realisasi_bulanan(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        task =  {}
        
        task_pool = self.pool.get('project.task')
        stage_pool = self.pool.get('project.task.type')
        for task_generate in self.browse(cr, uid, ids, context=context):
            #check Duplicate
            #Init Field
            target_category='bulanan'
            description=''
            lama_kegiatan=task_generate.lama_kegiatan
            user_id = task_generate.user_id.id
            target_period_year = task_generate.target_period_year
            target_period_month='xx'
            date_start='xx'
            date_end='xx'
            company_id=None
            currency_id=None
            user_id_bkd=None
            employee = self.get_employee_from_user_id( cr, uid, task_generate);
            if user_id!=uid:
              raise osv.except_osv(_('Invalid Action!'),
                                             _('Anda Tidak Memiliki Priviledge Untuk Proses Ini.'))
            if not employee :
                raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Ada Beberapa Informasi Kepegawaian Belum Diisi, Khususnya Data Pejabat Penilai Dan Atasan Banding.'))
            else :
                company = employee.company_id
                company_id = company.id
                currency_id= employee.company_id.currency_id
                
                #print "company_id : ",company_id,' - ',currency_id
                
                if not company_id :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Unit Dinas Pegawai Belum Dilengkapi.'))
                #print "employee parent : ",employee.parent_id
                if not task_generate.user_id_bkd:
                    if not company.user_id_bkd :
                        raise osv.except_osv(_('Invalid Action, Data Dinas Kurang Lengkap'),
                                    _('Staff Pemeriksa Dari BKD Tidak Tersedia Untuk Unit Anda, Silahkan hubungi Admin Atau isi Data Pemeriksa.'))
                    else :
                        user_id_bkd = company.user_id_bkd.id
                else :
                    user_id_bkd=task_generate.user_id_bkd.id 
                if not employee.user_id_atasan :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Penilai Belum Terisi.'))
                if not employee.user_id_banding :
                    raise osv.except_osv(_('Invalid Action, Data Pegawai Tidak Lengkap'),
                                _('Proses Tidak Dapat Dilanjutkan Karena Data Pejabat Pengajuan Banding.'))
            
            user_id_atasan =task_generate.user_id_atasan.id
            user_id_banding=task_generate.user_id_banding.id 
            
            if not task_generate.user_id_atasan.id :
                user_id_atasan = employee.user_id_atasan.user_id.id
            if not task_generate.user_id_banding.id :
                user_id_banding = employee.user_id_banding.user_id.id
            
            task.update({
                           'project_id':None,
                           'user_id':user_id,
                           'company_id':company_id,
                           'description':description,
                           'name': task_generate.name,
                           'code': None,
                           'target_category': target_category,
                           #'sequence': target_obj.priority,
                           'target_type_id':task_generate.target_type_id,
                           'target_period_year': target_period_year,
                            'user_id_atasan': user_id_atasan or False,
                            'user_id_banding':user_id_banding or False,
                            'user_id_bkd':user_id_bkd or False,
                            'priority':'2',
                            'currency_id':currency_id,
                             'target_waktu' : 0,
                            'target_kualitas' : 0,
                            'target_jumlah_kuantitas_output' : 0,
                             'task_category':'non_skp',
                           })
            #Update Task Target Bulanan
            now=DateTime.today();
            first_task_id=None
            
            if task_generate.date_start :
                curr_date = DateTime.strptime(task_generate.date_start,'%Y-%m-%d')
            else :
                january=DateTime.Date(now.year,1,1)
                curr_date =  DateTime.strptime(january.strftime('%Y-%m-%d'),'%Y-%m-%d')
            first_date =curr_date
            #print "THIS IS A DATE ",curr_date
            for i in range(0,lama_kegiatan):
                
                next_date = curr_date + DateTime.RelativeDateTime(months=i)
                target_period_month=next_date.strftime('%m')
                task.update({
                           'target_period_month':target_period_month,
                           'name': '%s %s' % (task_generate.name,target_period_month),
                 })
                #Check Duplicate Do Not Create
                task_ids = task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_month','=',target_period_month),('target_period_year','=',target_period_year),
                                                ('target_type_id','=',task_generate.target_type_id),('work_state','!=','draft')], context=None)
                if task_ids:
                    continue;
                else : 
                    #Delete Duplicate
                    task_ids = task_pool.search(cr, uid, [('user_id','=',user_id),('target_period_month','=',target_period_month),('target_period_year','=',target_period_year),
                                                          ('target_type_id','=',task_generate.target_type_id),('work_state','=','draft')], context=None)
                    task_pool.unlink(cr, uid, task_ids, context=None)
            
                date_start='xx'
                date_end='xx'
                stage_ids = stage_pool.search(cr,uid,[('sequence','=',0)], context=None)
                work_state='draft';
                if stage_ids :
                    task.update({
                                'stage_id': stage_ids[0],
                                'work_state':work_state,
                                'state':'draft',
                                'currency_id':currency_id
                        })

                #insert task
                task_id = task_pool.create(cr, uid, task)
                
            
            
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'notification.generate.task',
                'target': 'new',
                'context': context,#['notif_booking'],
            }

project_task_generate()
