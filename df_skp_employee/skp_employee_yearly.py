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

from openerp.osv import fields, osv
from datetime import datetime,timedelta
import time
from mx import DateTime



class skp_employee_yearly(osv.Model):
    _name = 'skp.employee.yearly'
    def _get_total_perilaku(self, cr, uid, ids, field_names, args, context=None):
        res = {}
        
        for me_obj in self.browse(cr, uid, ids, context=context):
            total = me_obj.nilai_pelayanan+ me_obj.nilai_integritas + me_obj.nilai_komitmen + me_obj.nilai_disiplin +me_obj.nilai_kepemimpinan + me_obj.nilai_kerjasama
            res[me_obj.id] = total   
        return res
    def _get_akumulasi_realiasai_per_bulan(self, cr, user_id, employee_id,target_period_year, context=None):
        
        
        if not employee_id and not target_period_year :
            return False
        uid = user_id.id
        skp_employee_pool = self.pool.get('skp.employee')
        data = {}
        
        skp_employee_ids = skp_employee_pool.search(cr, uid, [('employee_id', '=', employee_id.id),
                                                   ('target_period_year', '=', target_period_year),
                                                   ], context=None)
        count_tambahan_kreatifitas=count=0
        nilai_skp_tambahan_percent=nilai_skp=jml_skp=nilai_skp_percent=jml_perilaku=nilai_perilaku=nilai_perilaku_percent=0
        nilai_pelayanan=nilai_integritas=nilai_komitmen=nilai_disiplin=nilai_kerjasama=nilai_kepemimpinan=0
        fn_nilai_tambahan=fn_nilai_kreatifitas=nilai_total=0
        for skp_obj in  skp_employee_pool.browse(cr, uid, skp_employee_ids, context=context):
            jml_skp+=skp_obj.jml_skp
            nilai_skp+=skp_obj.nilai_skp
            nilai_skp_percent+=skp_obj.nilai_skp_percent
            nilai_skp_tambahan_percent+=skp_obj.nilai_skp_tambahan_percent
            jml_perilaku+=skp_obj.jml_perilaku
            nilai_perilaku+=skp_obj.nilai_perilaku
            nilai_perilaku_percent+=skp_obj.nilai_perilaku_percent
            nilai_pelayanan+=skp_obj.nilai_pelayanan
            nilai_integritas+=skp_obj.nilai_integritas
            nilai_komitmen+=skp_obj.nilai_komitmen
            nilai_disiplin+=skp_obj.nilai_disiplin
            nilai_kerjasama+=skp_obj.nilai_kerjasama
            nilai_kepemimpinan+=skp_obj.nilai_kepemimpinan
            fn_nilai_tambahan+=skp_obj.fn_nilai_tambahan
            fn_nilai_kreatifitas+=skp_obj.fn_nilai_kreatifitas
            nilai_total+=skp_obj.nilai_total
            if fn_nilai_tambahan or fn_nilai_kreatifitas :
                if fn_nilai_tambahan > 0 or fn_nilai_kreatifitas > 0:
                    count_tambahan_kreatifitas+=1
            count+=1
        if target_period_year:
            data['jml_skp']=jml_skp
            data['nilai_skp']=nilai_skp
            data['nilai_skp_percent']=nilai_skp_percent
            data['jml_perilaku']=jml_perilaku
            data['nilai_perilaku']=nilai_perilaku
            data['nilai_perilaku_percent']=nilai_perilaku_percent
            data['nilai_pelayanan']=nilai_pelayanan
            data['nilai_integritas']=nilai_integritas
            data['nilai_komitmen']=nilai_komitmen
            data['nilai_disiplin']=nilai_disiplin
            data['nilai_kerjasama']=nilai_kerjasama
            data['nilai_kepemimpinan']=nilai_kepemimpinan
            if count_tambahan_kreatifitas > 0 :
                data['fn_nilai_tambahan']=fn_nilai_tambahan/count_tambahan_kreatifitas
                data['fn_nilai_kreatifitas']=fn_nilai_kreatifitas/count_tambahan_kreatifitas
          
            data['nilai_total']=nilai_total
            data['count_of_month']=count
        
            
            if jml_skp > 0  and  count>0:
                data['nilai_skp_percent']=nilai_skp_percent/count
                data['nilai_skp_tambahan_percent']=data['nilai_skp_percent']
                data['nilai_skp']=nilai_skp/count
            if count_tambahan_kreatifitas > 0 :
                data['fn_nilai_tambahan']=fn_nilai_tambahan
                data['fn_nilai_kreatifitas']=fn_nilai_kreatifitas
                data['nilai_skp_tambahan_percent']=data['nilai_skp_percent']+data['fn_nilai_tambahan']+data['fn_nilai_kreatifitas'] 
            else :
                data['fn_nilai_tambahan']=0
                data['fn_nilai_kreatifitas']=0
            if jml_perilaku >0 and  count>0:
                data['nilai_perilaku']=nilai_perilaku/count
                data['nilai_perilaku_percent']=nilai_perilaku_percent/count
                data['nilai_pelayanan']=nilai_pelayanan/count
                data['nilai_integritas']=nilai_integritas/count
                data['nilai_komitmen']=nilai_komitmen/count
                data['nilai_disiplin']=nilai_disiplin/count
                data['nilai_kerjasama']=nilai_kerjasama/count
                data['nilai_kepemimpinan']=nilai_kepemimpinan/count
                data['indeks_nilai_pelayanan']=self.get_indeks_nilai(cr, uid, data['nilai_pelayanan'], context)
                data['indeks_nilai_integritas']=self.get_indeks_nilai(cr, uid, data['nilai_integritas'], context)
                data['indeks_nilai_komitmen']=self.get_indeks_nilai(cr, uid, data['nilai_komitmen'], context)
                data['indeks_nilai_disiplin']=self.get_indeks_nilai(cr, uid, data['nilai_disiplin'], context)
                data['indeks_nilai_kerjasama']=self.get_indeks_nilai(cr, uid, data['nilai_kerjasama'], context)
                data['indeks_nilai_kepemimpinan']=self.get_indeks_nilai(cr, uid, data['nilai_kepemimpinan'], context)
            
            if count>0 :
                data['nilai_total']=nilai_total/count
                data['indeks_nilai_total']=self.get_indeks_nilai(cr, uid, data['nilai_total'], context)
                   
        return data
    
        
    _columns = {
        'target_period_year'     : fields.char('Periode Tahun',size=4, required=True),
        'employee_id': fields.many2one('res.partner', 'Pegawai Yang Dinilai', readonly=True),
        'user_id': fields.many2one('res.users','User Login', readonly=True ),
        
        'company_id': fields.many2one('res.company', 'SKPD', readonly=True),
        'biro_id': fields.many2one('partner.employee.biro', 'Bagian / Bidang',readonly=True ),
        'department_id': fields.many2one('hr.department', 'Unit Kerja',readonly=True),
        'golongan_id': fields.many2one('hr.employee.golongan', 'Golongan',readonly=True), 
        'job_id': fields.many2one('hr.job', 'Jabatan',readonly=True),
        'jml_skp': fields.integer(string='Jumlah SKP',  help="Jumlah SKP",readonly = True),
        'count_of_month': fields.integer(string='Jumlah Realisasi Bulan',  help="Jumlah BUlan ",readonly = True),
        'jml_perilaku': fields.integer( string='Jumlah Perilaku',  help="Jumlah SKP",readonly = True),
        'nilai_skp': fields.float( string='Nilai SKP',  help="Nilai SKP Akan Muncul Apabila Semua Kegiatan Dibulan Tertentu Sudah Selesai Dinilai", readonly = True),
        'nilai_skp_percent': fields.float( string='Nilai SKP(%)',  help="60% Dari Kegiatan DPA Biro, APBN, SOTK", readonly = True),
        'nilai_skp_tambahan_percent': fields.float( string='Nilai SKP(%)+TB+Kreatifitas',  help="60% Dari Kegiatan DPA Biro, APBN, SOTK Ditambah rata2 Tugas Tambahan Dan Nilai Kreatifitas", readonly = True),
        'nilai_perilaku': fields.float( string='Nilai Perilaku', help="40% Kontribusi untuk nilai perilaku", readonly = True),
        'nilai_perilaku_percent': fields.float(string='Nilai Perilaku(%)', type='', help="40% Kontribusi untuk nilai perilaku",readonly = True),
        'fn_nilai_tambahan': fields.float( string='Nilai Tambahan',  help="Nilai Tambahan", readonly = True),
        'fn_nilai_kreatifitas': fields.float( string='Nilai Kreatifitas',help="Nilai Kreatifitas",readonly = True),
        'nilai_total': fields.float(string='Nilai Total (%)',  help="60% SKP + maks 2, Nilai Tambahan + 40% perilaku", readonly = True),
        'indeks_nilai_total': fields.char('Indeks Nilai Total',  size=25,readonly=True),
        'nilai_tpp': fields.float( string='TPP', help="TPP", readonly = True),
        'nilai_kepemimpinan': fields.float('Nilai Kepemimpinan', readonly=True),
        'nilai_kerjasama': fields.float('Nilai Kerjasama', readonly=True),
        'nilai_integritas': fields.float('Nilai Integritas', readonly=True),
        'nilai_komitmen': fields.float('Nilai Komitmen', readonly=True),
        'nilai_disiplin': fields.float('Nilai Disiplin', readonly=True),
        'nilai_pelayanan': fields.float('Nilai Pelayanan', readonly=True),
        'indeks_nilai_kepemimpinan': fields.char('Indeks Nilai Kepemimpinan', size=25,readonly=True),
        'indeks_nilai_kerjasama': fields.char('Indeks Nilai Kerjasama',  size=25,readonly=True),
        'indeks_nilai_integritas': fields.char('Indeks Nilai Integritas',  size=25,readonly=True),
        'indeks_nilai_komitmen': fields.char('Indeks Nilai Komitmen',  size=25,readonly=True),
        'indeks_nilai_disiplin': fields.char('Indeks Nilai Disiplin',  size=25,readonly=True),
        'indeks_nilai_pelayanan': fields.char('Indeks Nilai Pelayanan',  size=25,readonly=True),
        'total_perilaku': fields.function(_get_total_perilaku, string='Penambahan Semua Aspek Perilaku', type='integer',
            store = False),
   }
    def get_indeks_nilai(self,cr,uid,nilai,context=None):
        ret_val=''
        lookup_nilai_pool = self.pool.get('acuan.penailaian')
        lookup_nilai_id = lookup_nilai_pool.search(cr, uid, [('kategori_nilai', '=', 'threshold'), ('active', '=', True), ('type', '=', 'lain_lain')
                                                            , ('code', 'in', ('index_nilai_a','index_nilai_b','index_nilai_c','index_nilai_d','index_nilai_e'))
                                                            ,('nilai_bawah', '<=', nilai), ('nilai_atas', '>=', nilai)], context=None)
        if lookup_nilai_id :
            lookup_nilai_obj = lookup_nilai_pool.browse(cr, uid, lookup_nilai_id, context=None)[0]
            ret_val = lookup_nilai_obj.name
        
        return ret_val
skp_employee_yearly()




