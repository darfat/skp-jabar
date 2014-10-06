import pooler
import time
from datetime import datetime
import tools
import logging
from report import report_sxw
from datetime import datetime
from report_webkit import webkit_report

class skp_monthly_recapitulation_report_parser(report_sxw.rml_parse):

    def __init__(self, cr, uid, name, context=None):
        super(skp_monthly_recapitulation_report_parser, self).__init__(cr, uid, name, context=context)

    def get_skp_monthly_recapitulation_report_raw(self,filters,context=None):
        period_year=filters['form']['period_year']
        period_month=filters['form']['period_month']
        company_id=filters['form']['company_id']
        biro_id=filters['form']['biro_id']
        kepala_opd=filters['form']['is_kepala_opd']
        where_clause=" where employee and e.user_id notnull "
        if kepala_opd:
            where_clause = where_clause + " and c.head_of_comp_employee_id = e.id "
        else :
            if company_id:
		if company_id[0] != 1 :
	                where_clause = where_clause + " and e.company_id =  "+str(company_id[0])
            if biro_id:
                where_clause = where_clause + " and biro.id =  "+str(biro_id[0])
        
           
        query = """
        select e.id employee_id ,e.nip employee_nip,e.name employee_name,
           c.name company_name ,
           biro.name biro_name,
           skp.id skp_id,
           es.name eselon ,e.job_type tipe_jabatan ,gol.name golongan,
           dept.name bidang,
           job.name jabatan,
           sum(draft.cnt) count_draft,
           sum(realisasi.cnt) count_realisasi,
           sum(done.cnt) count_done,
           sum(realisasi_all.cnt) count_realisasi_all,
            e.user_id
            from res_partner e
            left  join
            res_company c on c.id = e.company_id
            left  join
            hr_employee_biro biro on biro.id = e.biro_id
            left  join
            hr_employee_eselon es on es.id = e.eselon_id
            left  join
            hr_employee_golongan gol on gol.id = e.golongan_id
            left  join
            hr_department dept on dept.id = e.department_id
            left  join
            hr_job job on job.id = e.job_id
            left  join
            skp_employee skp on skp.user_id = e.user_id
                                and skp.target_period_month=%s
                                and skp.target_period_year =%s
            left  join
            (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'draft'
                    and target_period_month=%s
                    and target_period_year = %s
                    and task_category='skp'
                    and project_id notnull
                   group by user_id,work_state, target_period_month ,target_period_year
                ) draft on draft.user_id = e.user_id
            left  join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state = 'realisasi'
                    and target_period_month=%s
                    and target_period_year = %s
                    and task_category='skp'
                    and project_id notnull
                    group by user_id,work_state, target_period_month ,target_period_year
                ) realisasi on realisasi.user_id = e.user_id
             left  join
            (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                  where work_state = 'done'
                    and target_period_month=%s
                    and target_period_year = %s
                    and task_category='skp'
                    and project_id notnull
                   group by user_id,work_state, target_period_month ,target_period_year
                ) done on done.user_id = e.user_id
            left  join 
                (select count(id) cnt,user_id,work_state, target_period_month ,target_period_year from project_task
                    where work_state <> 'cancelled'  
                    and target_period_month=%s
                    and target_period_year = %s
                    and task_category='skp'
                    and project_id notnull
                    group by user_id,work_state, target_period_month ,target_period_year
                ) realisasi_all on realisasi_all.user_id = e.user_id
        """+where_clause+""" 
        group by e.id ,e.nip ,e.name ,
                   c.name  ,
                   biro.name,
                   skp.id ,
                   es.name  ,e.job_type  ,gol.name ,
                   dept.name ,
                   job.name ,
                   e.user_id
            order by c.name,biro.name,dept.name,e.name,skp.id
        """
        employee_results = []
        
        domain = period_month, period_year,period_month, period_year,period_month, period_year,period_month, period_year,period_month, period_year
        self.cr.execute(query,domain)
        result = self.cr.fetchall()
        no_idx=1;
        for employee_id,employee_nip,employee_name,company_name,biro_name,skp_id,eselon,tipe_jabatan,golongan,bidang,jabatan,count_draft, count_realisasi, count_done,count_realisasi_all,user_id in result:
            new_dict = {}
            new_dict['no_idx'] = no_idx
            new_dict['employee_nip'] = employee_nip
            new_dict['employee_name'] = employee_name
            new_dict['company_name'] = company_name
            new_dict['biro_name'] = biro_name
            new_dict['skp_id'] = str(skp_id)
            new_dict['skp_obj'] = self.get_skp_obj(skp_id)
            new_dict['eselon'] = eselon
            new_dict['tipe_jabatan'] = tipe_jabatan
            new_dict['golongan'] = golongan
            new_dict['bidang'] = bidang
            new_dict['jabatan'] = jabatan
            new_dict['count_draft'] = count_draft
            new_dict['count_realisasi'] = count_realisasi
            new_dict['count_done'] = count_done
            new_dict['count_realisasi_all'] = count_realisasi_all
            
            
            
            new_dict['user_id'] = 'Belum Aktifasi' 
            if user_id : new_dict['user_id'] = 'Sudah Aktifasi'       
            
            employee_results.append(new_dict)
            no_idx+=1
    
        return employee_results;
    def get_skp_obj(self,skp_id):
        if skp_id:
             skp_pool = self.pool.get('skp.employee')
             skp_results = skp_pool.browse(self.cr,self.uid,[skp_id])
             skp_obj = skp_results[0]
             return skp_obj
            
        return None;
    def get_nilai_skp_percent(self,skp_obj):
        
        if not skp_obj :
            return 0
        return skp_obj.nilai_skp_percent
    def get_nilai_perilaku_percent(self,skp_obj):
        
        if not skp_obj :
            return 0
        return skp_obj.nilai_perilaku_percent
    def get_jml_skp(self,skp_obj):
        if not skp_obj :
            return 0
        return skp_obj.jml_skp
    def get_jml_all_skp(self,skp_obj):
        if not skp_obj :
            return 0
        return skp_obj.jml_all_skp
    def get_status_skp(self,skp_obj):
        if not skp_obj :
            return '-'
        return skp_obj.skp_state_count
    def get_jml_perilaku(self,skp_obj):
        
        if not skp_obj :
            return 0
        return skp_obj.jml_perilaku
    def get_nilai_tambahan(self,skp_obj):
        
        if not skp_obj :
            return 0
        return skp_obj.fn_nilai_tambahan
    def get_nilai_kreatifitas(self,skp_obj):
        
        if not skp_obj :
            return 0
        return skp_obj.fn_nilai_kreatifitas
    def get_nilai_total(self,skp_obj):
        if not skp_obj :
            return 0
        return skp_obj.nilai_total
    
    def get_kategori_penilaian_old(self,skp_obj,o):
        if not o:
            return '~'
        
        if not o['count_realisasi_all'] or o['count_realisasi_all'] == 0 :
            return 'Tidak Buat Target'
        draft_skp=( (o['count_draft'] or 0) + (o['count_realisasi'] or 0) )
        done_skp = o['count_done'] or 0
        all_skp=o['count_realisasi_all'] or 0
        if draft_skp == all_skp:
            return 'Tidak Ajukan Realisasi SKP'
        if done_skp>0 and done_skp < all_skp :
            return 'SKP Selesai Sebagian'
        if done_skp==0 and draft_skp == 0 and all_skp!=0 :
            return 'SKP Dalam Penilaian'
        if done_skp == all_skp:
            return 'SKP Selesai'
        return 'Lain-Lain'
    def get_nilai_toleransi_old(self,skp_obj,o):
        kategori = self.get_kategori_penilaian(skp_obj,o)
        perilaku=0
        tt=0
        kreatif=0
        if skp_obj:
            perilaku = self.get_nilai_perilaku_percent(skp_obj)
            tt =  self.get_nilai_tambahan(skp_obj)
            kreatif =  self.get_nilai_kreatifitas(skp_obj)
        if kategori == 'Tidak Buat Target' :
            toleransi =0
            return toleransi + perilaku + tt+ kreatif
        if kategori == 'Tidak Ajukan Realisasi SKP' :
            if not skp_obj:
                return 70
            else :
                return  perilaku + tt+ kreatif
        if kategori == 'SKP Selesai Sebagian' :
	    toleransi=self.get_nilai_skp_percent(skp_obj)
            return self.get_nilai_total(skp_obj)
        if kategori == 'SKP Dalam Penilaian' :
            toleransi=0
            if not skp_obj :
                tolerasi = 70 + perilaku + tt+ kreatif
            else :
                toleransi = self.get_nilai_total(skp_obj)
            return toleransi
        if kategori == 'SKP Selesai' :
            return self.get_nilai_total(skp_obj)
        if kategori == 'Lain-Lain' and skp_obj:
            return self.get_nilai_total(skp_obj)
     
        return self.get_nilai_total(skp_obj)
    def get_kategori_penilaian(self,skp_obj,o):
        if not o:
            return '~'
        
        if not o['count_realisasi_all'] or o['count_realisasi_all'] == 0 :
            return 'Tidak Buat Target'
        draft_skp=( (o['count_draft'] or 0) + (o['count_realisasi'] or 0) )
        done_skp = o['count_done'] or 0
        all_skp=o['count_realisasi_all'] or 0
        if draft_skp == all_skp:
            return 'Tidak Ajukan Realisasi SKP'
        if done_skp>0 and done_skp < all_skp :
            return 'SKP Selesai Sebagian'
        if done_skp==0 and draft_skp == 0 and all_skp!=0 :
            return 'SKP Dalam Penilaian'
        if done_skp == all_skp:
            return 'SKP Selesai'
        return 'Lain-Lain'
    def get_nilai_toleransi(self,skp_obj,o):
        kategori = self.get_kategori_penilaian(skp_obj,o)
        perilaku=0
        tt=0
        kreatif=0
        if skp_obj:
            perilaku = self.get_nilai_perilaku_percent(skp_obj)
            tt =  self.get_nilai_tambahan(skp_obj)
            kreatif =  self.get_nilai_kreatifitas(skp_obj)
        if kategori == 'Tidak Buat Target' :
            toleransi =0
            return toleransi + perilaku + tt+ kreatif
        if kategori == 'Tidak Ajukan Realisasi SKP' :
            if not skp_obj:
                return 0
            else :
                if perilaku > 0 :
                    perilaku = (perilaku *80)/100
                return perilaku+tt+kreatif
        if kategori == 'SKP Selesai Sebagian' :
            toleransi=self.get_nilai_skp_percent(skp_obj)
            if perilaku > 0 :
                    perilaku = (perilaku *80)/100
                    toleransi= perilaku+tt+kreatif + toleransi

            return toleransi
        if kategori == 'SKP Dalam Penilaian' :
            toleransi=0
            if not skp_obj :
                tolerasi = 0
            else :
                toleransi=self.get_nilai_skp_percent(skp_obj)
            if perilaku > 0 :
                    perilaku = (perilaku *80)/100
                    toleransi= perilaku+tt+kreatif + toleransi

            return toleransi
        if kategori == 'SKP Selesai' :
            return self.get_nilai_total(skp_obj)
        if kategori == 'Lain-Lain' and skp_obj:
            toleransi=self.get_nilai_skp_percent(skp_obj)
            if perilaku > 0 :
                    perilaku = (perilaku *80)/100
                    toleransi= perilaku+tt+kreatif + toleransi

            return toleransi

     
        return self.get_nilai_total(skp_obj)

    def get_realisasi_skp_by_status(self,user_id,work_state,filters):
        period_year=filters['form']['period_year']
        period_month=filters['form']['period_month']
        company_id=filters['form']['company_id']
        task_pool = self.pool.get('project.task')
        task_ids = task_pool.search(self.cr,self.uid,[('target_period_month','=',period_month),('target_period_year','=',period_year),
                                                     ('user_id','=',user_id),('work_state','=',work_state), ]);
        cnt = len(task_ids)
       
        return cnt
  
    def get_target_skp_by_status(self,user_id,state,filters):
        period_year=filters['form']['period_year']
        period_month=filters['form']['period_month']
        company_id=filters['form']['company_id']
        target_pool = self.pool.get('project.project')
        target_ids = target_pool.search(self.cr,self.uid,[('target_period_month','=',period_month),('target_period_year','=',period_year),
                                                     ('user_id','=',user_id),('state','=',state), ]);
        cnt = len(target_ids)
       
        return cnt
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
   #april
    def get_kategori_penilaian_april(self,skp_obj):
        if not skp_obj :
            return 'Tidak Lengkap'
        if skp_obj.jml_skp > 0 and skp_obj.nilai_perilaku > 0 :
            return 'Lengkap'
        if skp_obj.jml_skp > 0 and skp_obj.nilai_perilaku <= 0  :
            return 'Ada SKP | Tidak Ada Perilaku'
        if skp_obj.jml_skp <= 0 and skp_obj.jml_perilaku > 0 :
            return 'Tidak Ada SKP | Ada Perilaku'
        return 'Tidak Lengkap'
    def get_nilai_toleransi_april(self,skp_obj):
        kategori = self.get_kategori_penilaian(skp_obj)
        if kategori == 'Tidak Lengkap' :
            return 70
        else :
            return 100;
