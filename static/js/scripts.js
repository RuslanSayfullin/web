var getUrlParameter = function getUrlParameter(sParam) {
	var sPageURL = decodeURIComponent(window.location.search.substring(1)),
			sURLVariables = sPageURL.split('&'),
			sParameterName,
			i;

	for (i = 0; i < sURLVariables.length; i++) {
		sParameterName = sURLVariables[i].split('=');

		if (sParameterName[0] === sParam) {
			return sParameterName[1] === undefined ? true : sParameterName[1];
		}
	}
};
var the_get_query = getUrlParameter('departament');
if (the_get_query !== undefined) {
	the_get_query = '?departament='+the_get_query;
} else {
	the_get_query = '';
}
/* <based on the code from _base.html */
$("#day").click(function(){
	$("#day").css({"display": "none"});
	$("#current_day").css({"display": "inline"}).focus();
});
$("#current_day").datetimepicker({
	timepicker: false,
	lang: 'ru',
	format: 'Y/m/d',
	dayOfWeekStart: 1,
	startDate: '{{ day|date:"Y/m/d" }}',
	onSelectDate: function(ct, $i){
		window.location = '/calendar/' + ct.dateFormat("Y/m/d") + the_get_query;
	}
});
/* </based on the code from _base.html */
/* <comment for technical preprint */
function hide_comment(id, csrf_token, ){
	/*$.ajax({
			type: "POST",
			url: "/comments/"+id+"/hide/",
			data : {csrfmiddlewaretoken: csrf_token},
			dataType : "json",
			success: function(data) {
					$('.comment_' + id).html(data);
			}
	});*/
	$('.comment_' + id).css({display: 'none'});
}
function hide_comments(uuid){
		$('#comments_uuid_' + uuid).css({display: 'none'});
}
/* </comment for technical preprint */
/* <dogovora */
$(".dogovora_dates").datetimepicker({
	'step': 30,
	'lang': 'ru',
	'dayOfWeekStart': 1,
	'format': "d.m.Y",
	'timepicker':false,
	'scrollMonth': false,
	'scrollInput': false
});
function oplata_predoplata_and_ostatok() {
	var vsego_k_oplate = $("#id_vsego_k_oplate").val();
	var oplata_predoplata_rub = $("#id_oplata_predoplata_rub").val();
	if (vsego_k_oplate && oplata_predoplata_rub && vsego_k_oplate > 0 && oplata_predoplata_rub > 0) {
		var oplata_predoplata_procent = oplata_predoplata_rub / (vsego_k_oplate / 100);
		oplata_predoplata_procent = oplata_predoplata_procent.toFixed(2);
		var oplata_ostatok_procent = 100 - oplata_predoplata_procent;
		oplata_ostatok_procent = oplata_ostatok_procent.toFixed(2); // необязательно!
		var oplata_ostatok_rub = vsego_k_oplate - oplata_predoplata_rub;
		$("#id_oplata_predoplata_procent").val(oplata_predoplata_procent);
		$("#id_oplata_ostatok_procent").val(oplata_ostatok_procent);
		$("#id_oplata_ostatok_rub").val(oplata_ostatok_rub);
	} else {
		$("#id_oplata_predoplata_procent").val('');
		$("#id_oplata_ostatok_procent").val('');
		$("#id_oplata_ostatok_rub").val('');
	}
	if (oplata_predoplata_procent < 0) {
		$(".oplata_predoplata_procent_form_group").addClass("has-warning");
	} else {
		$(".oplata_predoplata_procent_form_group").removeClass("has-warning");
	}
	if (oplata_ostatok_procent < 0) {
		$(".oplata_ostatok_procent_form_group").addClass("has-warning");
	} else {
		$(".oplata_ostatok_procent_form_group").removeClass("has-warning");
	}
	if (oplata_ostatok_rub < 0) {
		$(".oplata_ostatok_rub_form_group").addClass("has-warning");
	} else {
		$(".oplata_ostatok_rub_form_group").removeClass("has-warning");
	}
}
function use_froze_data_for_dogovor(field_auto_id, the_value) {
	if (field_auto_id == 'id_adres_ustanovki') {
		$('input#id_adres_ustanovki').val(the_value);
	} else if(field_auto_id == 'id_adres_propiski') {
		$('input#id_adres_propiski').val(the_value);
	} else {
		fio = the_value.split(' ');
		if(fio[0] && fio[1] && fio[2]){
			$('input#id_passport_familiya').val(fio[0]);
			$('input#id_passport_imya').val(fio[1]);
			$('input#id_passport_otchestvo').val(fio[2]);
		}
		else{
			if (field_auto_id == 'id_passport_familiya') {
				$('input#id_passport_familiya').val(the_value);
			}
			else if (field_auto_id == 'id_passport_imya') {
				$('input#id_passport_imya').val(the_value);
			}
			else if (field_auto_id == 'id_passport_otchestvo') {
				$('input#id_passport_otchestvo').val(the_value);
			}
		}
	}
}
/*function stoimost_dostavki() {
	var km = $('input#id_stoimost_dostavki_vne_ufa_km').val();
	km = parseInt(km);
	var stoimost = km * 24;
	if (stoimost) {('internal installment', 'Внутренняя рассрочка'),
		$('input#id_stoimost_dostavki_vne_ufa').val(stoimost);
		$('input#id_stoimost_dostavki_vne_ufa_itogo').val(stoimost);
	} else {
		$('input#id_stoimost_dostavki_vne_ufa').val('');
		$('input#id_stoimost_dostavki_vne_ufa_itogo').val('');
	}
}
function stoimost_dostavki_onload() {
	var stoimost_dostavki_vne_ufa_itogo = $('input#id_stoimost_dostavki_vne_ufa_itogo').val();
	stoimost_dostavki_vne_ufa_itogo = parseInt(stoimost_dostavki_vne_ufa_itogo);
	var kolvo_km = stoimost_dostavki_vne_ufa_itogo / 24;
	if(kolvo_km){
		$('input#id_stoimost_dostavki_vne_ufa_km').val(kolvo_km);
	} else {
		$('input#id_stoimost_dostavki_vne_ufa_km').val('');
	}
}*/
$(document).ready(function() {
	oplata_predoplata_and_ostatok();
	/*stoimost_dostavki_onload();*/
	if ($("form.dogovora").attr("allowed") == 'disallowed') {
		$("input.form-control").attr("disabled", "disabled");
		$("select.form-control").attr("disabled", "disabled");
		$(".bootstrap-tagsinput").children("input").attr("disabled", "disabled");
	}
});
$('input#id_vsego_k_oplate').change(function(){
	oplata_predoplata_and_ostatok();
});
$('input#id_oplata_predoplata_rub').change(function(){
	oplata_predoplata_and_ostatok();
});
/*$('input#id_stoimost_dostavki_vne_ufa_km').change(function(){
	stoimost_dostavki();
});*/
function nomer_dogovora(csrf_token, self_id, id_from_existing_dogovor){
	if (id_from_existing_dogovor === undefined) {
		var data_for_send = "csrfmiddlewaretoken="+csrf_token+"&self_id="+self_id;
	}
	else {
		var data_for_send = "csrfmiddlewaretoken="+csrf_token+"&self_id="+self_id+"&id_from_existing_dogovor="+id_from_existing_dogovor;
	}
	$.ajax({
		type: "POST",
		url: "/dogovora/nomer_dogovora",
		data: data_for_send,
		success: function(data) {
			$("#id_nomer_dogovora").val(data);
			//alert("Номер к договору присвоен, после перезагрузки страницы изменить его будет нельзя.")
			$("#nomer_dogovora_info").html("Номер к договору присвоен, изменить нельзя.");
		}
	});
}
function poisk_dogovorov(csrf_token){
	var fio = $('#poisk_dogovorov').val();
	$.ajax({
		type: "POST",
		url: "/dogovora/poisk_dogovorov",
		data: "csrfmiddlewaretoken="+csrf_token+"&fio="+fio,
		success: function(data) {
			$('#poisk_dogovorov_div').html(data);
		}
	});
}
function kopirovat_dogovor(elem){
	var dogovor = $(elem).parent();
	$('#id_passport_familiya').val($(dogovor).children('.passport_familiya').html());
	$('#id_passport_imya').val($(dogovor).children('.passport_imya').html());
	$('#id_passport_otchestvo').val($(dogovor).children('.passport_otchestvo').html());

	$('#id_passport_birthday_date').val($(dogovor).children('.passport_birthday_date').html());
	$('#id_passport_birthday_place').val($(dogovor).children('.passport_birthday_place').html());
	$('#id_passport_seria').val($(dogovor).children('.passport_seria').html());
	$('#id_passport_nomer').val($(dogovor).children('.passport_nomer').html());
	$('#id_passport_kem_vydan').val($(dogovor).children('.passport_kem_vydan').html());
	$('#id_passport_kogda_vydan').val($(dogovor).children('.passport_kogda_vydan').html());
	$('#id_passport_kp').val($(dogovor).children('.passport_kp').html());
	$('#id_adres_propiski').val($(dogovor).children('.adres_propiski').html());
	$('#id_adres_ustanovki').val($(dogovor).children('.adres_ustanovki').html());

	$('#id_vsego_k_oplate').val($(dogovor).children('.vsego_k_oplate').html());
	$('#id_oplata_predoplata_rub').val($(dogovor).children('.oplata_predoplata_rub').html());
	$('#id_naimenov_soputstv_izdeliy').val($(dogovor).children('.naimenov_soputstv_izdeliy').html());
	$('#id_summa_za_soputstv_uslugi').val($(dogovor).children('.summa_za_soputstv_uslugi').html());
	$('#id_stoimost_dostavki_vne_ufa').val($(dogovor).children('.stoimost_dostavki_vne_ufa').html());

	$('#id_data_podpisaniya').val($(dogovor).children('.data_podpisaniya').html());
	$('#id_srok_ispolneniya_rabot').val($(dogovor).children('.srok_ispolneniya_rabot').html());
	//$('#id_tip_dogovora').val($(dogovor).children('.tip_dogovora').html());
	//$('#id_nomer_dogovora').val($(dogovor).children('.nomer_dogovora').html());
	//$('#id_tip_opisanie_izdeliya').val($(dogovor).children('.tip_opisanie_izdeliya').html());
	$('#id_doverennye_lica').val($(dogovor).children('.doverennye_lica').html());
	$('#id_nachalo_rabot_data').val($(dogovor).children('.nachalo_rabot_data').html());
	$('#id_okonchanie_rabot_data').val($(dogovor).children('.okonchanie_rabot_data').html());

	alert('В текущем договоре поля заполнены. Поля "Тип договора", "Номер договора" и "Тип (описание) изделия" не копируются.');
	oplata_predoplata_and_ostatok();
}

