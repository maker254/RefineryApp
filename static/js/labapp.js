$(document).ready(function(){

	$('table.td-hide tbody tr').each(function() {
		  $(this).find('td').each(function() {
			   $("td").has('input[type="hidden"]').addClass("hidetd");
		  });
	  });
	  document.getElementById("defaultOpen").click();
  });
$(function() {
	$('.submenu').on('shown.bs.collapse', function (e) {
		localStorage.setItem('lastSubMenu', $(this).attr('id'));
	});

	var lastSubMenu = localStorage.getItem('lastSubMenu');
	if (lastSubMenu) {
		$('[id="' + lastSubMenu + '"]').collapse('show');
	}
});
function opentab(evt, tabName) {
	var i, tabcontent, tablinks;
	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
	tabcontent[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
	tablinks[i].className = tablinks[i].className.replace(" active", "");
	}
	document.getElementById(tabName).style.display = "block";
	evt.currentTarget.className += " active";
	}
function notrequired(id)
{
	$('#'+id+'').find(':input').each(function(){
		$(this).prop('required',false)
	})
}

$(function(){
	$('.unique').change(function() {
		var input_list = [];
		var duplicates = [];
		$(".unique").each(function() {
			if($(this).val()!=""){
				input_list.push($.trim($(this).val().toLowerCase()));
			}
		});

		if(input_list.filter){
			duplicates= input_list.filter(function(itm, i){
				return input_list.lastIndexOf(itm)== i && input_list.indexOf(itm)!= i;
			});
		}
		if(duplicates.length>0){
			alert("Duplicate (" + duplicates +")removed!");
			var result = $(this).attr('id').split('-');
			$('#id_attendancedetail_set-'+result[1]+'-employee_no').val('');
			$('#id_attendancedetail_set-'+result[1]+'-employee_name').val('');
			$('#id_attendancedetail_set-'+result[1]+'-designation').val('');
			$('#id_attendancedetail_set-'+result[1]+'-total_hours').val('');

			$('#id_saccodeduction_set-'+result[1]+'-employee_no').val('');
			$('#id_saccodeduction_set-'+result[1]+'-employee_name').val('');

			$('#id_directorsfeedetail_set-'+result[1]+'-employee').val('');
			$('#id_directorsfeedetail_set-'+result[1]+'-employee_name').val('');

			$('#id_lunchdeduction_set-'+result[1]+'-employee_no').val('');
			$('#id_lunchdeduction_set-'+result[1]+'-employee_name').val('');

			$('#id_casualattendancedetail_set-'+result[1]+'-casual_employee_no').val('');
			$('#id_casualattendancedetail_set-'+result[1]+'-employee_name').val('');
			$('#id_casualattendancedetail_set-'+result[1]+'-designation').val('');
			$('#id_casualattendancedetail_set-'+result[1]+'-total_hours').val('');
			}
		else{
			$('input[name="add"]').prop("disabled", false);
			$('input[name="update"]').prop("disabled", false);
			$('input[name="copy"]').prop("disabled", false);
			$(".alert-danger").text("");
			$(".alert-danger").hide();
		}
	  });
	});
