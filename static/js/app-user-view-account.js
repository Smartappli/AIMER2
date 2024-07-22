/**
 * App User View - Account (jquery)
 */

$(function () {
  'use strict';

  // Variable declaration for table
  var dt_project_table = $('.datatable-project'),
    dt_invoice_table = $('.datatable-invoice');

  // Project datatable
  // --------------------------------------------------------------------
  if (dt_project_table.length) {
    var dt_project = dt_project_table.DataTable({
      ajax: assetsPath + 'json/user-profile.json',
      columns: [
        { data: '' },
        { data: 'id' },
        { data: 'project_name' },
        { data: 'project_leader' },
        { data: '' },
        { data: 'status' },
        { data: '' }
      ],
      columnDefs: [
        {
          // For Responsive
          className: 'control',
          searchable: false,
          orderable: false,
          responsivePriority: 2,
          targets: 0,
          render: function (data, type, full, meta) {
            return '';
          }
        },
        {
          // For Checkboxes
          targets: 1,
          orderable: false,
          searchable: false,
          responsivePriority: 3,
          checkboxes: true,
          render: function () {
            return '<input type="checkbox" class="dt-checkboxes form-check-input">';
          },
          checkboxes: {
            selectAllRender: '<input type="checkbox" class="form-check-input">'
          }
        },
        {
          // Avatar image/badge, Name and post
          targets: 2,
          responsivePriority: 4,
          render: function (data, type, full, meta) {
            var $user_img = full['project_img'],
              $name = full['project_name'],
              $date = full['date'];
            if ($user_img) {
              // For Avatar image
              var $output =
                '<img src="' + assetsPath + 'img/icons/brands/' + $user_img + '" alt="Avatar" class="rounded-circle">';
            } else {
              // For Avatar badge
              var stateNum = Math.floor(Math.random() * 6);
              var states = ['success', 'danger', 'warning', 'info', 'primary', 'secondary'];
              var $state = states[stateNum],
                $name = full['project_name'],
                $initials = $name.match(/\b\w/g) || [];
              $initials = (($initials.shift() || '') + ($initials.pop() || '')).toUpperCase();
              $output = '<span class="avatar-initial rounded-circle bg-label-' + $state + '">' + $initials + '</span>';
            }
            // Creates full output for row
            var $row_output =
              '<div class="d-flex justify-content-left align-items-center">' +
              '<div class="avatar-wrapper">' +
              '<div class="avatar avatar-sm me-3">' +
              $output +
              '</div>' +
              '</div>' +
              '<div class="d-flex flex-column gap-50">' +
              '<span class="text-truncate fw-medium text-heading">' +
              $name +
              '</span>' +
              '<small class="text-truncate">' +
              $date +
              '</small>' +
              '</div>' +
              '</div>';
            return $row_output;
          }
        },
        {
          // Task
          targets: 3,
          render: function (data, type, full, meta) {
            var $task = full['project_leader'];
            return '<span class="text-heading">' + $task + '</span>';
          }
        },
        {
          // Teams
          targets: 4,
          orderable: false,
          searchable: false,
          render: function (data, type, full, meta) {
            var $team = full['team'],
              $team_item = '',
              $team_count = 0;
            for (var i = 0; i < $team.length; i++) {
              $team_item +=
                '<li data-bs-toggle="tooltip" data-popup="tooltip-custom" data-bs-placement="top" title="Kim Karlos" class="avatar avatar-xs pull-up">' +
                '<img class="rounded-circle" src="' +
                assetsPath +
                'img/avatars/' +
                $team[i] +
                '"  alt="Avatar">' +
                '</li>';
              $team_count++;
              if ($team_count > 2) break;
            }
            if ($team_count > 2) {
              var $remainingAvatars = $team.length - 3;
              if ($remainingAvatars > 0) {
                $team_item +=
                  '<li class="avatar avatar-xs">' +
                  '<span class="avatar-initial rounded-circle pull-up text-heading" data-bs-toggle="tooltip" data-bs-placement="top" title="' +
                  $remainingAvatars +
                  ' more">+' +
                  $remainingAvatars +
                  '</span >' +
                  '</li>';
              }
            }
            var $team_output =
              '<div class="d-flex align-items-center">' +
              '<ul class="list-unstyled d-flex align-items-center avatar-group mb-0 z-2">' +
              $team_item +
              '</ul>' +
              '</div>';
            return $team_output;
          }
        },
        {
          // Label
          targets: -2,
          render: function (data, type, full, meta) {
            var $status_number = full['status'];
            return (
              '<div class="d-flex align-items-center">' +
              '<div class="progress w-100 me-3" style="height: 6px;">' +
              '<div class="progress-bar" style="width: ' +
              $status_number +
              '" aria-valuenow="' +
              $status_number +
              '" aria-valuemin="0" aria-valuemax="100"></div>' +
              '</div>' +
              '<span class="text-heading">' +
              $status_number +
              '</span></div>'
            );
          }
        },
        {
          // Actions
          targets: -1,
          searchable: false,
          title: 'Action',
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-inline-block">' +
              '<a href="javascript:;" class="btn btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="bx bx-dots-vertical-rounded bx-md"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="javascript:;" class="dropdown-item">Details</a>' +
              '<a href="javascript:;" class="dropdown-item">Archive</a>' +
              '<div class="dropdown-divider"></div>' +
              '<a href="javascript:;" class="dropdown-item text-danger delete-record">Delete</a>' +
              '</div>' +
              '</div>'
            );
          }
        }
      ],
      order: [[2, 'desc']],
      dom:
        '<"d-flex justify-content-between align-items-center flex-column flex-sm-row mx-6 row"' +
        '<"col-sm-4 col-12 d-flex align-items-center justify-content-sm-start justify-content-center"l>' +
        '<"col-sm-8 col-12 d-flex align-items-center justify-content-sm-end justify-content-center mt-sm-0 mt-n6"f>' +
        '>t' +
        '<"d-flex justify-content-between mx-6 row"' +
        '<"col-sm-12 col-md-6"i>' +
        '<"col-sm-12 col-md-6"p>' +
        '>',
      displayLength: 7,
      lengthMenu: [7, 10, 25, 50, 75, 100],
      language: {
        sLengthMenu: '_MENU_',
        search: '',
        searchPlaceholder: 'Search Project',
        paginate: {
          next: '<i class="bx bx-chevron-right bx-18px"></i>',
          previous: '<i class="bx bx-chevron-left bx-18px"></i>'
        }
      },
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
              return 'Details of "' + data['project_name'] + '" Project';
            }
          }),
          type: 'column',
          renderer: function (api, rowIdx, columns) {
            var data = $.map(columns, function (col, i) {
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                    col.rowIndex +
                    '" data-dt-column="' +
                    col.columnIndex +
                    '">' +
                    '<td>' +
                    col.title +
                    ':' +
                    '</td> ' +
                    '<td>' +
                    col.data +
                    '</td>' +
                    '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/><tbody />').append(data) : false;
          }
        }
      }
    });
    // Delete Record
    $('.datatable-project tbody').on('click', '.delete-record', function () {
      dt_project.row($(this).parents('tr')).remove().draw();
    });
  }

  // Invoice datatable
  // --------------------------------------------------------------------
  if (dt_invoice_table.length) {
    var dt_invoice = dt_invoice_table.DataTable({
      ajax: assetsPath + 'json/invoice-list.json', // JSON file to add data
      columns: [
        // columns according to JSON
        { data: '' },
        { data: 'invoice_id' },
        { data: 'invoice_status' },
        { data: 'total' },
        { data: 'issued_date' },
        { data: 'action' }
      ],
      columnDefs: [
        {
          // For Responsive
          className: 'control',
          responsivePriority: 2,
          targets: 0,
          render: function (data, type, full, meta) {
            return '';
          }
        },
        {
          // Invoice ID
          targets: 1,
          render: function (data, type, full, meta) {
            var $invoice_id = full['invoice_id'];
            // Creates full output for row
            var $row_output = '<a href="/app/invoice/preview/"><span>#' + $invoice_id + '</span></a>';
            return $row_output;
          }
        },
        {
          // Invoice status
          targets: 2,
          render: function (data, type, full, meta) {
            var $invoice_status = full['invoice_status'],
              $due_date = full['due_date'],
              $balance = full['balance'];
            var roleBadgeObj = {
              Sent: '<span class="badge badge-center d-flex align-items-center justify-content-center rounded-pill bg-label-success w-px-30 h-px-30"><i class="bx bx-check bx-xs"></i></span>',
              Draft:
                '<span class="badge badge-center d-flex align-items-center justify-content-center rounded-pill bg-label-primary w-px-30 h-px-30"><i class="bx bx-folder bx-xs"></i></span>',
              'Past Due':
                '<span class="badge badge-center d-flex align-items-center justify-content-center rounded-pill bg-label-danger w-px-30 h-px-30"><i class="bx bx-error bx-xs"></i></span>',
              'Partial Payment':
                '<span class="badge badge-center d-flex align-items-center justify-content-center rounded-pill bg-label-secondary w-px-30 h-px-30"><i class="bx bx-envelope bx-xs"></i></span>',
              Paid: '<span class="badge badge-center d-flex align-items-center justify-content-center rounded-pill bg-label-warning w-px-30 h-px-30"><i class="bx bx-pie-chart-alt bx-xs"></i></span>',
              Downloaded:
                '<span class="badge badge-center d-flex align-items-center justify-content-center rounded-pill bg-label-info w-px-30 h-px-30"><i class="bx bx-down-arrow-alt bx-xs"></i></span>'
            };
            return (
              "<span class='d-inline-block' data-bs-toggle='tooltip' data-bs-html='true' title='<span>" +
              $invoice_status +
              '<br> <span class="fw-medium">Balance:</span> ' +
              $balance +
              '<br> <span class="fw-medium">Due Date:</span> ' +
              $due_date +
              "</span>'>" +
              roleBadgeObj[$invoice_status] +
              '</span>'
            );
          }
        },
        {
          // Total Invoice Amount
          targets: 3,
          render: function (data, type, full, meta) {
            var $total = full['total'];
            return '$' + $total;
          }
        },
        {
          // Actions
          targets: -1,
          title: 'Actions',
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-flex align-items-center">' +
              '<a href="javascript:;" class="btn btn-icon delete-record"><i class="bx bx-trash bx-md"></i></a>' +
              '<a href="/app/invoice/preview/" class="btn btn-icon" data-bs-toggle="tooltip" title="Preview"><i class="bx bx-show bx-md"></i></a>' +
              '<div class="d-inline-block">' +
              '<a href="javascript:;" class="btn btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="bx bx-dots-vertical-rounded bx-md"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="javascript:;" class="dropdown-item">Download</a>' +
              '<a href="/app/invoice/edit/" class="dropdown-item">Edit</a>' +
              '<a href="javascript:;" class="dropdown-item">Duplicate</a>' +
              '</div>' +
              '</div>'
            );
          }
        }
      ],
      order: [[1, 'desc']],
      dom:
        '<"row mx-6"' +
        '<"col-sm-6 col-12 d-flex align-items-center justify-content-center justify-content-sm-start mt-6 mt-sm-0"<"head-label">>' +
        '<"col-sm-6 col-12 d-flex justify-content-center justify-content-md-end align-items-baseline"<"dt-action-buttons d-flex justify-content-center flex-md-row align-items-baseline gap-4"lB>>' +
        '>t' +
        '<"row mx-6"' +
        '<"col-sm-12 col-xxl-6 text-center text-xxl-start pb-md-2 pb-xxl-0"i>' +
        '<"col-sm-12 col-xxl-6 d-md-flex justify-content-xxl-end justify-content-center"p>' +
        '>',
      language: {
        sLengthMenu: '_MENU_',
        search: '',
        searchPlaceholder: 'Search Invoice',
        paginate: {
          next: '<i class="bx bx-chevron-right bx-18px"></i>',
          previous: '<i class="bx bx-chevron-left bx-18px"></i>'
        }
      },
      // Buttons with Dropdown
      buttons: [
        {
          extend: 'collection',
          className: 'btn btn-label-secondary dropdown-toggle float-sm-end mb-3 mb-sm-0',
          text: '<i class="bx bx-export bx-sm me-2"></i>Export',
          buttons: [
            {
              extend: 'print',
              text: '<i class="bx bx-printer me-2" ></i>Print',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'csv',
              text: '<i class="bx bx-file me-2" ></i>Csv',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'excel',
              text: '<i class="bx bxs-file-export me-2"></i>Excel',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'pdf',
              text: '<i class="bx bxs-file-pdf me-2"></i>Pdf',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            },
            {
              extend: 'copy',
              text: '<i class="bx bx-copy me-2" ></i>Copy',
              className: 'dropdown-item',
              exportOptions: { columns: [1, 2, 3, 4] }
            }
          ]
        }
      ],
      // For responsive popup
      responsive: {
        details: {
          display: $.fn.dataTable.Responsive.display.modal({
            header: function (row) {
              var data = row.data();
              return 'Details of ' + data['full_name'];
            }
          }),
          type: 'column',
          renderer: function (api, rowIdx, columns) {
            var data = $.map(columns, function (col, i) {
              return col.title !== '' // ? Do not show row in modal popup if title is blank (for check box)
                ? '<tr data-dt-row="' +
                    col.rowIndex +
                    '" data-dt-column="' +
                    col.columnIndex +
                    '">' +
                    '<td>' +
                    col.title +
                    ':' +
                    '</td> ' +
                    '<td>' +
                    col.data +
                    '</td>' +
                    '</tr>'
                : '';
            }).join('');

            return data ? $('<table class="table"/><tbody />').append(data) : false;
          }
        }
      }
    });
    $('div.head-label').html('<h5 class="card-title mb-0">Invoice List</h5>');
    $('.dataTables_length .form-select').addClass('mx-0');
  }
  // On each datatable draw, initialize tooltip
  dt_invoice_table.on('draw.dt', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl, {
        boundary: document.body
      });
    });
  });

  // Delete Record
  $('.datatable-invoice tbody').on('click', '.delete-record', function () {
    dt_invoice.row($(this).parents('tr')).remove().draw();
  });
  // Filter form control to default size
  // ? setTimeout used for multilingual table initialization
  setTimeout(() => {
    $('.dataTables_filter .form-control').removeClass('form-control-sm');
    $('.dataTables_length .form-select').removeClass('form-select-sm');
  }, 300);
});
