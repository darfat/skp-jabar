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
    "name": "Data Kepegwaian Perangkat Daerah",
    "version": "1.0",
    "author": "darfat",
    "category": "Partner/Kepegawaian",
    "description": """
    Berhubungan dengan Employee
    """,
    "website" : "http://www.asdarfat.wordpress.com",
    "license" : "GPL-3",
    "depends": [
                "df_hr",
                ],
    "init_xml": [],
    'data': [      "partner_employee_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
