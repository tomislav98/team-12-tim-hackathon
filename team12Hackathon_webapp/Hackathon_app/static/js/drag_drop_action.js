
+ function($) {
    'use strict';


    // UPLOAD CLASS DEFINITION
    // ======================

    var dropZone = document.getElementById('drop-zone');
    var uploadForm = document.getElementById('js-upload-form');

    var startUpload = function(files) {
        var fd = new FormData();
        var files = files[0];
        fd.append('file',files);
        $.ajax({
            url: '/api/object/detection',
            type: 'post',
            data: fd,
            contentType: false,
            processData: false,
            dataType: 'json',
            success: function(response){
                console.debug(response);
                var detObject = document.getElementById('detectObject');
                detObject.innerHTML = 'Non riconosciuto';
                if (!response){
                    return;
                }
                if (response['match']){
                    // $('#detectObject').innerHTML = 'Non riconosciuto';
                    if (response['typeObject'] === 'street_hole'){
                        detObject.innerHTML = 'Strada dissestata';
                    }
                    $('#first-step-modal').modal('hide');
                //TODO: set id.
                $('#second-step-modal').modal('show');
                console.log(response);
                }

            },
        });
    }

    console.log(uploadForm);
    console.log(dropZone);

    uploadForm.addEventListener('submit', function(e) {
        var uploadFiles = document.getElementById('js-upload-files').files;
        e.preventDefault()

        startUpload(uploadFiles);
    })

    dropZone.ondrop = function(e) {
        e.preventDefault();
        this.className = 'upload-drop-zone';

        startUpload(e.dataTransfer.files);
    }

    dropZone.ondragover = function() {
        this.className = 'upload-drop-zone drop';
        return false;
    }

    dropZone.ondragleave = function() {
        this.className = 'upload-drop-zone';
        return false;
    }

}(jQuery);
