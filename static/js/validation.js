
    "use strict";

    // Focus input
    var inputElements = document.querySelectorAll('.input100');
    inputElements.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (input.value.trim() !== "") {
                input.classList.add('has-val');
            } else {
                input.classList.remove('has-val');
            }
        });
    });

    // Validate
    var form = document.querySelector('.validate-form');
    form.addEventListener('submit', function(event) {
        var inputs = document.querySelectorAll('.validate-input .input100');
        var check = true;

        inputs.forEach(function(input) {
            if (!validate(input)) {
                showValidate(input);
                check = false;
            }
        });

        if (!check) {
            event.preventDefault(); // Prevent form submission if validation fails
        }
    });

    var inputElements = document.querySelectorAll('.validate-form .input100');
    inputElements.forEach(function(input) {
        input.addEventListener('focus', function() {
            hideValidate(input);
        });
    });

    function validate(input) {
        if (input.type === 'email' || input.name === 'email') {
            if (!input.value.trim().match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$/)) {
                return false;
            }
        } else {
            if (input.value.trim() === '') {
                return false;
            }
        }
        return true;
    }

    function showValidate(input) {
        var thisAlert = input.parentElement;
        thisAlert.classList.add('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = input.parentElement;
        thisAlert.classList.remove('alert-validate');
    }

    // Show password
    var showPass = 0;
    var btnShowPass = document.querySelector('.btn-show-pass');
    btnShowPass.addEventListener('click', function() {
        var passwordInput = this.nextElementSibling;
        if (showPass === 0) {
            passwordInput.type = 'text';
            this.classList.add('active');
            showPass = 1;
        } else {
            passwordInput.type = 'password';
            this.classList.remove('active');
            showPass = 0;
        }
    });

