
$(function () {

	$("#id_resources_category_in_left_nav_bar").addClass("active show");
	$("#id_video_call_service_accounts_in_left_nav_bar").addClass("active");

	$("#id_btn_delete_service_account").popover({
		placement: 'top',
		trigger: 'click',
		html: true,
		sanitize: false,
		content:
			`<div id="id_popover_service_account_delete">
				<div class="tx-14 mg-b-10">Are you sure you want to delete this video call service account?</div>
				<button id="id_btn_confirm_delete_service_account" type="button" class="btn btn-sm btn-uppercase btn-danger mg-r-5" onclick="deleteServiceAccount()">Yes</button>
				<button type="button" class="btn btn-sm btn-uppercase btn-white" onclick="$('#id_btn_delete_service_account').popover('hide');">Cancel</button>
			</div>`
	});

	$("#id_cohort").on("select2:selecting", function (e) {
		$("#id_parsley_cohort_errors").html("");
	}).select2({
		placeholder: "Search Cohort",
		allowClear: true
	});

	$("#id_video_call_service").on("select2:selecting", function (e) {
		$("#id_video_call_service_errors").html("");
	}).select2({
		placeholder: "Search Account Type",
		minimumResultsForSearch: Infinity,
	});

	$("#id_form_video_call_service_account_details").parsley({ successClass: "" })
		.on('form:submit', function (formInstance) {
			$("#id_btn_video_call_service_account_save").attr("disabled", true).html(
				'<span class="spinner-border spinner-border-sm mg-r-5" role="status" aria-hidden="true"></span> Saving'
			);
			var name = $("#id_name").val(),
				email = $("#id_email").val(),
				external_account_id = $("#id_external_account_id").val(),
				video_call_service = $("#id_video_call_service").val(),
				cohort = $("#id_cohort").val();


			if (id == null) {
				var request_type = "POST";
				var request_url = createURL;
			} else {
				var request_type = "PATCH";
				var request_url = updateURL;
			}
			$.ajax({
				type: request_type,
				url: request_url,
				beforeSend: function (request) {
					request.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
				},
				data: JSON.stringify({
					"name": name,
					"email": email,
					"external_account_id": external_account_id,
					"video_call_service": video_call_service,
					"cohort": cohort,
				}),
				contentType: 'application/json',
				processData: false,
				dataType: 'json'
			}).done(function (data) {
				//Go back to list page
				window.location.href = listURL;
			}).fail(function (data){
				$("#id_btn_video_call_service_account_save").removeAttr('disabled').html("<i data-feather=\"save\"></i> Save");
				$.each(data.responseJSON, function (fieldName, errorBag) {
					var errorsDivId = "#id_" + fieldName + "_errors";
					var htmlToInsert = "";
					// output each error message for this field
					$.each(errorBag, function(i, error) {
						htmlToInsert += '<li>* ' + error + '</li>';
					});
					$(errorsDivId).html(htmlToInsert);
				});
			});

			return false;

		});
});

function deleteServiceAccount() {
	var request_url = updateURL;
	var request_type = "DELETE";

	$("#id_btn_confirm_delete_service_account").attr('disabled', true).html('<div class="spinner-border spinner-border-sm spinner-border-thin mg-r-5" role="status"></div> Please wait..');

	$.ajax({
		type: request_type,
		url: request_url,
		beforeSend: function (request) {
			request.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
		},
		contentType: 'application/json',
		processData: false,
		dataType: 'json'
	}).done(function (response) {
		if (response) {
			$("#id_popover_service_account_delete").html(
				`<div class="tx-14 d-flex">
					<i class="fa fa-check-circle tx-success mg-t-5"></i> <div class="flex-grow-1 pd-l-5">This Service Account is deleted successfully. Redirecting back..</div>
				</div>`
			);
			window.dispatchEvent(new Event('resize'));
			window.location.href = listURL;
		} else {
			$("#id_modal_service_account_delete_not_possible").modal('show');
		}
	});
}