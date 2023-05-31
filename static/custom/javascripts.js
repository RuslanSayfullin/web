// Календарь jQuery
$(".dogovora_dates").datetimepicker({
	'step': 30,
	'lang': 'ru',
	'dayOfWeekStart': 1,
	'format': "d.m.Y",
	'timepicker':false,
	'scrollMonth': false,
	'scrollInput': false
});

// Расчет оплаты, предоплаты
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

// Адрес установки
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
$(document).ready(function() {
	oplata_predoplata_and_ostatok();
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

// Номер договора
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

// Поиск договоров
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

// Сроки доставки техники, данный код реализует функционал для ячейки "Сроки доставки техники", эта ячейка появляется только указанных договоров
$(document).ready(function() {
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
	// Поле для указания срока внутренней рассрочки, отображаеться только в случае выбора типа оплаты "Внутренняя рассрочка"
	if ($("#id_sposob_oplaty").val() != "internal_installment") {
		$('#id_installment_plan').parent().parent().hide();
	}
	$('#id_installment_plan').on('change', function() {
		if ($("#id_sposob_oplaty").val() == "internal_installment") {
			$('#id_installment_plan').parent().parent().show();
			$('#id_installment_plan').prop('required',true);
		} else {
			$('#id_installment_plan').parent().parent().hide();
			$('#id_installment_plan').prop('required',false);
			$('#id_installment_plan').val('');
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

// Поиск
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
		success: function(html){
			 $('#search_results').html(html);
		}
	});
}


