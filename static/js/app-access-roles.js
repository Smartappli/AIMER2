/**
 * App user list
 */

'use strict';

// Datatable (jquery)
$(function () {
  var dtUserTable = $('.datatables-users'),
    dt_User,
    statusObj = {
      1: { title: 'Pending', class: 'bg-label-warning' },
      2: { title: 'Active', class: 'bg-label-success' },
      3: { title: 'Inactive', class: 'bg-label-secondary' }
    };

  var userView = '/app/user/view/account/';

  // Users List datatable
  if (dtUserTable.length) {
    dt_User = dtUserTable.DataTable({
      ajax: assetsPath + 'json/user-list.json', // JSON file to add data
      columns: [
        // columns according to JSON
        { data: 'id' },
        { data: 'id' },
        { data: 'full_name' },
        { data: 'role' },
        { data: 'current_plan' },
        { data: 'billing' },
        { data: 'status' },
        { data: '' }
      ],
      columnDefs: [
        {
          // For Responsive
          className: 'control',
          orderable: false,
          searchable: false,
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
          checkboxes: {
            selectAllRender: '<input type="checkbox" class="form-check-input">'
          },
          render: function () {
            return '<input type="checkbox" class="dt-checkboxes form-check-input" >';
          },
          searchable: false
        },
        {
          // User full name and email
          targets: 2,
          responsivePriority: 4,
          render: function (data, type, full, meta) {
            var $name = full['full_name'],
              $email = full['email'],
              $image = full['avatar'];
            if ($image) {
              // For Avatar image
              var $output =
                '<img src="' + assetsPath + 'img/avatars/' + $image + '" alt="Avatar" class="rounded-circle">';
            } else {
              // For Avatar badge
              var stateNum = Math.floor(Math.random() * 6) + 1;
              var states = ['success', 'danger', 'warning', 'info', 'dark', 'primary', 'secondary'];
              var $state = states[stateNum],
                $name = full['full_name'],
                $initials = $name.match(/\b\w/g) || [];
              $initials = (($initials.shift() || '') + ($initials.pop() || '')).toUpperCase();
              $output = '<span class="avatar-initial rounded-circle bg-label-' + $state + '">' + $initials + '</span>';
            }
            // Creates full output for row
            var $row_output =
              '<div class="d-flex justify-content-left align-items-center">' +
              '<div class="avatar-wrapper">' +
              '<div class="avatar avatar-sm me-4">' +
              $output +
              '</div>' +
              '</div>' +
              '<div class="d-flex flex-column">' +
              '<a href="' +
              userView +
              '" class="text-heading text-truncate"><span class="fw-medium">' +
              $name +
              '</span></a>' +
              '<small>@' +
              $email +
              '</small>' +
              '</div>' +
              '</div>';
            return $row_output;
          }
        },
        {
          // User Role
          targets: 3,
          render: function (data, type, full, meta) {
            var $role = full['role'];
            var roleBadgeObj = {
              Subscriber: '<i class="bx bx-crown text-primary me-2"></i>',
              Author: '<i class="bx bx-edit text-warning me-2"></i>',
              Maintainer: '<i class="bx bx-user text-success me-2"></i>',
              Editor: '<i class="bx bx-pie-chart-alt text-info me-2"></i>',
              Admin: '<i class="bx bx-desktop text-danger me-2"></i>'
            };
            return (
              "<span class='text-truncate d-flex align-items-center text-heading'>" +
              roleBadgeObj[$role] +
              $role +
              '</span>'
            );
          }
        },
        {
          // Plans
          targets: 4,
          render: function (data, type, full, meta) {
            var $plan = full['current_plan'];

            return '<span class="text-heading">' + $plan + '</span>';
          }
        },
        {
          // User Status
          targets: 6,
          render: function (data, type, full, meta) {
            var $status = full['status'];

            return (
              '<span class="badge ' +
              statusObj[$status].class +
              '" text-capitalized>' +
              statusObj[$status].title +
              '</span>'
            );
          }
        },
        {
          // Actions
          targets: -1,
          title: 'Actions',
          searchable: false,
          orderable: false,
          render: function (data, type, full, meta) {
            return (
              '<div class="d-flex align-items-center">' +
              '<a href="javascript:;" class="btn btn-icon delete-record"><i class="bx bx-trash bx-md"></i></a>' +
              '<a href="' +
              userView +
              '" class="btn btn-icon"><i class="bx bx-show bx-md"></i></a>' +
              '<a href="javascript:;" class="btn btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="bx bx-dots-vertical-rounded bx-md"></i></a>' +
              '<div class="dropdown-menu dropdown-menu-end m-0">' +
              '<a href="javascript:;" class="dropdown-item">Edit</a>' +
              '<a href="javascript:;" class="dropdown-item">Suspend</a>' +
              '</div>' +
              '</div>'
            );
          }
        }
      ],
      order: [[2, 'desc']],
      dom:
        '<"row"' +
        '<"col-sm-12 col-md-4 col-lg-6" l>' +
        '<"col-sm-12 col-md-8 col-lg-6"<"dt-action-buttons text-xl-end text-lg-start text-md-end text-start d-flex align-items-center justify-content-md-end justify-content-center align-items-center flex-sm-nowrap flex-wrap flex-sm-row flex-column"<"me-4"f><"user_role w-px-200 me-sm-4 mb-6 mb-sm-0"><"user_plan w-px-200 mb-6 mb-sm-0">>>' +
        '>t' +
        '<"row"' +
        '<"col-sm-12 col-md-6"i>' +
        '<"col-sm-12 col-md-6"p>' +
        '>',
      language: {
        sLengthMenu: '_MENU_',
        search: '',
        searchPlaceholder: 'Search User',
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
      },
      initComplete: function () {
        // Adding role filter once table initialized
        this.api()
          .columns(3)
          .every(function () {
            var column = this;
            var select = $(
              '<select id="UserRole" class="form-select text-capitalize"><option value=""> Select Role </option></select>'
            )
              .appendTo('.user_role')
              .on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
              });

            column
              .data()
              .unique()
              .sort()
              .each(function (d, j) {
                select.append('<option value="' + d + '" class="text-capitalize">' + d + '</option>');
              });
          });
        this.api()
          .columns(4)
          .every(function () {
            var column = this;
            var select = $(
              '<select id="Userplan" class="form-select text-capitalize"><option value=""> Select Plan </option></select>'
            )
              .appendTo('.user_plan')
              .on('change', function () {
                var val = $.fn.dataTable.util.escapeRegex($(this).val());
                column.search(val ? '^' + val + '$' : '', true, false).draw();
              });

            column
              .data()
              .unique()
              .sort()
              .each(function (d, j) {
                select.append('<option value="' + d + '" class="text-capitalize">' + d + '</option>');
              });
          });
      }
    });
  }

  // Delete Record
  $('.datatables-users tbody').on('click', '.delete-record', function () {
    dt_User.row($(this).parents('tr')).remove().draw();
  });
  // Filter form control to default size
  // ? setTimeout used for multilingual table initialization
  setTimeout(() => {
    $('.dataTables_filter .form-control').removeClass('form-control-sm');
    $('.dataTables_length .form-select').removeClass('form-select-sm');
    $('.dataTables_length .form-select').addClass('mx-0');
    $('.dataTables_length').addClass('mb-0 mb-md-6');
  }, 300);
});

(function () {
  // On edit role click, update text
  var roleEditList = document.querySelectorAll('.role-edit-modal'),
    roleAdd = document.querySelector('.add-new-role'),
    roleTitle = document.querySelector('.role-title');

  roleAdd.onclick = function () {
    roleTitle.innerHTML = 'Add New Role'; // reset text
  };
  if (roleEditList) {
    roleEditList.forEach(function (roleEditEl) {
      roleEditEl.onclick = function () {
        roleTitle.innerHTML = 'Edit Role'; // reset text
      };
    });
  }
})();
