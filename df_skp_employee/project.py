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

from osv import fields, osv
from datetime import datetime,timedelta
import time
from mx import DateTime


class project(osv.osv):
    _inherit = 'project.project'
    def _get_target_total_kuantitas_output_tahunan(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        for _target in self.browse(cr, uid, ids, context=context):
            total = 0.0
            count =0.0
            if _target.target_jumlah_kuantitas_output >0 :
                if _target.realisasi_lines:
                    for task_obj in _target.realisasi_lines:
                        if task_obj.work_state == 'done':
                            total+= task_obj.target_jumlah_kuantitas_output
                            count+=1
                    if count >1 :
                        total = total/count;
            res[_target.id]=total
        return res
    def _get_realisasi_total_kuantitas_output_tahunan(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        for _target in self.browse(cr, uid, ids, context=context):
            total = 0.0
            count =0.0
            if _target.target_jumlah_kuantitas_output >0 :
                if _target.realisasi_lines:
                    for task_obj in _target.realisasi_lines:
                        if task_obj.work_state == 'done':
                            total+= task_obj.realisasi_jumlah_kuantitas_output
                            count+=1
                    if count >1 :
                        total = total/count
            res[_target.id]=total
        return res
    
    def _get_target_total_biaya_tahunan(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        for _target in self.browse(cr, uid, ids, context=context):
            total = 0.0
            count =0.0
            if _target.target_biaya >0 :
                if _target.realisasi_lines:
                    for task_obj in _target.realisasi_lines:
                        if task_obj.work_state == 'done':
                            total+= task_obj.target_biaya
                            count+=1
                    if count >1 :
                        total = total/count;
            res[_target.id]=total
        return res
    def _get_realisasi_total_biaya_tahunan(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if not ids:
            return res
        for _target in self.browse(cr, uid, ids, context=context):
            total = 0.0
            count =0.0
            if _target.target_biaya >0 :
                if _target.realisasi_lines:
                    for task_obj in _target.realisasi_lines:
                        if task_obj.work_state == 'done':
                            total+= task_obj.realisasi_biaya
                            count+=1
                    if count >1 :
                        total = total/count
            res[_target.id]=total
        return res
    
    def _get_akumulasi_target_realisasi_tahunan(self, cr, uid, _target, context=None):
        data = {}
        total_target_biaya=total_target_waktu=total_target_kualitas=total_target_jumlah_kuantitas_output=total_target_angka_kredit=0
        total_realisasi_biaya=total_realisasi_waktu=total_realisasi_kualitas=total_realisasi_jumlah_kuantitas_output=total_realisasi_angka_kredit=0
        count_biaya=count_waktu=count_kualitas=count_kuantitas=count_angka_kredit=0
        count_all=count=total_nilai_target_skp=total_capaian_target_skp=0
        if _target:
            if _target.realisasi_lines:
                for task_obj in _target.realisasi_lines:
                    if task_obj.work_state and task_obj.work_state != 'cancelled' :
                        total_target_biaya+= task_obj.target_biaya
                        total_target_waktu+= task_obj.target_waktu
                        total_target_kualitas+= task_obj.target_kualitas
                        total_target_jumlah_kuantitas_output+= task_obj.target_jumlah_kuantitas_output
                        total_target_angka_kredit+= task_obj.target_angka_kredit
                        count_all+=1
                    if task_obj.work_state and task_obj.work_state == 'done':
                        total_realisasi_biaya+= task_obj.realisasi_biaya
                        total_realisasi_waktu+= task_obj.realisasi_waktu
                        total_realisasi_kualitas+= task_obj.realisasi_kualitas
                        total_realisasi_jumlah_kuantitas_output+= task_obj.realisasi_jumlah_kuantitas_output
                        total_realisasi_angka_kredit+= task_obj.realisasi_angka_kredit
                        
                        count+=1
                        total_nilai_target_skp += task_obj.nilai_akhir
                        #calculate
                        
                        
                        
            
            if count_all > 0:
                total_capaian_target_skp=total_nilai_target_skp/count_all
            data['total_target_biaya']=total_target_biaya
            data['total_target_waktu']=total_target_waktu
            data['total_target_kualitas']=total_target_kualitas
            data['total_target_jumlah_kuantitas_output']=total_target_jumlah_kuantitas_output
            data['total_target_angka_kredit']=total_target_angka_kredit
            data['total_realisasi_biaya']=total_realisasi_biaya
            data['total_realisasi_waktu']=total_realisasi_waktu
            data['total_realisasi_kualitas']=total_realisasi_kualitas
            data['total_realisasi_jumlah_kuantitas_output']=total_realisasi_jumlah_kuantitas_output
            data['total_realisasi_angka_kredit']=total_realisasi_angka_kredit
            data['total_nilai_target_skp']=total_nilai_target_skp
            data['total_capaian_target_skp']=total_capaian_target_skp
            data['count_biaya']=count_biaya
            data['count_waktu']=count_waktu
            data['count_kualitas']=count_kualitas
            data['count_kuantitas']=count_kuantitas
            data['count_angka_kredit']=count_angka_kredit
            data['count_of_done']=count
        return data
    _columns = {
        'total_target_jumlah_kuantitas_output'     : fields.float('Total Target Kuantitas Output', readonly=True, ),
        'total_target_angka_kredit'     : fields.float('Total Target Angka Kredit', readonly=True,  ), #digits_compute=dp.get_precision('angka_kredit')
        'total_target_kualitas'     : fields.float('Total Target  Kualitas', readonly=True, ), # digits_compute=dp.get_precision('no_digit'),
        'total_target_waktu'     : fields.float('Total Target Waktu', readonly=True, ),
        'total_target_biaya'     : fields.float('Total Target Biaya', readonly=True,),  
        
        'total_realisasi_jumlah_kuantitas_output'     : fields.float('Total Realisasi Kuantitas Output', readonly=True, ),
        'total_realisasi_angka_kredit'     : fields.float('Total Realisasi Angka Kredit', readonly=True,  ), #digits_compute=dp.get_precision('angka_kredit')
        'total_realisasi_kualitas'     : fields.float('Total Realisasi  Kualitas', readonly=True, ), # digits_compute=dp.get_precision('no_digit'),
        'total_realisasi_waktu'     : fields.float('Total Realisasi Waktu', readonly=True, ),
        'total_realisasi_biaya'     : fields.float('Total Realisasi Biaya', readonly=True,),   
        'count_of_done'     : fields.integer('Jumlah Realisasi Yang Sudah Dinilai', readonly=True,),     
         'total_nilai_target_skp'     : fields.float('Jumlah Perhitungan', readonly=True,),     
         'total_capaian_target_skp'     : fields.float('Nilai Capaian SKP', readonly=True,),
    }
project()