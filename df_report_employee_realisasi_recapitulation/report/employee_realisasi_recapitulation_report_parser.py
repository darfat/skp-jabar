import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class employee_realisasi_recapitulation_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(employee_realisasi_recapitulation_report_parser, self).__init__(cr, uid, name, context=context)

    def get_employee_realisasi_recapitulation_report_raw(self,filters,context=None):
        period_year=filters['form']['period_year']
        period_month=filters['form']['period_month']
        company_id=filters['form']['company_id']
        
        if company_id[0] == 1 :
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
                select e.employee_id ,e.user_id,e.employee_nip,e.employee_name,
                j.name jabatan,
                    d.name bidang,
                    c.name company_name ,
                    biro.name biro_name,
                    sum(draft.cnt) count_draft,
                    sum(realisasi.cnt) count_realisasi,
                    sum(propose.cnt) count_propose,
                    sum(rejected_manager.cnt) count_rejected_manager,
                    sum(appeal.cnt) count_appeal,
                    sum(evaluated.cnt) count_evaluated,
                    sum(rejected_bkd.cnt) count_rejected_bkd,
                    sum(done.cnt) count_done,
                    sum(rekap.nilai_akhir) nilai_akhir
                    
            from(  select    emp.id employee_id ,emp.user_id user_id ,
                    emp.nip employee_nip,emp.name employee_name,
                    emp.company_id,emp.job_id, emp.department_id,emp.biro_id
                from res_partner emp
                where employee and user_id notnull ) e
                left join
                            res_company c on c.id = e.company_id
                    left join
                            hr_job j on j.id = e.job_id
                    left join
                            hr_department d on d.id = e.department_id
                    left join hr_employee_biro biro on biro.id = e.biro_id
                    left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'draft'
                    and target_period_month=%s
                    and target_period_year = %s
                   group by user_id,work_state, target_period_month ,target_period_year
                ) draft on draft.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'realisasi'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) realisasi on realisasi.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'propose'
                    and target_period_month=%s
                    and target_period_year = %s
                   group by user_id,work_state, target_period_month ,target_period_year
                ) propose on propose.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'rejected_manager'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) rejected_manager on rejected_manager.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'appeal'
                    and target_period_month=%s
                    and target_period_year = %s
                   group by user_id,work_state, target_period_month ,target_period_year
                ) appeal on appeal.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'evaluated'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) evaluated on evaluated.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'rejected_bkd'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) rejected_bkd on rejected_bkd.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'done'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) done on done.user_id = e.user_id
                left join 
                (select user_id,target_period_month,target_period_year,sum (nilai_akhir) nilai_akhir from skp_employee  
                                where target_period_month=%s
                                and target_period_year = %s
                group by user_id,target_period_month,target_period_year
                )rekap on rekap.user_id = e.user_id and done.cnt > 0
                group by e.employee_id ,e.user_id,e.employee_nip,e.employee_name,j.name, d.name,c.name,biro.name
                order by c.name,biro.name,d.name,e.employee_name
                    """
                domain = period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year
           
        else :
            query = """
           select e.employee_id ,e.user_id,e.employee_nip,e.employee_name,
                j.name jabatan,
                    d.name bidang,
                    c.name company_name ,
                    biro.name biro_name,
                    sum(draft.cnt) count_draft,
                    sum(realisasi.cnt) count_realisasi,
                    sum(propose.cnt) count_propose,
                    sum(rejected_manager.cnt) count_rejected_manager,
                    sum(appeal.cnt) count_appeal,
                    sum(evaluated.cnt) count_evaluated,
                    sum(rejected_bkd.cnt) count_rejected_bkd,
                    sum(done.cnt) count_done,
                    sum(rekap.nilai_akhir) nilai_akhir
                    
            from(  select    emp.id employee_id ,emp.user_id user_id ,
                    emp.nip employee_nip,emp.name employee_name,
                    emp.company_id,emp.job_id, emp.department_id,emp.biro_id
                from res_partner emp
                where employee and user_id notnull ) e
                left join
                            res_company c on c.id = e.company_id
                    left join
                            hr_job j on j.id = e.job_id
                    left join
                            hr_department d on d.id = e.department_id
                    left join hr_employee_biro biro on biro.id = e.biro_id
                    left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'draft'
                    and target_period_month=%s
                    and target_period_year = %s
                   group by user_id,work_state, target_period_month ,target_period_year
                ) draft on draft.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'realisasi'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) realisasi on realisasi.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'propose'
                    and target_period_month=%s
                    and target_period_year = %s
                   group by user_id,work_state, target_period_month ,target_period_year
                ) propose on propose.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'rejected_manager'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) rejected_manager on rejected_manager.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'appeal'
                    and target_period_month=%s
                    and target_period_year = %s
                   group by user_id,work_state, target_period_month ,target_period_year
                ) appeal on appeal.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'evaluated'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) evaluated on evaluated.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'rejected_bkd'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) rejected_bkd on rejected_bkd.user_id = e.user_id
                left join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'done'
                    and target_period_month=%s
                    and target_period_year = %s
                    group by user_id,work_state, target_period_month ,target_period_year
                ) done on done.user_id = e.user_id
                left join 
                (select user_id,target_period_month,target_period_year,sum (nilai_akhir) nilai_akhir from skp_employee  
                                where target_period_month=%s
                                and target_period_year = %s
                group by user_id,target_period_month,target_period_year
                )rekap on rekap.user_id = e.user_id and done.cnt > 0
                where e.company_id = %s
                group by e.employee_id ,e.user_id,e.employee_nip,e.employee_name,j.name, d.name,c.name,biro.name
                order by c.name,biro.name,d.name,e.employee_name
            """
            domain = period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year, period_month, period_year,company_id[0]
        
        employee_results = []
        self.cr.execute(query,domain)
        result = self.cr.fetchall()
        idx=1
        for employee_id,user_id,employee_nip,employee_name,jabatan,bidang,company_name,biro_name,count_draft,count_realisasi,count_propose,count_rejected_manager,count_appeal,count_evaluated,count_rejected_bkd,count_done,nilai_akhir in result:
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
            new_dict['count_realisasi'] = count_realisasi      
            new_dict['count_propose'] = count_propose
            new_dict['count_realisasi'] = count_realisasi      
            new_dict['count_rejected_manager'] = count_rejected_manager
            #new_dict['count_target_new'] = count_target_new  
            new_dict['count_appeal'] = count_appeal
            new_dict['count_evaluated'] = count_evaluated
            new_dict['count_rejected_bkd'] = count_rejected_bkd      
            new_dict['count_done'] = count_done
            new_dict['nilai_akhir'] = nilai_akhir  
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
        period_month=filters['form']['period_month']
        str_period = self.get_period(period_month, period_year)
      
        return prefiks+ " "+str_period
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
            elif month =='04':
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
   
    
