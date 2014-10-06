import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class employee_data_summary_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(employee_data_summary_report_parser, self).__init__(cr, uid, name, context=context)

    def get_employee_data_summary_report_raw(self,filters,context=None):

        
        #employee_pool = self.pool.get('hr.employee')
        #employee_ids =[1]
        #results = employee_pool.browse(self.cr, self.uid, employee_ids)
        query = """
        select e.id employee_id ,e.nip employee_nip,e.name_related employee_name,
           c.name company_name ,
           es.name eselon ,e.job_type tipe_jabatan ,gol.name golongan,
           dept.name bidang,
           job.name jabatan,
           br.name biro_name,
           atasan.nip nip_atasan, atasan.name_related nama_atasan,
           banding.nip nip_banding, banding.name_related nama_banding,
           sch.name nama_sekolah,std.name jurusan,
           e.diklat_kepemimpinan,diklat_fungsional,
           tempat_lahir,tanggal_lahir,agama,
           r.user_id
            from hr_employee e
            left  join
            resource_resource r on e.resource_id = r.id
            left  join
            (select ep.id,ep.nip,ep.name_related      
            from hr_employee  ep 
            ) atasan
        on atasan.id = e.parent_id
        left  join
            (select ep.id,ep.nip,ep.name_related      
            from hr_employee  ep 
            ) banding
        on banding.id = e.user_id_banding
            left  join
            res_company c on c.id = r.company_id
            left  join
            hr_employee_eselon es on es.id = e.eselon_id
            left  join
            hr_employee_golongan gol on gol.id = e.golongan_id
            left  join
            hr_department dept on dept.id = e.department_id
            left  join
            hr_job job on job.id = e.job_id
            left  join
            hr_employee_school sch on sch.id = e.nama_sekolah
            left  join
            hr_employee_study std on std.id = e.jurusan
            left join
            hr_employee_biro br on br.id = e.biro_id
            order by c.name,dept.name,e.name_related
        """
        employee_results = []
        
        #domain = date_from, date_to, date_from, post_all_state, post_state, date_from, date_to, post_all_state, post_state, date_from, date_from, date_to, date_from, date_from, date_to, post_all_state, post_state, date_from, post_all_state, post_state
        self.cr.execute(query)
        result = self.cr.fetchall()
        no_idx=1;
        for employee_id,employee_nip,employee_name,company_name,eselon,tipe_jabatan,golongan,bidang,jabatan,biro_name,nip_atasan,nama_atasan,nip_banding,nama_banding,nama_sekolah,jurusan,diklat_kepemimpinan,diklat_fungsional,tempat_lahir,tanggal_lahir,agama , user_id in result:
            new_dict = {}
            new_dict['no_idx'] = employee_id
            new_dict['employee_nip'] = employee_nip
            new_dict['employee_name'] = employee_name
            new_dict['company_name'] = company_name
            new_dict['eselon'] = eselon
            new_dict['biro_name'] = biro_name
            new_dict['tipe_jabatan'] = tipe_jabatan
            new_dict['golongan'] = golongan
            new_dict['bidang'] = bidang
            new_dict['jabatan'] = jabatan
            new_dict['nip_atasan'] = nip_atasan
            new_dict['nama_atasan'] = nama_atasan
            new_dict['nip_banding'] = nip_banding
            new_dict['nama_banding'] = nama_banding
            new_dict['nama_sekolah'] = nama_sekolah
            new_dict['jurusan'] = jurusan
            new_dict['diklat_kepemimpinan'] = diklat_kepemimpinan
            new_dict['diklat_fungsional'] = diklat_fungsional
            new_dict['tempat_lahir'] = tempat_lahir
            new_dict['tanggal_lahir'] = tanggal_lahir
            new_dict['agama'] = agama
            new_dict['user_id'] = 'Belum Aktifasi' 
            if user_id : new_dict['user_id'] = 'Sudah Aktifasi'       
            
            employee_results.append(new_dict)
            no_idx+=1
    
        return employee_results;
    def get_title(self,prefiks,filters):
        
      
        return ''
   
    
