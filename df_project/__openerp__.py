##############################################################################
#
#    Darmawan Fatriananda
#    BKD Pemprov Jabar
#    Copyright (c) 2014 <http://www.asdarfat.wordpress.com>
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

{
    "name": "Kegiatan Dan Program Pemprov Jabar (Project)",
    "version": "1.0",
    "author": "darfat",
    "category": "Project/Unit Kerja",
    "description": """
    Berhubungan dengan "Kegiatan Dan Program Pemprov Jabar dalam satuan unit kerja.
    Tiap unit kerja menyusun Satuan Rencana Kerja Per tahun dan Tiap Bulan
    Pada Akhir Periode outnya adalah nilai dari Target vs Realisasi.
    Nilai Tersebut akan di konversi menjadi Sejumlah Uang (Bonus Tahunan)
    """,
    "website" : "http://www.asdarfat.wordpress.com",
    "license" : "GPL-3",
    "depends": [
                "project","hr"
                ],
    "init_xml": [],
    'update_xml': [
                   "security/project_security.xml",
                   "project_view.xml","project_config_view.xml",
                   #"project_task_view.xml",
                   "project_task_skp_view.xml",                   
                   "project_task_perilaku_view.xml",
                   "employee_view.xml",
                   "project_menu_view.xml",
                   "wizard/project_task_massive_view.xml",
                   "wizard/project_massive_view.xml",
                   "project_task_menu_view.xml",    
                   "popup_view/project_task_popup_view.xml",
                    
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': 'certificate',
}
