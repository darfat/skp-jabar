<html>
<head>
<style>
.break_me { page-break-before: always; }
installment_border{
	border-top:0px;
	border-bottom:1px;
	border-right:2px;
	border-left:2px;
	border-bottom-style:dotted;
}	
table
	{
	font-size:11px;
	}
td
	{
	padding:1px;
	valign=top;
	}
#page_note
	{
	border:0px solid #000;
	right:0px;
	position:relative;
	font-size:12px;
	margin-right:0px;
	}
table .header
	{
	display:none;
	}
.main
	{
	margin:0 auto;
	}
.main td
	{
	border:1px solid #000;
	}
td .pajak
	{
	border:0px;
	}
.partner td
	{
	border:0px;
	}
.lines
	{
	border-collapse:collapse;
	width:23.7cm;
	}
.inv_line td
	{
	border-top:0px;
	border-bottom:0px;
	}
.inv_cell
	{
	text-align:right;
	}
.subkegiatan
	{
	background-color: #000000;
	}
p { page-break-after: always}
</style>
<style type="text/css">
table.gridtable {
	font-family: verdana,arial,sans-serif;
	font-size:11px;
	color:#333333;
	border-width: 1px;
	border-color: #666666;
	border-collapse: collapse;
}
table.gridtable th {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #dedede;
}
table.gridtable td {
	border-width: 1px;
	padding: 8px;
	border-style: solid;
	border-color: #666666;
	background-color: #ffffff;
}

</style>

<style type="text/css">
/* flat table */
.sub-td{
background-color: #74ccba
}
.flat-table {
		/*top: 27%;
		left: 10%;*/
		border-collapse:collapse;
		font-family: 'Lato', Calibri, Arial, sans-serif;
		border: none;
		/*position: absolute;*/
        border-radius: 1px;
        -webkit-border-radius: 1px;
        -moz-border-radius: 1px;
	}
	.flat-table td {
		box-shadow: inset 0 -1px rgba(0,0,0,0.25), 
		inset 0 1px rgba(0,0,0,0.25);
	}
	.flat-table th {
		font-weight: normal;
		border=2px;
		background:#17a88a;
		color: #fffff;
		font-size: 1em;
	}
	.flat-table td {
		color: black;
		padding: 0.7em 1em 0.7em 1.15em;
		text-shadow: 0 0 1px rgba(255,255,255,0.1);
		font-size: 0.9em;
	}
	.flat-table tr {
		-webkit-transition: background 0.3s, box-shadow 0.3s;
		-moz-transition: background 0.3s, box-shadow 0.3s;
		transition: background 0.3s, box-shadow 0.3s;
	}
	.flat-table-1 {
		
		/*background:rgba(0,0,0,0.45);*/
	}
	.flat-table-1 tr:hover {
		background: rgba(0,0,0,0.19);
	}
	.flat-table-2 tr:hover {
		background: rgba(0,0,0,0.1);
	}
	.flat-table-2 {
		background: #f06060;
	}
	.flat-table-3 {
		background: #17a88a ;
	}
	.flat-table-3 tr:hover {
		background: rgba(0,0,0,0.1);
	}
