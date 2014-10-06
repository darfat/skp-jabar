import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class skp_recap_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(skp_recap_report_parser, self).__init__(cr, uid, name, context=context)

    def get_skp_recap_report_raw(self,filters,context=None):
        skp_employee_pool = self.pool.get('skp.employee')
        period_month=filters['form']['period_month']
        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        biro_id=filters['form']['biro_id']
        kepala_opd=filters['form']['is_kepala_opd']
        data_filter= [] 
        
        if company_id :
            data_filter = [('target_period_month','=',period_month),
                          ('target_period_year','=',period_year),
                          ('company_id','=',company_id[0]),]
        else :
          if self.uid == 1:
            data_filter = [('target_period_month','=',period_month),
                          ('target_period_year','=',period_year),
                         ]

          else :
            users_pool = self.pool.get('res.users')
            user_uid_obj = users_pool.browse(self.cr,self.uid,self.uid,context=None);
            company_to_find =[];
            company_to_find.append(user_uid_obj.company_id.id);
            for child_company in user_uid_obj.company_id.child_ids:
                company_to_find.append(child_company.id);
                if child_company.child_ids:
                    for child_of_mine in child_company.child_ids:
                        company_to_find.append(child_of_mine.id);
            data_filter = [('target_period_month','=',period_month),
                           ('target_period_year','=',period_year),
                           ('company_id','in',company_to_find),];
        
        if biro_id:
            data_filter.append(('biro_id','=',biro_id[0]),)
        if kepala_opd:
            data_filter.append(('is_kepala_opd','=',True),)
        
        skp_employee_ids = skp_employee_pool.search(self.cr,self.uid,data_filter);
        results = skp_employee_pool.browse(self.cr, self.uid, skp_employee_ids)
        return results
    def get_opd_name_filter(self,prefiks,filters):
        if not filters['form']['company_id'] : return prefiks;

        title_company_name = filters['form']['company_id'][1]
        return prefiks+ " " + title_company_name
    def get_title(self,prefiks,filters):
        if not filters['form']['company_id'] : return prefiks;

        title_company_name = filters['form']['company_id'][1]
        return prefiks+ " " + title_company_name
    def get_period(self,filters):
        bulan ='';
        year='';
        if filters['form']['period_month']:
            month = filters['form']['period_month']
            if month == '10':
                bulan = "Oktober"
            elif month == '11':
                bulan = "November"
            elif month == '12':
                bulan = "Desember"
            elif month == '01':
                bulan = "Januari"
            elif month == '02':
                bulan = "Februari"
            elif month == '03':
                bulan = "Maret"
            elif month == '04':
                bulan = "April"
            elif month == '05':
                bulan = "Mei"
            elif month == '06':
                bulan = "Juni"
            elif month == '07':
                bulan = "Juli"
            elif month == '08':
                bulan = "Agustus"
            elif month == '09':
                bulan = "September"
        if filters['form']['period_year']:
            year = filters['form']['period_year']
        return bulan+ " " + year
        
   
    
