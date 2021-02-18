var jobsTableObj;

$(function () {
  'use strict';


  jobsTableObj = $('#id_tbl_service_accounts').DataTable({
    ajax: {
      url: getUrl,
      dataSrc: function (data) {
        console.log(data);
        return data['results'];
      },
    },
    dom: "<'row'<'col-md-8 col-xl-9'><'col-md-4 col-xl-3 mb-3'f>>rtip",
    initComplete: function () {
      feather.replace();
    },
    stripeClasses: [],
    responsive: true,
    lengthChange: false,
    ordering: true,
    aaSorting: [],
    language: {
      searchPlaceholder: 'Search..',
      sSearch: '',
    },
    "columnDefs": [
      { "width": "170px", "targets": 3 },
    ],
    columns: [
      {
        data: 'name',
        title: 'Name',
        className: 'align-text-center',
        render: function (data, type, full, meta) {
          return getLinkForUpdating(full.id, full.name);
        }

      },
      {
        data: 'email',
        title: 'Email',
        className: 'text-nowrap align-text-center',
      },
      {
        data: 'video_call_service',
        title: 'Account Type',
        className: 'align-text-center',
      },
      {
        data: 'cohort_name',
        title: 'Cohort',
        className: 'align-text-center',
      }
    ],
  });


});
