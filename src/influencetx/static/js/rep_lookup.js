var MAPS_API = "https://maps.google.com/maps/api/js?libraries=places";
var INFO_API = 'https://www.googleapis.com/civicinfo/v2/representatives';
var API_KEY = 'AIzaSyDWV3t6w5_eYmyrtkpXcpbwWoGkAUFnYYw';
var address, divisions, data;

function addressSearch(address) {
    var params = {
        'key': API_KEY,
        'address': address,
        'includeOffices': false
    }
    var roles =[
        // 'headOfState',
        // 'headOfGovernment',
        // 'deputyHeadOfGovernment',
        'legislatorUpperBody',
        'legislatorLowerBody',
        // 'highestCourtJudge',
        // 'judge'
        // 'governmentOfficer',
        // 'schoolBoard',
        // 'specialPurposeOfficer',
    ]
    var roles_mapped = roles.map(function(x){ return 'roles='+x}).join('&');
    var queryString = '?'+$.param(params)+'&'+roles_mapped;
    // console.log(queryString);
    var findreps_url;

    $.getJSON(INFO_API+queryString, function(data, status)
    {
        if (status == 'success') {
            divisions = data['divisions'];
            // Split division data for state to get district numbers.
            var districts = getDistricts(divisions);
            var senate_district = districts['sldu']
            var house_district = districts['sldl']
            if (senate_district === undefined || senate_district === null) {
                 senate_district = 0
            }
            if (house_district === undefined || house_district === null) {
                 house_district = 0
            }
            // console.log(location.origin);
            // console.log(senate_district, house_district);
            findreps_url = location.origin + '/legislators/findreps/' + senate_district + ',' + house_district
            // Do url call to django url with district numbers.
            location.assign(findreps_url)
      }
    })

}

$(document).ready(function($) {
    var autocomplete = new google.maps.places.Autocomplete(document.getElementById('address'), { types: ['address'] });
    // console.log(autocomplete);
    autocomplete.addListener('place_changed', function() {
        var place = autocomplete.getPlace();
        address = place.formatted_address;
        console.log(address);
    })

    // console.log(address);

    $('#address-search').click(function() {
        if (address != '')
            console.log(address);
            addressSearch(address);
    });
});

function getDistricts(divisions) {
    var district_tags = {}
    for (var division in divisions) {
        var district_tag = division.split("/");
        district_tag = district_tag[district_tag.length - 1];
        district_tag = district_tag.split(":");
        district_tags[district_tag[0]] = district_tag[1];
    }
    return district_tags;
}