</style>	
</head>
<body>
<% setLang('en_US') %>
<% var_mod=data['form']['paging_data'] + 1 %>  
	<TABLE width=100% >
	<TR>
		<TD width=100%>
				<!----------------------------------------  HEADER ----------------------------------------->
				<table id="header" width=100% border="0">
					<tr>
						<td colspan="5 "align="center"> <b>Rekapitulasi Hasil SKP</b></td>
						
					</tr>
					
				
				</table>
					
		<TD>
	</TR>`
	<TR>
		<TD width=100%>
				<!----------------------------------------  Content ----------------------------------------->
				<table class="flat-table flat-table-1" width=100% >
					
					<thead>
				<%
				sisa = 0
				is_setda = False
				if data['form']['company_id'] :
					if data['form']['company_id'][0] == 212 :
						is_setda = True
					endif
				endif
				%>
				
				%if not is_setda:
						<tr>
							<th  rowspan="2" width="2px">No</th>
							<th  rowspan="2" width="10px">Nama Pegawai</th>
							<th  rowspan="2" width="7px">NIP</th>
							<th  rowspan="2" width="7px">OPD/Dinas</th>
							<th  colspan="3"  width="5px">SKP</th>
							<th  colspan="2" width="3px">Perilaku</th>
							<th  colspan="2"  width="3px">Tambahan Dan Kreatifitas</th>
							<th  rowspan="2" width="5px">Nilai Total</th>						
						</tr>
						<tr>
							<th  width="5px">Jml</th>			
							<th   width="5px">Nilai </th>
							<th  width="5px">Nilai (%)</th>
							<th  width="5px">Nilai </th>
							<th  width="5px">Nilai (%)</th>
							<th  width="5px">Tambahan</th>
							<th  width="5px">Kreatifitas </th>
						</tr>
				%else :
					<tr>
							<th  rowspan="2" width="2px">No</th>
							<th  rowspan="2" width="10px">Nama Pegawai</th>
							<th  rowspan="2" width="7px">NIP</th>
							<th  rowspan="2" width="7px">OPD/Dinas</th>
							<th  rowspan="2" width="5px">Biro</th>
							<th  colspan="3"  width="5px">SKP</th>
							<th  colspan="2" width="3px">Perilaku</th>
							<th  colspan="2"  width="3px">Tambahan Dan Kreatifitas</th>
							<th  rowspan="2" width="5px">Nilai Total</th>						
						</tr>
						<tr>
							<th  width="5px">Jml</th>			
							<th   width="5px">Nilai </th>
							<th  width="5px">Nilai (%)</th>
							<th  width="5px">Nilai </th>
							<th  width="5px">Nilai (%)</th>
							<th  width="5px">Tambahan</th>
							<th  width="5px">Kreatifitas </th>
						</tr>
				%endif;
				
					</thead>
					<tbody>
					<% idx=1 %>
%for results in get_skp_summary_bulanan(data) :
				
							
				%if not is_setda:		
							<tr   >
							<td  align="center"   >${idx} </td>
							<td  > ${results.employee_id.name} </td>
							<td  > ${results.employee_id.nip} </td>
							<td  > ${results.company_id.name}  </td>
							<td  align="right" > ${formatLang (results.jml_skp)} </td>
							<td  align="right" > ${formatLang( results.nilai_skp )} </td>
							<td  align="right" > ${formatLang( results.nilai_skp_percent )} </td>
							<td  align="right" > ${formatLang( results.nilai_perilaku )} </td>
							<td  align="right" > ${formatLang( results.nilai_perilaku_percent )} </td>
							<td  align="right" > ${formatLang( results.fn_nilai_tambahan )} </td>
							<td  align="right" > ${formatLang( results.fn_nilai_kreatifitas )} </td>
							<td  align="right" > ${formatLang( results.nilai_total )} </td>
						</tr>
				%else:
							<tr   >
							<td  align="center"   >${idx} </td>
							<td  > ${results.employee_id.name} </td>
							<td  > ${results.employee_id.nip} </td>
							<td  > ${results.company_id.name}   </td>
							<td  > ${results.employee_id.biro_id.name} </td>
							<td  align="right" > ${formatLang (results.jml_skp)} </td>
							<td  align="right" > ${formatLang( results.nilai_skp )} </td>
							<td  align="right" > ${formatLang( results.nilai_skp_percent )} </td>
							<td  align="right" > ${formatLang( results.nilai_perilaku )} </td>
							<td  align="right" > ${formatLang( results.nilai_perilaku_percent )} </td>
							<td  align="right" > ${formatLang( results.fn_nilai_tambahan )} </td>
							<td  align="right" > ${formatLang( results.fn_nilai_kreatifitas )} </td>
							<td  align="right" > ${formatLang( results.nilai_total )} </td>
						</tr>
				
				%endif
				<% idx+=1 %>
			    <%    sisa = idx % var_mod %>
				%if sisa == 0 :
					<tr>	<td colspan="11"> <p class="break_me"> </p> </td>					</tr>
				%endif;
					
%endfor
				 </tbody>	
				</table>
				<!-- End Content -->

		<TD>
	</TR>
	<TR>
		<TD width=100%>
				<!----------------------------------------  FOOTER ----------------------------------------->
                %if sisa >= (var_mod -5 ):
						<p class="break_me"> </p>
					<br />
				%endif
				<table id="header" width=100% border="0">
					<tr>
					<td align="right"> <br>Periode &nbsp;  : &nbsp;  ${ get_period(data) } </td>
					</tr>
					<tr>
						
						<td align="right">
									Menyetujui,&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; 
									<br><br><br><br>
									<br><br><br>
									
									(____________________)
								</td>
					</tr>
					
				</table>
					
		<TD>
	</TR>
</TABLE>


</body>
</html>