$(document).ready(function() {
	$('input#id_dizaynerskoe_voznagrazhdenie').parent().parent().css({'display': 'none'});
	$('select#id_akciya').parent().parent().css({'display': 'none'});
});
    // функция позволяет в ручную присваивать номера для договоров с юр. лицами
function ooo_reforma(){
	var the_value = $('#id_tip_dogovora').val();
	if(the_value == 'ooo_reforma_plus_s_nds' || the_value == 'ooo_reforma_plus_bez_nds' || the_value == 'ooo_reforma_sever_s_nds' || the_value == 'ooo_reforma_sever_bez_nds' || the_value == 'ooo_reforma_sever' || the_value == 'ooo_reforma_plus' || the_value == 'iskusstvenny_kamen_ooo_re_forma_plus' || the_value == 'ooo_reforma_plus_tehnika' || the_value == 'montazh_demontazh_ooo_reforma_plus_yur' || the_value == 'podklyuchenie_2021_06_tehniki_ooo_reforma_plus_yur' || the_value == 'transportation_services_ooo_reforma_plus_yur' || the_value == 'entity_furniture_making_reforma_plus_ooo' || the_value == 'juridical_moscow_ooo-refabrik_furniture_making' || the_value == 'juridical_furniture_making_fabrika_mebeli_reforma' || the_value == 'entity_householdtec_reforma_plus_ooo' || the_value == 'juridical_moscow_ooo-refabrik_householdtec' || the_value =='juridical_householdtec_fabrika_mebeli_reforma' || the_value == 'entity_connectiontec_reforma_plus_ooo' || the_value == 'juridical_connectiontec_fabrika_mebeli_reforma' || the_value == 'entity_mattresses_reforma_plus_ooo' || the_value == 'juridical_ooo-refabrik_mattresses' || the_value == 'juridical_mattresses_fabrika_mebeli_reforma' || the_value == 'juridical_ooo-refabrik_mattresses' || the_value == 'entity_finishedfur_reforma_plus_ooo' || the_value == 'juridical_ooo-refabrik_finishedfur' || the_value == 'juridical_finishedfur_fabrika_mebeli_reforma' || the_value == 'entity_stone_reforma_plus_ooo' || the_value == 'juridical_ooo-refabrik_stone' || the_value == 'juridical_stone_reforma_fabrika_mebeli_reforma' || the_value == 'entity_textile_reforma_plus_ooo' || the_value == 'juridical_moscow_ooo-refabrik_textile' || the_value == 'juridical_textile_reforma_fabrika_mebeli_reforma' || the_value == 'entity_transport_reforma_plus_ooo' || the_value == 'juridical_transport_reforma_fabrika_mebeli_reforma' || the_value == 'entity_assembling_reforma_plus_ooo' || the_value == 'juridical_assembling_reforma_fabrika_mebeli_reforma' || the_value == 'entity_furnitureassemblywork_reforma_plus_ooo' || the_value == 'juridical_furnitureassemblywork_fabrika_mebeli_reforma' || the_value == 'juridical_moscow_ooo-refabrik_furnitureassemblywork' || the_value == 'entity_ufa_furniture_making_fabrika_mebeli_reforma' || the_value == 'entity_ufa_ooo-refabrik_furniture_making' || the_value == 'entity_ufa_householdtec_fabrika_mebeli_reforma' || the_value == 'entity_ufa_ooo-refabrik_householdtec' || the_value == 'entity_ufa_connectiontec_fabrika_mebeli_reforma' || the_value == 'entity_ufa_mattresses_fabrika_mebeli_reforma' || the_value == 'entity_ufa_ooo-refabrik_mattresses' || the_value == 'entity_ufa_ooo-refabrik_mattresses' || the_value == 'entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma' || the_value == 'entity_ufa_stone_fabrika_mebeli_reforma' || the_value == 'entity_ufa_ooo-refabrik_stone' || the_value == 'entity_ufa_finishedfur_fabrika_mebeli_reforma' || the_value == 'entity_ufa_ooo-refabrik_finishedfur' || the_value == 'entity_ufa_textile_fabrika_mebeli_reforma' || the_value == 'entity_ufa_ooo-refabrik_textile' || the_value == 'entity_ufa_transport_fabrika_mebeli_reforma' || the_value == 'entity_ufa_assembling_fabrika_mebeli_reforma'){
		$('#id_nomer_dogovora').prop("disabled", false);
	}
	else {
		$('#id_nomer_dogovora').prop("disabled", true);
	}
}
$(document).ready(function() {
	$('#id_tip_dogovora').on('change', function() {
		ooo_reforma();
	})
	ooo_reforma();
});
$(document).ready(function() {
	// Сроки доставки техники, данный код реализует функционал для ячейки "Сроки доставки техники", эта ячейка появляется только указанных договоров
	$('#id_technics_sroki_dostavki_tehniki').parent().parent().hide();
	$('#id_technics_sroki_dostavki_tehniki_v_dnyah').parent().parent().hide();
	if ($("#id_tip_dogovora").val() == "technic_2021_04_ip_frolov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_bagautdinov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_sadykov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_hafizov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_frolov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_sadykov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_hafizov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_usmanov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_frolov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_sadykov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_hafizov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_usmanov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_frolov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_bagautdinov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_sadykov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_frolov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_bagautdinov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_sadykov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ooo-refabrik" || $("#id_tip_dogovora").val() == "mattresses_ooo-refabrik" || $("#id_tip_dogovora").val() == "entity_householdtec_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_moscow_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "juridical_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_mattresses_reforma_plus_ooo" || $("#id_tip_dogovora").val() ==  'juridical_ooo-refabrik_mattresses' || $("#id_tip_dogovora").val() == "juridical_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "entity_ufa_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() =="entity_ufa_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma") {
		$('#id_technics_sroki_dostavki_tehniki').parent().parent().show();
	}
	$('#id_tip_dogovora').on('change', function() {
		if ($("#id_tip_dogovora").val() == "technic_2021_04_ip_frolov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_bagautdinov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_sadykov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_hafizov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_frolov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_sadykov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_hafizov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_usmanov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_frolov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_sadykov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_hafizov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_usmanov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_frolov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_bagautdinov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_sadykov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_frolov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_bagautdinov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_sadykov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ooo-refabrik" || $("#id_tip_dogovora").val() == "mattresses_ooo-refabrik" || $("#id_tip_dogovora").val() == "entity_householdtec_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_moscow_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "juridical_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_mattresses_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "juridical_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "entity_ufa_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() =="entity_ufa_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma") {
			$('#id_technics_sroki_dostavki_tehniki').parent().parent().show();
		} else {
			$('#id_technics_sroki_dostavki_tehniki').parent().parent().hide();
		}
	})
	if ($("#id_technics_sroki_dostavki_tehniki").val() == "2") {
		$('#id_technics_sroki_dostavki_tehniki_v_dnyah').parent().parent().show();
	}
	$('#id_technics_sroki_dostavki_tehniki').on('change', function() {
		if ($("#id_technics_sroki_dostavki_tehniki").val() == "2") {
			$('#id_technics_sroki_dostavki_tehniki_v_dnyah').parent().parent().show();
		} else {
			$('#id_technics_sroki_dostavki_tehniki_v_dnyah').parent().parent().hide();
		}
	})
	// Телефоны доверенных лиц
	if ( $('#id_doverennye_lica').length && $('#id_doverennye_lica').val().length == 0 ) {
		$('#id_doverennye_lica_telefony').parent().parent().hide();
	}
	$('#id_doverennye_lica').on('keyup', function() {
		if ( $('#id_doverennye_lica').val().length ) {
			$('#id_doverennye_lica_telefony').parent().parent().show();
			$('#id_doverennye_lica_telefony').prop('required',true);
		} else {
			$('#id_doverennye_lica_telefony').parent().parent().hide();
			$('#id_doverennye_lica_telefony').prop('required',false);
			$('#id_doverennye_lica_telefony').val('');
		}
	})
	// Сроки доставки техники, данный код реализует функционал для ячейки "№ договора на изготовление мебели", эта ячейка появляется только указанных договоров
	$('#id_drugoy_dogovor').parent().parent().hide();
	if ($("#id_tip_dogovora").val() == "technic_2021_04_ip_frolov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_bagautdinov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_sadykov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_hafizov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_frolov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_bagautdinov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_sadykov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_frolov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_bagautdinov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_sadykov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ooo-refabrik" || $("#id_tip_dogovora").val() == "mattresses_ooo-refabrik" || $("#id_tip_dogovora").val() == "m_householdtec_ip_frolov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_sadykov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_hafizov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_usmanov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_frolov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_sadykov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_hafizov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_usmanov" || $("#id_tip_dogovora").val() == "entity_householdtec_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_moscow_ooo-refabrik_householdtec"  || $("#id_tip_dogovora").val() == "juridical_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_mattresses_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "juridical_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "entity_ufa_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() =="entity_ufa_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma") {
		$('#id_drugoy_dogovor').parent().parent().show();
	}
	$('#id_tip_dogovora').on('change', function() {
		if ($("#id_tip_dogovora").val() == "technic_2021_04_ip_frolov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_bagautdinov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_sadykov" || $("#id_tip_dogovora").val() == "technic_2021_04_ip_hafizov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_frolov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_bagautdinov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_sadykov" || $("#id_tip_dogovora").val() == "matrasy_2021_06_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_frolov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_bagautdinov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_sadykov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ip_hafizov" || $("#id_tip_dogovora").val() == "carpets_and_rugs_ooo-refabrik" || $("#id_tip_dogovora").val() == "mattresses_ooo-refabrik" || $("#id_tip_dogovora").val() == "m_householdtec_ip_frolov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_sadykov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_hafizov" || $("#id_tip_dogovora").val() == "m_householdtec_ip_usmanov"  || $("#id_tip_dogovora").val() == "m_mattresses_ip_frolov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_bagautdinov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_sadykov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_hafizov" || $("#id_tip_dogovora").val() == "m_mattresses_ip_usmanov" || $("#id_tip_dogovora").val() == "entity_householdtec_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_moscow_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "juridical_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_mattresses_reforma_plus_ooo" || $("#id_tip_dogovora").val() == "juridical_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "juridical_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_householdtec_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() == "entity_ufa_ooo-refabrik_householdtec" || $("#id_tip_dogovora").val() == "entity_ufa_mattresses_fabrika_mebeli_reforma" || $("#id_tip_dogovora").val() =="entity_ufa_ooo-refabrik_mattresses" || $("#id_tip_dogovora").val() == "entity_ufa_carpets_and_rugs_fabrika_mebeli_reforma") {
			$('#id_drugoy_dogovor').parent().parent().show();
		} else {
			$('#id_drugoy_dogovor').parent().parent().hide();
		}
	})
});
function drugoy_dogovor(csrf_token, self_id, id_dogovora_na_izgotovlenie_mebeli){
	var data_for_send = "csrfmiddlewaretoken="+csrf_token+"&self_id="+self_id+"&id_dogovora_na_izgotovlenie_mebeli="+id_dogovora_na_izgotovlenie_mebeli;
	$.ajax({
		type: "POST",
		url: "/dogovora/drugoy_dogovor",
		data: data_for_send,
		success: function(data) {
			$("#id_drugoy_dogovor").val(data);
		}
	});
}
$('.uslugi_po_podklyucheniyu_create_update').on('change', function() {
	var usluga_key = $(this).attr('key');
	console.log(usluga_key);
	var usluga_price = $(this).find('option:selected').attr('price');
	console.log(usluga_price);
	$('#usluga_tsena_'+usluga_key).val(usluga_price);
})
/* </dogovora */
/* <otchety */
$(document).ready(function() {
	$('table#otchet_1 tbody tr').click(function(){
		var link = $(this).attr('a');
		window.open(link, '_blank');
	});
});
/* </otchety */
/* <vechernie_otchety */
var istochniki = ['Email-рассылка',
	'2Гис',
	'Баннер',
	'Бартер-кард',
	'Бартер',
	'Буклет',
	'Визитка',
	'Вконтакте',
	'Внутренний',
	'Вывеска салон',
	'Гугл',
	'Дизайнер интерьера',
	'Живо-сайт',
	'Журнал гланец',
	'Оформление запроса (почта, ЖС, соц. сети)',
	'Инстаграм',
	'Инстаграм купон Вытяжка в подарок',
	'новости в СМИ',
	'Интернет',
	'Квитанция',
	'Купон от партнеров',
	'Листовка',
	'Лифт',
	'Пазик',
	'Первый трест',
	'Повторный заказ',
	'Радио',
	'Радио в ТЦ',
	'Реклама (обобщенный ответ, в случае, если клиент затрудняется)',
	'Ре-пин (наши дизайнеры интерьера)',
	'Рекомендация',
	'Сайт',
	'Сертификат',
	'Сертификат Текстиль',
	'СМС',
	'Стенд в Галерее Арт',
	'ТВ реклама',
	'Тент',
	'Листовка на двери (Хенгер)',
	'Шоу-рум',
	'Ютуб',
	'Яндекс',
	'Входящий звонок',
	'Ре-фабрик Инстаграм',
	'Москва Инстаграм',
	'Москва Рекомендации',
	'Москва Повтор',
	'Москва Дизайнер интерьера',
	'От Фархада',
	'Умный дом акция',
	'Телеграм',
	'Дизайнер интерьера (рекомендация от др. ДИ)',
	'Новосел Зиларт',
	'Обзвон купон',
	'Карта 10% Уфа',
	'Карта 10% Москва',
	'Строитель',
	'Авито',
	'Визуализаторы',
	'Новосел',
	'Застройщик',
	];
