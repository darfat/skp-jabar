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

from osv import fields, osv
from datetime import datetime,timedelta
import time
from mx import DateTime
from tools import html_email_clean

_DATA = [('draft','Draft'),('new','Baru'),
                                   ('propose','Penilaian Atasan'), ('rejected_manager', 'Penilaian Ditolak'),
                                   ('evaluated','Verifikasi BKD'), ('rejected_bkd', 'Pengajuan Ditolak BKD'),
                                   ('confirm','Target Di Terima'), 
                                   ('pending','Pending'),
                                   ('propose_to_close','Pengajuan Closing Target'),('closed','Closed'),
                                   ('deleted', 'Batal'),
                                   ('propose_correction', 'Ajukan Perubahan Target'),
                                   ('correction', 'Revisi Target'),
                                   ]
_DATA_TASK = [('draft', 'Draft'), ('realisasi', 'Realisasi'),
                                        ('propose', 'Atasan'), ('rejected_manager', 'Pengajuan Ditolak Atasan'),
                                        ('appeal', 'Banding'), ('evaluated', 'BKD'), ('rejected_bkd', 'Pengajuan Ditolak BKD'),
                                        ('propose_to_close','Pengajuan Closing Target'),('closed','Closed'),
                                        ('done', 'Selesai'), ('cancelled', 'Cancel')]
class message_notification(osv.osv):
    _name = 'message.notification'
    
    
    
    def lookup_state_name(self,state):
        for in_data in _DATA :
            if in_data[0] == state :
                return in_data[1];
        return state
    def lookup_task_state_name(self,state):
        for in_data in _DATA_TASK :
            if in_data[0] == state :
                return in_data[1];
        return state
    def write_project_notification(self, cr, uid, id,v_title,v_nama_kegiatan,v_catatan,v_state, context=None):
            mail_message_pool = self.pool.get('mail.message')
            #'<div> &nbsp; &nbsp; &bull; <b>Status</b>: %s</div>'\
            vals = (
                    '<div>  <b>%s</b> </div>'\
                    '<div> &nbsp; &nbsp; &bull; <b>Status</b>: %s</div>'\
                    '<div> &nbsp; &nbsp; &bull; <b>Nama Kegiatan</b>: %s</div>'\
                    '' % (v_title,self.lookup_state_name    (v_state),v_nama_kegiatan))
            body_html = html_email_clean(vals)
            values = {
                    'body': body_html,
                    'model': 'project.project',
                    'record_name': v_nama_kegiatan,
                    'type': 'notification',
                    'res_id': id,                    
                }
            message_id = mail_message_pool.create(cr, uid, values,context)
            
            return True;
    def write_project_task_notification(self, cr, uid, id,v_title,v_nama_kegiatan,v_catatan,v_state, context=None):
            mail_message_pool = self.pool.get('mail.message')
            #'<div> &nbsp; &nbsp; &bull; <b>Status</b>: %s</div>'\
            vals = (
                    '<div>  <b>%s</b> </div>'\
                    '<div> &nbsp; &nbsp; &bull; <b>Status</b>: %s</div>'\
                    '<div> &nbsp; &nbsp; &bull; <b>Nama Kegiatan</b>: %s</div>'\
                    '' % (v_title,self.lookup_task_state_name(v_state),v_nama_kegiatan))
            body_html = html_email_clean(vals)
            values = {
                    'body': body_html,
                    'model': 'project.task',
                    'record_name': v_nama_kegiatan,
                    'type': 'notification',
                    'res_id': id,                    
                }
            message_id = mail_message_pool.create(cr, uid, values,context)
            
            return True;
message_notification()


class project_task(osv.osv):
    _inherit = 'project.task'
    def write(self, cr, uid, ids, vals, context=None):
        if not isinstance(ids, list): ids = [ids]
        super(project_task, self).write(cr, uid, ids, vals, context=context)   
        m_notif_pool = self.pool.get('message.notification')        
        for task_obj in self.browse(cr, uid, ids, context=context):
            if vals.get('work_state',False):
                m_notif_pool.write_project_task_notification(cr,uid,task_obj.id,
                                                        'Perubahan Status',
                                                        task_obj.name or '-' ,
                                                        task_obj.notes or '-' , 
                                                        task_obj.work_state,
                                                    context)
                
        return True
        
    
project_task()