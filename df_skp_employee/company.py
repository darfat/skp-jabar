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

class notification_company_summary_target(osv.osv_memory):
    _name = "notification.company.summary.target"
    _columns = {
        'name': fields.char('Notif', size=128),
    }
notification_company_summary_target();

class res_company(osv.osv):
    _inherit = 'res.company'
    def action_company_summary_target(self, cr, uid, ids, context=None):
        res = {}
        target_pool = self.pool.get('project.project')
        task_pool = self.pool.get('project.task')
        employee_pool = self.pool.get('res.partner')
        try :
            for company_obj in self.browse(cr,uid,ids,context=context) :
                employee_ids = employee_pool.search(cr, uid, [('company_id', '=', company_obj.id),], context=None)
                
                for employee in employee_pool.browse(cr, uid, employee_ids, context=context) :
                    if employee.user_id and employee.user_id.id :
                        
                        target_ids = target_pool.search(cr, uid, [('user_id', '=', employee.user_id.id),
                                                                  ('state', 'in', ('confirm','closed')),
                                                               ], context=context)
                        for target_obj in target_pool.browse(cr, uid, target_ids, context=context) :
                            task_pool.do_target_summary_calculation(cr, uid, target_obj, context)
                            task_pool.do_skp_summary_calculation(cr,uid,target_obj.user_id,target_obj.employee_id,target_obj.target_period_year, context=None)
        except :
            print "cannot generated...."
        return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'notification.company.summary.target',
                'target': 'new',
                'context': context,
            }
res_company()