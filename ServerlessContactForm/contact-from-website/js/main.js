/*
--------------------------------
Ajax Contact Form
--------------------------------
+ https://github.com/mehedidb/Ajax_Contact_Form
+ A Simple Ajax Contact Form developed in PHP with HTML5 Form validation.
+ Has a fallback in jQuery for browsers that do not support HTML5 form validation.
+ version 1.0.1
+ Copyright 2016 Mehedi Hasan Nahid
+ Licensed under the MIT license
+ https://github.com/mehedidb/Ajax_Contact_Form
*/

(function ($, window, document, undefined) {
    'use strict';

    var $form = $('.validate-form');

    $form.submit(function (e) {
        // remove the error class
        //$('.form-group').removeClass('has-error');
        //$('.help-block').remove();

        // get the form data
        var formData = {
            'name' : $('input[name="name"]').val(),
            'email' : $('input[name="email"]').val(),
            'subject' : $('input[name="subject"]').val(),
            'message' : $('textarea[name="message"]').val()
        };
        console.log(JSON.stringify(formData));

        // process the form
        $.ajax({
            type : 'POST',
            url  : 'https://e36pbmc4g5.execute-api.us-east-1.amazonaws.com/dev/correo',
            data : JSON.stringify(formData),
            dataType : 'json',
            contentType: "application/json",
            beforeSend: function(data) {
                //$('#submit').attr('disabled', true);
                //$('#status').html('<i class="fa fa-refresh fa-spin"></i> Sending Mail...').show();
            }
        }).done(function (data) {
            // Handle
            console.log(data);
            alert("Mensaje Enviado!!");

            // Clean
            $('.validate-form').trigger("reset");
        }).fail(function (data) {
            // for debug
            console.log(data)
            alert("Erro :(");
        });

        e.preventDefault();
    });
}(jQuery, window, document));