$('.istochnik').tagsinput({
	typeahead: {
		source: istochniki
	},
	onTagExists: function(item, $tag) {
		$tag.hide.fadeIn();
	},
	freeInput: false
});

var vid_oplaty = ['Наличные', 'Карта'];
$('.vid_oplaty').tagsinput({
	typeahead: {
		source: vid_oplaty
	},
	onTagExists: function(item, $tag) {
		$tag.hide.fadeIn();
	},
	freeInput: false
});

$('.bootstrap-tagsinput').change(function(){
	$(this).find('input').val('');
});


function show_data_vechernie_otchety(){
	if($("#vechernie_otchety_day").prop("checked") == true && $("#vechernie_otchety_all_time").prop("checked") == false){
		$('#vechernie_otchety_data').css({'display': 'block'});
	}
	else if($("#vechernie_otchety_day").prop("checked") == false && $("#vechernie_otchety_all_time").prop("checked") == true){
		$('#vechernie_otchety_data').css({'display': 'none'});
	}
}
$(document).ready(function() {
	show_data_vechernie_otchety();
});
$("#vechernie_otchety_day").click(function(){
	show_data_vechernie_otchety();
});
$("#vechernie_otchety_all_time").click(function(){
	show_data_vechernie_otchety();
});
$(".vechernie_otchety_dates").datetimepicker({
		'step': 30,
		'lang': 'ru',
		'dayOfWeekStart': 1,
		'format': "d.m.Y H:i",
		'timepicker': true,
		'scrollMonth': false,
		'scrollInput': false
});

	/* <vyezd */
	function calculate_sum(the_element){
		var summa_predoplaty = 0;
		$('.view_otchet_vyezd .'+the_element).each(function(i,elem) {
			if($(this).text()){
				summa_predoplaty = summa_predoplaty + parseInt($(this).text());
				var this_text = $(this).text();
				$(this).text(this_text.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 '))
			}
		})
//			console.log(summa_predoplaty);
		summa_predoplaty = summa_predoplaty.toString();
		$('#'+the_element).text(summa_predoplaty.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ') + ' руб.');
	}
	$(document).ready(function() {
		calculate_sum('jq_sd');
		calculate_sum('jq_sp');
	});
	/* </vyezd */
	/* <call */
	function calculate_sum2(the_element){
		var summa_predoplaty = 0;
		$('.view_otchet_call .'+the_element).each(function(i,elem) {
			if($(this).text()){
				summa_predoplaty = summa_predoplaty + parseInt($(this).text());
				var summa_predoplaty_str = summa_predoplaty.toString();
				//$(this).text(summa_predoplaty_str.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 '))
			}
		})
//			console.log(summa_predoplaty);
		summa_predoplaty = summa_predoplaty.toString();
		$('#'+the_element).text(summa_predoplaty.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ') + '');
	}
	$(document).ready(function() {
		calculate_sum2('zamerov_na_vyezd');
		calculate_sum2('nazn_priglash_v_salon');
		calculate_sum2('zamerov_s_vk');
		calculate_sum2('zamerov_s_insta');
		calculate_sum2('zamerov_iz_jivo');
		calculate_sum2('priglas_iz_jivo');
		calculate_sum2('konsult_v_jivo');
	});
	/* </call */
/* </vechernie_otchety */
/* <froze:month_calendar */
$(document).ready(function() {
	$("td.m_cal a").click(function(){
		var csrf_token = $("div#month_calendar").attr("csrf_token");
		var event_date_and_designer = $(this).parent().attr("id");
		$.ajax({
			type: "POST",
			url: "/mcalendar/create_delete/" + event_date_and_designer,
			data: "csrfmiddlewaretoken="+csrf_token,
			success: function(data) {
				if (data == "error_PastEvent") {
					alert("Выходной нельзя поставить в прошедшее время, только на сегодняшний и будущие дни. Также нельзя удалить прошедший выходной, только выходные сегодняшнего и будущих дней.")
				}
				else if (data == "error_Exception") {
					alert("Неизвестная ошибка 1");
				}
				else if(data == "error_AccessDenied") {
					alert("Недостаточно прав для создания/удаления выходных в графике");
				}
				else {
					data = data.split(',');
					if(data[0] == "deleted") {
						$("#"+data[1]).removeClass("m_restday");
					}
					else if(data[0] == "created") {
						$("#"+data[1]).addClass("m_restday");
					}
					else {
						alert("Неизвестная ошибка 2");
					}
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					alert('Ошибка 403 (Нет прав доступа на это действие)');
				}
			}
		});
		return false;
	});

	var month_widths = [];
	var month_tbody_row = $('#month_calendar').children('table').children('tbody').children('tr:nth-child(2)').children('td');
	$(month_tbody_row).each(function(i,elem) {
		month_widths.push($(elem).outerWidth());
		$(elem).css({'width': month_widths[i]+'px'});
	});
	var month_thead_row = $('#month_calendar').children('table').children('thead').children('tr:first').children('th');
	$(month_thead_row).each(function(i,elem) {
		$(elem).css({'width': month_widths[i]+'px'});
	});

	$(window).scroll(function() {
		var top = $(document).scrollTop();
		if (top < 207) {
			$('#month_calendar').children('table').children('thead').css({'position': 'initial'});
			$('#month_calendar').css({'margin-top': '0px'});
		} else {
			$('#month_calendar').children('table').children('thead').css({'position': 'fixed'});
			$('#month_calendar').css({'margin-top': '58px'});
		}
	});

});

/* </froze:month_calendar */
/* <froze:froze */
function dubl_btn(csrf_token, uuid){
	$.ajax({
		type: "POST",
		url: "/dubl_btn",
		cache: false,
		data: "csrfmiddlewaretoken="+csrf_token+"&uuid="+uuid,
		success: function(answer){
//			console.log(answer);
			if(answer == 'True'){
				$('#dubl_btn_'+uuid).addClass('active');
				$('#dubl_text_'+uuid).show();
			}
			else{
				$('#dubl_btn_'+uuid).removeClass('active');
				$('#dubl_text_'+uuid).hide();
			}
		},
		error: function (xhr, ajaxOptions, thrownError) {
			if(xhr.status==403) {
				alert('Ошибка 403 (Нет прав доступа на это действие)');
			}
		}
	});
}
/* </froze:froze */
/* <search */
function the_new_search(csrf_token){
	var po_telefonu = $('#po_telefonu').val();
	var po_adresu = $('#po_adresu').val();
	var po_imeni = $('#po_imeni').val();
	var by_designer = $('#by_designer').val();

	$.ajax({
		type: "GET",
		url: "/search/search_results",
		cache: false,
		data: "po_telefonu="+po_telefonu+"&po_adresu="+po_adresu+"&po_imeni="+po_imeni+"&by_designer="+by_designer,
//		beforeSend: function(){
//				$('#loading_image').show();
//		},
//		complete: function(){
//				$('#loading_image').hide();
//		},
		success: function(html){
			 $('#search_results').html(html);
		}
	});
}
/*
*
*
*
</search
*
*
*
*/
/*
*
*
*
<staff.prava_dostupa
*
*
*
*/
$('table#prava_dostupa').find('a').click(function(){
	var csrf_token = $('table#prava_dostupa').attr('csrf');
	var user = $(this).attr('user');
	var permission = $(this).attr('permission');

	$.ajax({
		context: this,
		type: "POST",
		url: "/staff/prava_dostupa_postavit_udalit",
		data: {csrfmiddlewaretoken: csrf_token, permission: permission, user: user},
		success: function(data) {
			$(this).removeClass('btn-success');
			$(this).removeClass('btn-warning');

			if(data == 'prava_dostupa_udaleno') {
				$(this).addClass('btn-warning');
			}
			else if(data == 'prava_dostupa_dobavleno') {
				$(this).addClass('btn-success');
			}
			else {
				alert('Ошибка');
				$(this).addClass('btn-default');
			}
		}.bind(this),
		error: function (xhr, ajaxOptions, thrownError) {
			if(xhr.status==403) {
				alert('Ошибка 403 (Нет прав доступа на это действие)');
			}
		}
	});
});
$(document).ready(function() {
	$('tbody').scroll(function(e) { //detect a scroll event on the tbody
		$('thead').css("left", -$("tbody").scrollLeft()); //fix the thead relative to the body scrolling
		$('thead th:nth-child(1)').css("left", $("tbody").scrollLeft()); //fix the first cell of the header
		$('tbody td:nth-child(1)').css("left", $("tbody").scrollLeft()); //fix the first column of tdbody
	});
});
/*
*
*
*
</staff.prava_dostupa
*
*
*
*/
/*
*
*
*
<ko_tz
*
*
*
*/
function set_ko_tz_route(route, froze_id, csrf_token) {
	$.ajax({
		type: "POST",
		url: "/ko_tz/ko_tz_route_set/" + froze_id,
		cache: false,
		data: "csrfmiddlewaretoken="+csrf_token+"&route="+route,
		success: function(data){
			var answer = JSON.parse(data);
//			console.log(answer['route_changed']);
//			console.log(answer['for_alert']);
//			console.log(answer['for_html']);
			if (answer['route_changed'] == 'yes') {
				$(".ko_tz_status_"+froze_id).html(answer['for_html']);
			}
			alert(answer['for_alert']);
		}
	});
}
function open_tz_ko(froze_id, url) {
	var div_html = $("#ko_tz_"+froze_id);
	var btn = $("#ko_tz_btn_"+froze_id);

//	console.log(div_html.html().length);
	if(div_html.html().length > 0){
		div_html.html('');
		btn.text('Открыть историю ТЗ/КО... ▼');
	} else {
		$.ajax({
			type: "GET",
			url: url + '?redirect_to=' + window.location.pathname,
			cache: false,
			data: "",
			beforeSend: function() {
				$('#loading_image').show();
			},
			complete: function() {
				$('#loading_image').hide();
			},
			success: function(data){
				 btn.show();
				 div_html.html(data);
				 div_html.show();
				 btn.text('Скрыть историю ТЗ/КО... ▲');

				 $("#ko_tz_files_for_1c_" + froze_id).html('');
				 $("#ko_tz_btn_files_for_1c_" + froze_id).text('Показать файлы для 1С');
			}
		});
	}
	btn.show();
}
function open_tz_ko_files_for_1c(froze_id, url){
	var div_html = $("#ko_tz_files_for_1c_"+froze_id);
	var btn = $("#ko_tz_btn_files_for_1c_"+froze_id);

//	console.log(div_html.html().length);
	if(div_html.html().length > 0) {
		div_html.html('');
		btn.text('Показать файлы для 1С');
	} else {
		$.ajax({
			type: "GET",
			url: url + '?redirect_to=' + window.location.pathname,
			cache: false,
			data: "",
			success: function(data){
				 btn.show();
				 div_html.html(data);
				 btn.text('Скрыть файлы для 1С... ▲');

				 $("#ko_tz_"+froze_id).html('');
				 $("#ko_tz_btn_"+froze_id).text('Открыть историю ТЗ/КО... ▼');
			}
		});
	}
}
function letter_files_download(class_of_file){
	var urls = [];
	$('.'+class_of_file).each(function(i,elem) {
		urls.push($(elem).prop('href'));
		// elem.click();
		// window.open($(elem).prop('href'));
	});

	$.each(urls,function (intIndex, objValue) {
		 window.open(objValue);
	});
}

function $_GET(key) {
	var p = window.location.search;
	p = p.match(new RegExp(key + '=([^&=]+)'));
	return p ? p[1] : false;
}
$(document).ready(function() {
	var open_froze_ko_tz = $_GET('open_froze_ko_tz');
	if (open_froze_ko_tz > 0) {
		$('#ko_tz_btn_'+open_froze_ko_tz).click();
	}
	var open_froze_ko_tz_1c = $_GET('open_froze_ko_tz_1c');
	if (open_froze_ko_tz_1c > 0) {
		$('#ko_tz_btn_files_for_1c_'+open_froze_ko_tz_1c).click();
	}
});
function display_actual_status_ko_tz() {
	var froze_id = 0
	$('dd.status_ko_tz').each(function(i,elem) {
		froze_id = $(elem).attr("froze");
		$.ajax({
			type: "GET",
			url: "/ko_tz/check_ko_tz_status/" + froze_id + "/",
			data: "",
			success: function(data) {
				var answer = JSON.parse(data);
				$(elem).text(answer['ko_tz_status_words']);
			}
		});
	})
}
$(document).ready(function() {
	if ($("dd").is(".status_ko_tz")) {
		setInterval(function() {
			display_actual_status_ko_tz();
		}, 10000);
	}
});

/*
*
*
*
</ko_tz
*
*
*
*/
$(document).ready(function() {
	var sadf= $('input').attr('autocomplete','off');

	$('.have_files_tz').change(function(){
		if(this.checked){
			$('.files_tz').fadeIn('fast');
			$('.files_tz').prop('required', true);
			$('.have_files_tz').prop('checked', true);
		}
		else {
			$('.files_tz').fadeOut('fast');
			$('.files_tz').prop('required', false);
			$('.have_files_tz').prop('checked', false);
		}
	});
});

/* */
