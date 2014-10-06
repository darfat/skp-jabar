import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class target_tahunan_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(target_tahunan_report_parser, self).__init__(cr, uid, name, context=context)

    def get_target_tahunan_report_raw(self,filters,context=None):
        project_pool = self.pool.get('project.project')
        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        
        filter_status=[]
        if filters['form']['draft'] : filter_status.append('draft')
        if filters['form']['new'] : filter_status.append('new')
        if filters['form']['propose'] : filter_status.append('propose')
        if filters['form']['evaluated'] : filter_status.append('evaluated')
        if filters['form']['confirm'] : filter_status.append('confirm')
        if filters['form']['deleted'] : filter_status.append('deleted')
        
        users_pool = self.pool.get('res.users')
        user_uid_obj = users_pool.browse(self.cr,self.uid,self.uid,context=None);
        is_evaluator=False;
        for group in user_uid_obj.groups_id :
            if group.category_id.name =='Project' and group.name == 'Evaluasi BKD' :
                is_evaluator=True
            elif self.uid==1:
                is_evaluator=True
        if not is_evaluator :
               project_ids = project_pool.search(self.cr,self.uid,[('target_period_year','=',period_year),
                                                                             ('user_id','=',self.uid),
                                                                             ('state','in',filter_status),]);
        elif company_id :
               project_ids = project_pool.search(self.cr,self.uid,[('target_period_year','=',period_year),
                                                                             ('company_id','=',company_id[0]),
                                                                             ('state','in',filter_status),]);
        else :
                company_to_find =[];
                company_to_find.append(user_uid_obj.company_id.id);
                for child_company in user_uid_obj.company_id.child_ids:
                    company_to_find.append(child_company.id);
                    
                project_ids = project_pool.search(self.cr,self.uid,[('target_period_year','=',period_year),
                                                                             ('company_id','in',company_to_find),
                                                                             ('state','in',filter_status),]);
                
        results = project_pool.browse(self.cr, self.uid, project_ids)
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
    
        if filters['form']['period_year']:
            year = filters['form']['period_year']
        return year
        
    def get_lookup_state(self,state):
        str_state='';
        if state:
            if state == 'draft':
                str_state = "Draft"
            elif state == 'new':
                str_state = "Baru"
            elif state == 'propose':
                str_state = "Pengajuan Atasan"
            elif state == 'evaluated':
                str_state = "Verifikasi BKD"
            elif state == 'confirm':
                str_state = "Target Di Terima"
            elif state == 'deleted':
                str_state = "Batal"
       
        return str_state
    def get_lookup_target_type(self,state):
        str_return='';
        if state:
            if state == 'dipa_apbn':
                str_return = "Kegiatan Pada Daftar Isian Pelaksanaan Anggaran (DIPA) APBN"
            elif state == 'dpa_opd_biro':
                str_return = "Kegiatan Pada Daftar Pelaksanaan Anggaran (DPA) OPD/Biro"
            elif state == 'sotk':
                str_return = "Uraian Tugas Sesuai Peraturan Gubernur Tentang SOTK OPD/Biro"
            elif state == 'lain_lain':
                str_return = "Lain-Lain"
         
       
        return str_return
