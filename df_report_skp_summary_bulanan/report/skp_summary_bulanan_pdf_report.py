from openerp.report import report_sxw
import pooler
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby
from report_webkit import webkit_report
from osv import fields, osv
from tools.translate import _
import netsvc
import tools
import decimal_precision as dp
import math

class skp_summary_bulanan_pdf_report(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(skp_summary_bulanan_pdf_report, self).__init__(cr, uid, name, context=context)
        
        self.localcontext.update({
            'get_skp_summary_bulanan' : self.get_skp_summary_bulanan,
            'get_company_logo' : self.get_company_logo,
            'get_period':self.get_period,
            'rounding_nol' : self._rounding_nol,
        })
        
    
        
    def get_skp_summary_bulanan(self, filters, context=None):
        period_year=filters['form']['target_period_year']
        period_month=filters['form']['target_period_month']
        company_id=filters['form']['company_id']
        biro_id=filters['form']['biro_id']
        kepala_opd=filters['form']['is_kepala_opd']
        skp_pool = self.pool.get('skp.employee')
        
        users_pool = self.pool.get('res.users')
        user_uid_obj = users_pool.browse(self.cr,self.uid,self.uid,context=None);
        is_evaluator=False;
        is_admin=False;
        
        for group in user_uid_obj.groups_id :
            if group.category_id.name =='Project' and group.name == 'Evaluasi BKD' :
                is_evaluator=True
            elif self.uid==1:
                is_admin=True
        
        data_filter= [] 
        
        
        if is_admin and not company_id:
            if period_month:
               data_filter= [('target_period_month','=',period_month),('target_period_year','=',period_year),
                                                         ] 
            else :
                data_filter= [('target_period_year','=',period_year),
                                                         ]
               
        elif is_evaluator and not company_id:
                company_to_find =[];
                company_to_find.append(user_uid_obj.company_id.id);
                for child_company in user_uid_obj.company_id.child_ids:
                    company_to_find.append(child_company.id);
                    if child_company.child_ids:
                        for child_of_mine in child_company.child_ids:
                            company_to_find.append(child_of_mine.id);
                if period_month:
                    data_filter= [('target_period_month','=',period_month),('target_period_year','=',period_year),
                                                                                 ('company_id','in',company_to_find),
                                                                                       ]
                else :
                    data_filter= [('target_period_year','=',period_year),
                                                                                 ('company_id','in',company_to_find),
                                                                                       ]   
        elif (is_admin or is_evaluator) and company_id:
            if period_month:
                data_filter= [('target_period_month','=',period_month),('target_period_year','=',period_year),
                                                                             ('company_id','=',company_id[0])]
            else :
                data_filter= [('target_period_year','=',period_year),
                                                                             ('company_id','=',company_id[0])]
        else :
            if period_month:
                data_filter=[('target_period_month','=',period_month),('target_period_year','=',period_year),
                                                                             ('user_id','=',self.uid),
                                ]
            else :
                data_filter=[('target_period_year','=',period_year),
                                                                             ('user_id','=',self.uid),
                                ]
        if biro_id:
            data_filter.append(('biro_id','=',biro_id[0]),)
        if kepala_opd:
            data_filter.append(('is_kepala_opd','=',True),)
        
        skp_ids = skp_pool.search(self.cr,self.uid,data_filter,order='company_id,biro_name,department_name,employee_id');
        results_skp=skp_pool.browse(self.cr,self.uid,skp_ids)
        
        return results_skp
    
    def get_company_logo(self, filters, context=None):
        users_pool = self.pool.get('res.users')
        user_uid_obj = users_pool.browse(self.cr,self.uid,self.uid,context=None);
        if user_uid_obj:
            if user_uid_obj.company_id.logo :
                return user_uid_obj.company_id.logo
        else :
            user_uid_obj = users_pool.browse(self.cr,self.uid,1,context=None);
        return user_uid_obj.company_id.logo
    def get_period(self,filters):
        bulan ='';
        year='';
        if filters['form']['target_period_month']:
            month = filters['form']['target_period_month']
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
        if filters['form']['target_period_year']:
            year = filters['form']['target_period_year']
        return bulan+ "  " + year
        
    def _rounding_nol(self,num):
        orig=num
        if not orig :return 0;
        whole = math.floor(orig)
        frac = orig-whole
        
        if frac == 0.0 :
            return int(orig);
        
        return num
report_sxw.report_sxw('report.skp.summary.bulanan.report.form',
                        'skp.summary.bulanan.report', 
                        'addons/df_report_skp_summary_bulanan/report/skp_summary_bulanan_pdf_report.mako', parser=skp_summary_bulanan_pdf_report)
# report_sxw.report_sxw('report.penjualan.form', 'report.keuangan', 'addons/ad_laporan_keuangan/report/salesreport.mako', parser=ReportKeu)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: