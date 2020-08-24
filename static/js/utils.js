function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function doAjaxSetup() {
    const csrftoken = Cookies.get('csrftoken');
    // Ensure jQuery AJAX calls set the CSRF header to prevent security errors
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}

function showMessage(messageType, message) {
    let alert = $("<div>").addClass("alert")
                        .addClass("alert-" + messageType);
    alert.append($("<span>").text(message));
    let container = $("#message-container");
    container.empty().append(alert).show();
    setTimeout(function (){container.hide();}, 3000);
}