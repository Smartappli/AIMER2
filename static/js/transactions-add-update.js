'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    let fv; // Declare fv in a scope accessible to both initialization and event listeners

    // Variables for DataTable
    var TransactionDate = $('#transaction-date');
    var DueDate = $('#due-date');
    var select2 = $('.select2');

    if (select2.length) {
      select2.each(function () {
        var $this = $(this);
        $this.wrap('<div class="position-relative"></div>').select2({
          placeholder: 'Select Status',
          dropdownParent: $this.parent()
        });

        // Add event listener to clear validation messages on input change
        $this.on('change', function () {
          fv.revalidateField('status');
        });
      });
    }

    // Transaction Date (flatpicker)
    if (TransactionDate) {
      TransactionDate.flatpickr({
        monthSelectorType: 'static',
        dateFormat: 'Y-m-d',
        onClose: function () {
          fv.revalidateField('due_date');
        }
      });
    }

    // DueDate (flatpicker)
    if (DueDate) {
      DueDate.flatpickr({
        monthSelectorType: 'static',
        dateFormat: 'Y-m-d',
        onClose: function () {
          fv.revalidateField('due_date');
        }
      });
    }

    const addTransactionForm = document.getElementById('addTransactionForm');
    if (addTransactionForm) {
      // Add New Customer Form Validation
      fv = FormValidation.formValidation(addTransactionForm, {
        fields: {
          customer: {
            validators: {
              notEmpty: {
                message: 'Please enter Customer Name'
              }
            }
          },
          status: {
            validators: {
              notEmpty: {
                message: 'Please select a Transaction Status'
              }
            }
          },
          total: {
            validators: {
              notEmpty: {
                message: 'Please fill the amount'
              },
              regexp: {
                regexp: /^\d+(\.\d{1,2})?$/,
                message: 'Only 2 digits are allowed after the decimal point'
              }
            }
          },
          due_date: {
            validators: {
              notEmpty: {
                message: 'Please select a Due Date'
              },
              callback: {
                message: 'Due Date should be equal to or later than Transaction Date',
                callback: function (input) {
                  const dueDate = input.value;
                  const transactionDate = TransactionDate.val(); // Use .val() to get the value of jQuery element

                  if (new Date(dueDate) >= new Date(transactionDate)) {
                    return true;
                  }

                  return false;
                }
              }
            }
          },
          transaction_date: {
            validators: {
              notEmpty: {
                message: 'Please select a Transaction Date'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-5'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }

    // Update transaction form validation
    const UpdateTransactionForm = document.getElementById('UpdateTransactionForm');
    if (UpdateTransactionForm) {
      fv = FormValidation.formValidation(UpdateTransactionForm, {
        fields: {
          customer: {
            validators: {
              notEmpty: {
                message: 'Please enter Customer Name'
              }
            }
          },
          status: {
            validators: {
              notEmpty: {
                message: 'Please select a Transaction Status'
              }
            }
          },
          total: {
            validators: {
              notEmpty: {
                message: 'Please fill the amount'
              },
              regexp: {
                regexp: /^\d+(\.\d{1,2})?$/,
                message: 'Only 2 digits are allowed after the decimal point'
              }
            }
          },
          due_date: {
            validators: {
              notEmpty: {
                message: 'Please select a Due Date'
              },
              callback: {
                message: 'Due Date should be equal to or later than Transaction Date',
                callback: function (input) {
                  const dueDate = input.value;
                  const transactionDate = TransactionDate.val(); // Use .val() to get the value of jQuery element

                  if (new Date(dueDate) >= new Date(transactionDate)) {
                    return true;
                  }

                  return false;
                }
              }
            }
          },
          transaction_date: {
            validators: {
              notEmpty: {
                message: 'Please select a Transaction Date'
              }
            }
          }
        },
        plugins: {
          trigger: new FormValidation.plugins.Trigger(),
          bootstrap5: new FormValidation.plugins.Bootstrap5({
            eleValidClass: '',
            rowSelector: '.mb-5'
          }),
          submitButton: new FormValidation.plugins.SubmitButton(),

          defaultSubmit: new FormValidation.plugins.DefaultSubmit(),
          autoFocus: new FormValidation.plugins.AutoFocus()
        },
        init: instance => {
          instance.on('plugins.message.placed', function (e) {
            if (e.element.parentElement.classList.contains('input-group')) {
              e.element.parentElement.insertAdjacentElement('afterend', e.messageElement);
            }
          });
        }
      });
    }
  })();
});
