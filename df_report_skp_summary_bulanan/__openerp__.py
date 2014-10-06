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
    "name": "Hasil Rekapitulasi Realisasi Per Bulan",
    "version": "1.0",
    "author": "darfat",
    "category": "Penilaian Prestasi Kerja /Reporting / Rekapitulasi Realisasi Bulanan",
    "description": """
   Hasil Rekapitulasi Realisasi Per Bulan
    """,
    "website" : "http://www.asdarfat.wordpress.com",
    "license" : "GPL-3",
    "depends": [
                "project","hr"
                ],
    "init_xml": [],
    'update_xml': [
                   "skp_summary_bulanan_report_view.xml"
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,

}