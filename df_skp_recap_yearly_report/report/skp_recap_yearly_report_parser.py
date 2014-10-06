import openerp.pooler
import time
from datetime import datetime
import openerp.tools
import logging
from openerp.report import report_sxw
from datetime import datetime
from openerp.addons.report_webkit import webkit_report
from tools.translate import _
from openerp.osv import osv
import math
import locale

class skp_recap_yearly_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        locale.setlocale(locale.LC_ALL, 'id_ID.utf8')
        super(skp_recap_yearly_report_parser, self).__init__(cr, uid, name, context=context)

    def get_skp_recap_yearly_report_raw(self,filters,context=None):
        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        user_id = False
        if filters['form']['user_id']:
            user_id=filters['form']['user_id'][0]
        target_pool = self.pool.get('project.project')
        target_ids=target_pool.search(self.cr, self.uid, [('state','in',('confirm','closed')),('target_period_year','=',period_year),('user_id','=',user_id)], context=None)
        results = target_pool.browse(self.cr, self.uid, target_ids)
        return results;
    def get_atribut_kepegawaian(self,filters,context=None):
        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        user_id = False
        data_pegawai=None
        if filters['form']['user_id']:
            user_id=filters['form']['user_id'][0]
        target_pool = self.pool.get('project.project')
        target_ids=target_pool.search(self.cr, self.uid, [('state','in',('confirm','closed')),('target_period_year','=',period_year),('user_id','=',user_id),], context=None)
        if target_ids:
            result = target_pool.browse(self.cr, self.uid, target_ids)[0]
            if  result.user_id and result.employee_id:
                print result.employee_id
                data_pegawai = result.employee_id
        return data_pegawai;
    def get_nilai_tambahan_kreatifitas_data(self,filters,context=None):
        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        user_id = False
        if filters['form']['user_id']:
            user_id=filters['form']['user_id'][0]
        
        query = """
        select 
            sum(fn_nilai_tambahan),count(fn_nilai_tambahan),
            sum(fn_nilai_kreatifitas),count(fn_nilai_kreatifitas) 
        from skp_employee
        where user_id = %s and target_period_year =%s
        group by user_id,target_period_year
        """
        data_results = []
        
        domain = user_id, period_year
        self.cr.execute(query,domain)
        result = self.cr.fetchall()
        no_idx=1;
        for sum_nilai_tambahan,count_nilai_tambahan,sum_nilai_kreatifitas,count_nilai_kreatifitas in result:
            new_dict = {}
            new_dict['sum_nilai_tambahan'] = sum_nilai_tambahan
            new_dict['count_nilai_tambahan'] = count_nilai_tambahan
            new_dict['sum_nilai_kreatifitas'] = sum_nilai_kreatifitas
            new_dict['count_nilai_kreatifitas'] = count_nilai_kreatifitas
               
            
            data_results.append(new_dict)
            no_idx+=1
        if data_results:
            return data_results[0];
        return False;
    
    def get_recap_yearly_report_raw(self,filters,context=None):
        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        user_id = False
        if filters['form']['user_id']:
            user_id=filters['form']['user_id'][0]
        skp_yearly_pool = self.pool.get('skp.employee.yearly')
        skp_yearly_ids=skp_yearly_pool.search(self.cr, self.uid, [('target_period_year','=',period_year),('user_id','=',user_id)], context=None)
        results = skp_yearly_pool.browse(self.cr, self.uid, skp_yearly_ids)
        if results:
            return results[0];
        if not results :
            raise osv.except_osv(_('Laporan Tidak Bisa Di Download'),
                                    _('Belum ada rekapitulasi tahunan pegawai.'))
        
    def get_title(self,prefix,filters,context=None):
        period_year=filters['form']['period_year'];
        return prefix+' '+period_year
    def get_concat_with_format_date(self,str_prefix,filters,context=None):
        print_date=filters['form']['print_date'];
        formatted_print_date = time.strftime('%d %B %Y', time.strptime(print_date,'%Y-%m-%d'))
        return str_prefix+' '+formatted_print_date
    def get_concat_kuantitas_output(self,kuantitas_output,satuan,context=None):
        ret_qty=''
        ret_satuan =''
        if kuantitas_output:
            ret_qty = str(kuantitas_output)
        if satuan and satuan.name :
            ret_satuan = satuan.name
        return ret_qty+' '+ret_satuan
    def get_concat_nilai_perilaku(self,nilai_perilaku,pengali,context=None):
        str_nilai_perilaku=''
        
        if nilai_perilaku:
            str_nilai_perilaku = str(round(nilai_perilaku))
        ret_skp = "%s x %s" % (str_nilai_perilaku, pengali),
        return ret_skp
    def get_concat_nilai_skp(self,nilai_skp,pengali,tugas_tambahan,kreatifitas,context=None):
        str_nilai_skp=''
        str_tugas_tambahan='0'
        str_kreatifitas='0'
        if nilai_skp:
            str_nilai_skp = str(round(nilai_skp))
        if tugas_tambahan:
            str_tugas_tambahan = str(int(tugas_tambahan))
        if kreatifitas:
            str_kreatifitas = str(int(kreatifitas))
        ret_skp = "(%s x %s ) + %s + %s " % (str_nilai_skp, pengali,str_tugas_tambahan,str_kreatifitas),
        return ret_skp
        