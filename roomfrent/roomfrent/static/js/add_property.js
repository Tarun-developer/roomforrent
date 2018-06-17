$(document).ready(function() {
    $("#button116").click(function() {
        event.preventDefault();
        var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
       /*
       *form data to array
       */
        var o = {};
        var a = $('form').serializeArray();
        $.each(a, function() {
            if (o[this.name] !== undefined) {
                if (!o[this.name].push) {
                    o[this.name] = [o[this.name]];
                }
                o[this.name].push(this.value || '');
            } else {
                o[this.name] = this.value || '';
            }
        });
        var form_data = JSON.stringify(o);
       
        $.ajax({
            type: "POST",
            url: "/owner/owner_add_property/",
            data: {
                'form_data': form_data,
                'owner_id': getUrlParameter('own'),
                'csrfmiddlewaretoken': csrf // from form
            },
            success: function(responce) {}
        });
    });
    /*
     *Get url paramiter
     *
     */
    var getUrlParameter = function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }
    };
});