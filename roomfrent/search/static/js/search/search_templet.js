 $(document).ready(function() {
     $(".alert").hide();
     var input_value = document.getElementById('search_value').value;
     $('#pac-input').val(input_value);

     $("#search").click(function() {
         if (document.getElementById('pac-input').value == '') {
             alert('missing address');
             return
         }
         $("#loader").show();
         $('.clone_html_properity').remove();
         // event.preventDefault();
         var csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value;
         $.ajax({
             type: "POST",
             url: "/dashboard/search_results/",
             data: {
                 'search_query': $('#pac-input').val(),
                 'csrfmiddlewaretoken': csrf // from form
             },
             success: function(responce) {
                 $("#loader").hide();
                 var i;
                 for (i = 0; i < responce.length; ++i) {
                     var title = responce[i]['name']
                     var distance_float = responce[i]['distance'];
                     var distance = Math.round(parseFloat((distance_float * Math.pow(10, 2)).toFixed(2))) / Math.pow(10, 2);
                     var search_location = $('#pac-input').val();
                     var search_locationresult = search_location.substring(0,15);
                     var image_url = responce[i]['image'];
                     var budget = responce[i]['budget'];
                     var location = responce[i]['location'];
                     var owner = responce[i]['owner'];
                     var owner_mob = responce[i]['owner_mob'];


                     $('.heading_result').text('Rooms for rent near ' + $('#pac-input').val());
                     var image_len = (image_url.match(new RegExp(",", "g")) || []).length;
                     if (image_len > 1) {
                         // for(i = 0; i < image_len; i++) { 
                         var arr = image_url.split(',')[0];
                         // }
                     } else {
                         var arr = responce[i]['image'];
                     }

                     var clone = $('#proerity_script').clone().html();
                     var this_div_index = parseInt($(".clone_html_properity").length) + 1;
                     var this_div_id = "clone_html_properity_" + this_div_index;
                     $("#append_properity").append(clone);
                     $(".clone_html_properity:last").attr('id', this_div_id);
                     $("#" + this_div_id).find('.property_title').text(title);
                     $("#" + this_div_id).find('.budget').text("₹" + budget);
                     $("#" + this_div_id).find('.owner').text("By Owner " + owner);
                     $("#" + this_div_id).find('.owner_mobile').text("Mob: " + owner_mob);



                     $("#" + this_div_id).find('.location').text(location + " " + distance + " km from " + search_locationresult);
                     // $("#" + this_div_id).find('.distance').text(distance + " km from " + $('#pac-input').val());
                     if (arr != 'None') {
                         $("#" + this_div_id).find('.pro_image').attr('src', arr);
                     }
                 }

             },
             error: function(xhr, ajaxOptions, thrownError) {
                 $("#loader").hide();
                 $(".alert").show();
                 $('.alert').alert('close')
                 $('.alert').html(thrownError);

             }

         });
         return false;
     });



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
     var search = getUrlParameter('search');
     if (search === '') {
         window.location.replace("/dashboard");
     } else {
         $('#search').trigger('click');
     }

 });