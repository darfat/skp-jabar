# -*- encoding: utf-8 -*-
##############################################################################
#
#    Darmawan Fatriananda
#    BKD Pemprov Jabar
#    Copyright (c) 2014 <http://www.asdarfat.wordpress.com.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields
from tools.translate import _
from datetime import datetime,timedelta
import time

class project_task_scheduler(osv.osv):
    _name = 'project.task.scheduler'
    _columns = {
        'notes'     : fields.text('Catatan',help='Auto Generate.'),
        'task_id'   : fields.integer('Task ID'),
        'user_id'   : fields.integer('User ID'),
        'company_id'   : fields.integer('Company ID'),
        'type': fields.selection([ ('success', 'Berhasil'),
                                            ('failed', 'Gagal'),
                                                      ], 'Jenis', 
                                                     ),
        'task_category': fields.selection([('skp', 'SKP'), ('non_skp', 'Perilaku, Tambahan dan Kreatifitas')], 'Kategori Kegiatan', ),
    }
    def auto_hitung_nilai_sementara(self, cr, uid, context=None):
        task_pool = self.pool.get('project.task')
        task_ids = task_pool.search(cr,uid, [('work_state', '=', 'evaluated'),], context=None)
        print "Hitung Nilai Sementara count..... : ",len(task_ids)
        
        success_task=[]
        fail_task=[]
        update_task_ids=[]
        task_history_data =  {}
        for task_obj in  task_pool.browse(cr,uid,task_ids,context):
            if not task_obj.nilai_sementara :
                try:
                    task_pool.do_task_temp_poin_calculation(cr, uid, task_obj.id, context=context)
                    success_task.append(task_obj)
                except : 
                    fail_task.append(task_obj)
            elif task_obj.nilai_sementara and task_obj.nilai_sementara == 0.0:
                try:
                    task_pool.do_task_temp_poin_calculation(cr, uid, task_obj.id, context=context)
                    success_task.append(task_obj)
                except : 
                    fail_task.append(task_obj)
            
        #insert into history
        for hist_data in success_task :
            task_history_data.update({
                        'task_id':hist_data.id,
                        'user_id':hist_data.user_id.id,
                        'company_id':hist_data.company_id.id,
                        'notes': hist_data.name,
                        'task_category':hist_data.task_category,
                        'type':'success'
                        })
            history_data = self.create(cr,uid,task_history_data)
            
        #for hist_data in fail_task :
        #    task_history_data.update({
        #                'task_id':hist_data.id,
        #                'user_id':hist_data.user_id.id,
        #                'company_id':hist_data.company_id.id,
        #                'notes': hist_data.name,
        #                'task_category':hist_data.task_category,
        #                'type':'failed'
        #                })
        #    history_data = self.create(cr,uid,task_history_data)
        return True
    
project_task_scheduler()


