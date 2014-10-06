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

class res_users(osv.osv):
    _inherit = 'res.users'
    _description    ="Res Users Custom"
   
    def penjadwalan_input_skp_per_opd(self, cr, uid,ids, context=None):
        print "Penjadwalan IDS : ",ids
        company_ids_to_deactive=[]
        company_pool = self.pool.get('res.company')
        all_company_ids = company_pool.search(cr,uid,[],context=None);
        print "Jumlah Semua OPD... ",len(all_company_ids);
        for company_id in all_company_ids :
            if company_id not in ids :
                company_ids_to_deactive.append(company_id);
        
        cr.execute('update res_users set active=%s where company_id IN %s ', (False, tuple(company_ids_to_deactive)))
        print "Jumlah OPD Yang Aktif... ",len(ids);
        cr.execute('update res_users set active=%s where company_id IN %s ', (True, tuple(ids)))
        
        return True
    
res_users()


