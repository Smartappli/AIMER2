/**
 *  Pages Click Loader
 */

'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  (function () {
    // From loading state while processing an email sent
    var btnSubmit = document.getElementById('btnSubmit');
    var btnText = document.getElementById('btnText');
    var btnLoader = document.getElementById('btnLoader');
    if (btnSubmit && btnText && btnLoader) {
      // Show loading state
      btnSubmit.addEventListener('click', function () {
        btnSubmit.classList.add('disabled');
        btnText.textContent = 'Sending email... ';
        btnLoader.classList.remove('visually-hidden');
      });
    }
  })();
});
