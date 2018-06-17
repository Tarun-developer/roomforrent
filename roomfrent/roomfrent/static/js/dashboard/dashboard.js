jQuery(document).ready(function() {

    jQuery('#location').click(function() {
        var ip_location = jQuery('#ip_location').val();
        // $('.search_input').attr('value', '');
        $('.search_input').val('');
        $('.search_input').val(ip_location);
    });
});

function initAutocomplete() {
    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

    });
}

