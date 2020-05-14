$('#message-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_message();
    console.log($('#message-text').val())
});


var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


function create_message() {
    console.log("create post is working!") // sanity check
    $.ajax({
        url : 'create_message/',
        type : 'POST',
        data : {the_message : $('#message-text').val()},
        success : function(json) {
            $('#message-text').val('');
            console.log(json);
            $("#talk").prepend("<div class=\"date\"">+json.created+"</div> <p><a href=\"\">"+json.author+"</a>: "+json.created+"</p>");
            console.log("success");
            location.reload();
        },
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! error: "+errmsg+" <a href='#' class='close'>&times;</a></div>");
            console.log(xhr.status + ": " + xhr.responseText);
        }
    });
};