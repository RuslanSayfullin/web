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
});

// Присвоение номера догвора
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

// Адрес установки и адрес прописки из заявки
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
