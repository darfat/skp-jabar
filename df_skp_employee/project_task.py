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


class project_task(osv.osv):
    _inherit = 'project.task'
    def action_work_done(self, cr, uid, ids, context=None):
        if not isinstance(ids, list): ids = [ids]
        super(project_task, self).action_work_done(cr, uid, ids, context=context)   
        self.do_yearly_summary_calculation(cr, uid, ids, context)     
        #self.action_task_summary_calculation(cr,uid,ids,context)
        return True
    
    def do_recalculate_poin(self, cr, uid, ids, context=None):
         if not isinstance(ids, list): ids = [ids]
         super(project_task, self).do_recalculate_poin(cr, uid, ids, context=context)   
         self.do_yearly_summary_calculation(cr, uid, ids, context) 
         #self.action_task_summary_calculation(cr,uid,ids,context)
         return True;
    def action_work_done_use_target(self, cr, uid, ids, context=None):
         if not isinstance(ids, list): ids = [ids]
         super(project_task, self).action_work_done_use_target(cr, uid, ids, context=context)   
         self.do_yearly_summary_calculation(cr, uid, ids, context) 
         #self.action_task_summary_calculation(cr,uid,ids,context)
         return True;
    def action_task_summary_calculation(self, cr, uid, ids,  context=None):
        """ BKD->Done (Rekap Summary) """
        # Summary Calculation
        
        target_pool = self.pool.get('project.project')
        skp_employee_pool = self.pool.get('skp.employee')
        if not isinstance(ids, list): ids = [ids]
        for task_obj in self.browse(cr, uid, ids, context=context):
                skp_employee_ids = skp_employee_pool.search(cr, uid, [('employee_id', '=', task_obj.employee_id.id),
                                                   ('target_period_year', '=', task_obj.target_period_year),
                                                   ('target_period_month', '=', task_obj.target_period_month),
                                                   ], context=None)
                if not skp_employee_ids:
                        values = {
                            'employee_id': task_obj.employee_id.id,
                            'user_id': task_obj.user_id.id,
                            'target_period_year': task_obj.target_period_year,
                            'target_period_month':task_obj.target_period_month,
                        }
                        skp_employee_pool.create(cr , uid, values, context=None)
                else :
                    for skp_employee_obj in  skp_employee_pool.browse(cr, uid, skp_employee_ids, context=context):
                        skp_state_count = skp_employee_obj.skp_state_count;
                        jml_skp = skp_employee_obj.jml_skp;
                        jml_all_skp = skp_employee_obj.jml_all_skp;
                        jml_perilaku = skp_employee_obj.jml_perilaku;
                        nilai_skp = skp_employee_obj.nilai_skp;
                        nilai_skp_percent = skp_employee_obj.nilai_skp_percent;
                        nilai_perilaku = skp_employee_obj.nilai_perilaku;
                        nilai_perilaku_percent = skp_employee_obj.nilai_perilaku_percent;
                        fn_nilai_tambahan = skp_employee_obj.fn_nilai_tambahan;
                        fn_nilai_kreatifitas = skp_employee_obj.fn_nilai_kreatifitas;
                        nilai_total = skp_employee_obj.nilai_total;
                        nilai_tpp = skp_employee_obj.nilai_tpp;
                        nilai_pelayanan,nilai_disiplin,nilai_komitmen,nilai_integritas,nilai_kerjasama,nilai_kepemimpinan = skp_employee_pool.get_detail_nilai_perilaku(cr,uid,task_obj.user_id.id,task_obj.target_period_month,task_obj.target_period_year,'done',context)
                        
                        update_values = {
                            'skp_state_count': skp_state_count,
                            'jml_skp': jml_skp,
                            'jml_all_skp': jml_all_skp,
                            'jml_perilaku': jml_perilaku,
                            'nilai_skp': nilai_skp,
                            'nilai_skp_percent': nilai_skp_percent,
                            
                            'nilai_perilaku': nilai_perilaku,
                            'nilai_perilaku_percent': nilai_perilaku_percent,
                            'fn_nilai_tambahan': fn_nilai_tambahan,
                            'fn_nilai_kreatifitas': fn_nilai_kreatifitas,
                            
                             'nilai_pelayanan': nilai_pelayanan,
                             'nilai_integritas': nilai_integritas,
                             'nilai_komitmen':nilai_komitmen,
                             'nilai_disiplin': nilai_disiplin,
                             'nilai_kerjasama': nilai_kerjasama,
                             'nilai_kepemimpinan':nilai_kepemimpinan,
                             
                            'nilai_total': nilai_total,
                            
                            'nilai_tpp': nilai_tpp,
                        }
                        skp_employee_pool.write(cr , uid,[skp_employee_obj.id,], update_values, context=None)
                
        return True;
    def do_yearly_summary_calculation(self, cr, uid, ids,  context=None):
        
        if not isinstance(ids, list): ids = [ids]
        
        for task_obj in self.browse(cr, uid, ids, context=context):
                #kalkulasi akumulasi skp tahunan
                if task_obj.task_category=='skp':
                    self.do_target_summary_calculation(cr, uid, task_obj.project_id, context)
                self.do_skp_summary_calculation(cr,uid,task_obj.user_id,task_obj.employee_id,task_obj.target_period_year)
                    
        return True;
    def do_target_summary_calculation(self, cr, uid, target_obj,  context=None):
        
        target_pool = self.pool.get('project.project')
        if target_obj:
            data_target  = target_pool._get_akumulasi_target_realisasi_tahunan(cr, uid, target_obj, context=context)
            if data_target:
                        update_values = {
                            'total_target_jumlah_kuantitas_output': data_target['total_target_jumlah_kuantitas_output'],
                            'total_target_angka_kredit': data_target['total_target_angka_kredit'],
                            'total_target_kualitas': data_target['total_target_kualitas'],
                            'total_target_waktu': data_target['total_target_waktu'],
                            'total_target_biaya': data_target['total_target_biaya'],
                            'total_realisasi_jumlah_kuantitas_output': data_target['total_realisasi_jumlah_kuantitas_output'],
                            'total_realisasi_angka_kredit': data_target['total_realisasi_angka_kredit'],
                            'total_realisasi_kualitas': data_target['total_realisasi_kualitas'],
                            'total_realisasi_waktu': data_target['total_realisasi_waktu'],
                            'total_realisasi_biaya': data_target['total_realisasi_biaya'],
                            'total_realisasi_biaya': data_target['total_realisasi_biaya'],
                            'total_nilai_target_skp': data_target['total_nilai_target_skp'],
                            'total_capaian_target_skp': data_target['total_capaian_target_skp'],
                            'count_of_done': data_target['count_of_done'],
                        }
                        target_pool.write(cr , uid,[target_obj.id,], update_values, context=None)
        return True;
    def do_skp_summary_calculation(self, cr,uid, user_id,employee_id, target_period_year,  context=None):
        
        sey_pool = self.pool.get('skp.employee.yearly')
        data_skp_summary  = sey_pool._get_akumulasi_realiasai_per_bulan(cr, user_id,employee_id, target_period_year, context=context)
        skp_yearly_ids = sey_pool.search(cr, uid, [('employee_id', '=', employee_id.id),
                                                     ('target_period_year', '=', target_period_year),
                                                   ], context=None)
        if not skp_yearly_ids:
                        values = {
                            'employee_id': employee_id.id,
                            'user_id': user_id.id,
                            'target_period_year': target_period_year,
                        }
                        new_skp_yearly_id=sey_pool.create(cr , uid, values, context=None)
                        skp_yearly_ids.append(new_skp_yearly_id)
                        
        if data_skp_summary and skp_yearly_ids :
            for skp_yearly_obj in  sey_pool.browse(cr, uid, skp_yearly_ids, context=context):
                        count_of_month = data_skp_summary['count_of_month']
                        if count_of_month > 0 :
                            update_values = {
                                'jml_skp': data_skp_summary['jml_skp'],
                                'nilai_skp': data_skp_summary['nilai_skp']   ,
                                'nilai_skp_percent': data_skp_summary['nilai_skp_percent'],
                                'nilai_skp_tambahan_percent': data_skp_summary['nilai_skp_tambahan_percent'],
                                'jml_perilaku': data_skp_summary['jml_perilaku'],
                                'nilai_perilaku': data_skp_summary['nilai_perilaku'],
                                'nilai_perilaku_percent': data_skp_summary['nilai_perilaku_percent'],
                                'nilai_pelayanan': data_skp_summary['nilai_pelayanan'],
                                'nilai_integritas': data_skp_summary['nilai_integritas'],
                                'nilai_komitmen': data_skp_summary['nilai_komitmen'],
                                'nilai_disiplin': data_skp_summary['nilai_disiplin'],
                                'nilai_kerjasama': data_skp_summary['nilai_kerjasama'],
                                'nilai_kepemimpinan': data_skp_summary['nilai_kepemimpinan'],
                                'fn_nilai_tambahan': data_skp_summary['fn_nilai_tambahan'],
                                'fn_nilai_kreatifitas': data_skp_summary['fn_nilai_kreatifitas'],
                                'nilai_total': data_skp_summary['nilai_total'],
                                'indeks_nilai_pelayanan': data_skp_summary['indeks_nilai_pelayanan'],
                                'indeks_nilai_integritas': data_skp_summary['indeks_nilai_integritas'],
                                'indeks_nilai_komitmen': data_skp_summary['indeks_nilai_komitmen'],
                                'indeks_nilai_disiplin': data_skp_summary['indeks_nilai_disiplin'],
                                'indeks_nilai_kerjasama': data_skp_summary['indeks_nilai_kerjasama'],
                                'indeks_nilai_kepemimpinan': data_skp_summary['indeks_nilai_kepemimpinan'],
                                'indeks_nilai_total': data_skp_summary['indeks_nilai_total'],
                                
                            }
                            sey_pool.write(cr , uid,[skp_yearly_obj.id,], update_values, context=None)
        return True;
project_task()
