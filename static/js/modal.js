document.addEventListener('DOMContentLoaded', function () {
    // var saveButtons = document.querySelectorAll('.save-btn');
    
    // saveButtons.forEach(function(button) {
    //     button.addEventListener('click', function(event) {
    //         var modal = bootstrap.Modal.getInstance(button.closest('.modal'));
    //         modal.hide();
    //     });
    // });
    var modals = document.querySelectorAll('.modal');

    modals.forEach(function (modal) {
      modal.addEventListener('shown.bs.modal', function () {
        var firstInput = modal.querySelector('input, select, textarea');
        if (firstInput) {
          firstInput.focus();
        }
      });
    });
  });