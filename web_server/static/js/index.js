$('#threshold_form').submit(function(event){
    event.preventDefault(); 
    var btn = document.getElementById("btn_submit");
    btn.setAttribute('disabled', '');
    var url = '/set_threshold';
    $.ajax({
        url: url,
        type: 'post',
        data: $('#threshold_form').serialize(),
        success: function(data){
            btn.removeAttribute('disabled');
            document.getElementById("current_threshold").innerHTML = data["threshold"];
        }
    });
});

$('#recording_time_form').submit(function(event){
    event.preventDefault(); 
    var btn = document.getElementById("btn_submit");
    btn.setAttribute('disabled', '');
    var url = '/set_recording_time';
    $.ajax({
        url: url,
        type: 'post',
        data: $('#recording_time_form').serialize(),
        success: function(data){
            btn.removeAttribute('disabled');
            document.getElementById("current_recording_time").innerHTML = data["recording_time"];
        }
    });
});

function trash(file,self){
    filename=file.split("/")[1]
    if (confirm("Êtes-vous sûrs de vouloir supprimer le fichier '"+filename+"' ?")) {
        var url = '/remove_file';
        $.ajax({
            url: url,
            type: 'post',
            data: {filename:filename},
            success: function(data){
                if(data){
                    self.parentNode.remove()
                }
            }
        });
    } 
}