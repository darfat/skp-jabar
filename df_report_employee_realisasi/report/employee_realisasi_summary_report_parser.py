import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class employee_realisasi_summary_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(employee_realisasi_summary_report_parser, self).__init__(cr, uid, name, context=context)

    def get_employee_realisasi_summary_report_raw(self,filters,context=None):
        period_year=filters['form']['period_year']
        period_month=filters['form']['period_month']
        company_id=filters['form']['company_id']
        
        if not company_id :
            users_pool = self.pool.get('res.users')
            user_uid_obj = users_pool.browse(self.cr,self.uid,self.uid,context=None);
            is_evaluator=False;
            is_admin=False;
            for group in user_uid_obj.groups_id :
                if group.category_id.name =='Project' and group.name == 'Evaluasi BKD' :
                    is_evaluator=True
                elif self.uid==1:
                    is_admin=True
            if is_admin : 
                query = """
                select e.id employee_id ,e.nip employee_nip,e.name_related employee_name,
                    j.name jabatan,t.target_type_id,
                    c.name company_name ,
                    r.user_id user_id ,u.login,
                    t.target_period_month,t.target_period_year,t.work_state,count(t.id)
                from hr_employee e
                left  join
                resource_resource r on e.resource_id = r.id
                left  join
                res_company c on c.id = r.company_id
                left  join
                hr_job j on j.id = e.job_id
                left  join 
                project_task t on t.user_id = r.user_id
                left  join
                res_users u on u.id = t.user_id_bkd
                where 
                t.target_period_month=%s
                and t.target_period_year = %s
                group by e.id,e.nip,e.name_related,c.name,r.user_id,j.name,t.work_state,u.login, 
                t.target_period_month,t.target_period_year,t.target_type_id
                order by c.name,e.nip
                    """
                domain = period_month, period_year
            else :
                company_to_find =[];
                
                str_company_to_find=" and r.company_id in ( "+str(user_uid_obj.company_id.id)+",";
                company_to_find.append(user_uid_obj.company_id.id);
                for child_company in user_uid_obj.company_id.child_ids:
                    company_to_find.append(child_company.id);
                    str_company_to_find=str_company_to_find+str((child_company.id))+",";
                str_company_to_find=str_company_to_find+"0)"
                    
                query = """
                   select e.id employee_id ,e.nip employee_nip,e.name_related employee_name,
                        j.name jabatan,t.target_type_id,
                        c.name company_name ,
                        r.user_id user_id ,u.login,
                        t.target_period_month,t.target_period_year,t.work_state,count(t.id)
                    from hr_employee e
                    left  join
                    resource_resource r on e.resource_id = r.id
                    left  join
                    res_company c on c.id = r.company_id
                    left  join
                    hr_job j on j.id = e.job_id
                    left  join 
                    project_task t on t.user_id = r.user_id
                    left  join
                    res_users u on u.id = t.user_id_bkd
                    where 
                    t.target_period_month=%s
                    and t.target_period_year = %s
                    %s
                    group by e.id,e.nip,e.name_related,c.name,r.user_id,j.name,t.work_state,u.login, 
                    t.target_period_month,t.target_period_year,t.target_type_id
                    order by c.name,e.nip
                    """
                domain = period_month, period_year,str_company_to_find
        else :
            query = """
           select e.id employee_id ,e.nip employee_nip,e.name_related employee_name,
                j.name jabatan,t.target_type_id,
                c.name company_name ,
                r.user_id user_id ,u.login,
                t.target_period_month,t.target_period_year,t.work_state,count(t.id)
            from hr_employee e
            left  join
            resource_resource r on e.resource_id = r.id
            left  join
            res_company c on c.id = r.company_id
            left  join
            hr_job j on j.id = e.job_id
            left  join 
            project_task t on t.user_id = r.user_id
            left  join
            res_users u on u.id = t.user_id_bkd
            where 
            t.target_period_month=%s
            and t.target_period_year = %s
            and r.company_id = %s
            group by e.id,e.nip,e.name_related,c.name,r.user_id,j.name,t.work_state,u.login, 
            t.target_period_month,t.target_period_year,t.target_type_id
            order by c.name,e.nip
            """
            domain = period_month, period_year,company_id[0]
        
        employee_results = []
        self.cr.execute(query,domain)
        result = self.cr.fetchall()
        for employee_id,employee_nip,employee_name,jabatan,target_type_id,company_name,user_id,verificator_login,target_period_month,target_period_year,status,count_of_task in result:
            new_dict = {}
            new_dict['employee_id'] = str(employee_id)
            new_dict['employee_nip'] = employee_nip
            new_dict['jabatan'] = jabatan
            new_dict['target_type_id'] = target_type_id
            new_dict['employee_name'] = employee_name
            new_dict['company_name'] = company_name
            new_dict['user_id'] = 'Belum Aktifasi' 
            if user_id : new_dict['user_id'] = str(user_id)   
            new_dict['verificator_login'] = verificator_login
            new_dict['target_period_month'] = target_period_month      
            new_dict['target_period_year'] = target_period_year
            new_dict['status'] = status  
            new_dict['count_of_task'] = count_of_task
            employee_results.append(new_dict)
        
    
        return employee_results;
    def get_title(self,prefiks,filters):
        
      
        return ''
    def get_period(self,p_month,p_year):
        bulan ='';
        year='';
        if p_month:
            month = p_month
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
        if p_year:
            year = p_year
        return bulan+ " " + year
        
    def get_lookup_state(self,state):
        str_state='';
        if state:
            if state == 'draft':
                str_state = "Draft"
            elif state == 'realisasi':
                str_state = "Realisasi"
            elif state == 'propose':
                str_state = "Penilaian Atasan"
            elif state == 'rejected_manager':
                str_state = "Penilaian Ditolak Atasan"
            elif state == 'appeal':
                str_state = "Banding"
            elif state == 'evaluated':
                str_state = "Verifikasi BKD"
            elif state == 'rejected_bkd':
                str_state = "Verifikasi Ditolak BKD"
            elif state == 'done':
                str_state = "Selesai"
            elif state == 'cancelled':
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
            elif state == 'tambahan':
                str_return = "Tugas Tambahan Dan Kreativitas"
            elif state == 'perilaku':
                str_return = "Perilaku Kerja"
       
        return str_return
   
    
