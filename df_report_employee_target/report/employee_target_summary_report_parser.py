import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class employee_target_summary_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(employee_target_summary_report_parser, self).__init__(cr, uid, name, context=context)

    def get_employee_target_summary_report_raw(self,filters,context=None):

        period_year=filters['form']['period_year']
        company_id=filters['form']['company_id']
        
        query = """
        select e.employee_id ,e.user_id,e.employee_nip,e.employee_name,
                j.name jabatan,
                    d.name bidang,
                    c.name company_name ,
                    biro.name biro_name,
                    sum(draft.cnt) count_draft,
                    sum(new.cnt) count_new,
                    sum(propose.cnt) count_propose,
                    sum(rejected_manager.cnt) count_rejected_manager,
                    sum(evaluated.cnt) count_evaluated,
                    sum(rejected_bkd.cnt) count_rejected_bkd,
                    sum(confirm.cnt) count_confirm,
                    sum(propose_correction.cnt) count_propose_correction,
                    sum(correction.cnt) count_correction
            from( select    emp.id employee_id ,emp.user_id user_id ,
                    emp.nip employee_nip,emp.name employee_name,
                    emp.company_id,emp.job_id, emp.department_id,emp.biro_id
                from res_partner emp
                where employee and user_id notnull) e
                left join
                            res_company c on c.id = e.company_id
                    left join
                            hr_job j on j.id = e.job_id
                    left join
                            hr_department d on d.id = e.department_id
                    left join hr_employee_biro biro on biro.id = e.biro_id
                    left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'draft'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) draft on draft.user_id = e.user_id
         left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'new'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) new on new.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'propose'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) propose on propose.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'rejected_manager'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) rejected_manager on rejected_manager.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'evaluated'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) evaluated on evaluated.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'rejected_bkd'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) rejected_bkd on rejected_bkd.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'confirm'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) confirm on confirm.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'propose_correction'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) propose_correction on propose_correction.user_id = e.user_id
        left join 
            (select count(p.id) cnt,aac.user_id,p.state, target_period_month ,target_period_year from project_project p,account_analytic_account aac
              where p.state = 'correction'
                and target_period_year = %s   
                and p.analytic_account_id = aac.id
               group by aac.user_id,p.state, target_period_month ,target_period_year
            ) correction on correction.user_id = e.user_id
            where e.company_id = %s
        group by e.employee_id ,e.user_id,e.employee_nip,e.employee_name,j.name, d.name,c.name,biro.name
                order by c.name,biro.name,d.name,e.employee_name
        """
        employee_results = []
        
        domain = period_year,period_year,period_year,period_year,period_year,period_year,period_year,period_year,period_year,company_id[0]
        self.cr.execute(query,domain)
        result = self.cr.fetchall()
        idx=1
        for employee_id,user_id,employee_nip,employee_name,jabatan,bidang,company_name,biro_name,count_draft,count_new,count_propose,count_rejected_manager,count_evaluated,count_rejected_bkd,count_confirm,count_propose_correction,count_correction in result:
            new_dict = {}
            new_dict['idx'] = idx
            new_dict['employee_id'] = str(employee_id)
            new_dict['employee_nip'] = employee_nip
            new_dict['jabatan'] = jabatan
            new_dict['bidang'] = bidang
            new_dict['employee_name'] = employee_name
            new_dict['company_name'] = company_name
            new_dict['biro_name'] = biro_name
            new_dict['user_id'] = 'Belum Aktifasi' 
            if user_id : new_dict['user_id'] = 'Sudah Aktifasi' 
            new_dict['count_draft'] = count_draft
            new_dict['count_new'] = count_new      
            new_dict['count_propose'] = count_propose
            new_dict['count_rejected_manager'] = count_rejected_manager      
            new_dict['count_propose_correction'] = count_propose_correction
            new_dict['count_correction'] = count_correction  
            new_dict['count_evaluated'] = count_evaluated
            new_dict['count_rejected_bkd'] = count_rejected_bkd      
            new_dict['count_confirm'] = count_confirm
            employee_results.append(new_dict)
            idx+=1
        
    
        return employee_results;
    def get_company(self,filters):
        company_id=filters['form']['company_id']
        if not company_id :
            return ''
        return company_id[1]
    def get_title_period(self,prefiks,filters):
        period_year=filters['form']['period_year']
        
        str_period = period_year
      
        return prefiks+ " "+str_period
    
   
    
