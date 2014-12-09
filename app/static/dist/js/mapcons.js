		L.mapbox.accessToken = 'pk.eyJ1IjoidmFyZ2ZyYW4iLCJhIjoiRW44bEMyQSJ9.i3kosn_djpsoR6Qy4TO0Vw#15';
		var southWest = L.latLng(55.874962, -3.404167),
		    northEast = L.latLng(55.988625, -3.096550),
		    bounds = L.latLngBounds(southWest, northEast);
		var map = L.mapbox.map('map', 'vargfran.b9bd48fd', {
    maxBounds: bounds,
    maxZoom: 19,
    minZoom: 10
})
		    .setView([ 55.944, -3.192], 15);
    var featureGroup = L.featureGroup().addTo(map);

	var circle_options = {
      color: '#fff',      // Stroke color
      opacity: 1,         // Stroke opacity
      weight: 1,         // Stroke weight
      fillColor: '#F00',  // Fill color
      fillOpacity: 1    // Fill opacity
  };

   //var circle_one = L.circle([ 55.944, -3.192], 20, circle_options).addTo(featureGroup);
    var drawControl = new L.Control.Draw({
    edit: {
      featureGroup: featureGroup
    }
  }).addTo(map);

	map.on('draw:created', function(e) {
	  featureGroup.addLayer(e.layer);
	});

	var popup = L.popup();

	// Parse lat long
	function parseLatLong(latStr){
		var n = latStr.length;
		var outStr = "";
		for(i = 0; i < n; i ++){
			if(!isNaN(latStr[i]) || latStr[i]===',' || latStr[i]==='.'  || latStr[i]==='-' ){
				outStr += latStr[i];
			}
		}
		return outStr;
	};

	// String.format function to be used
	// for address fetching
	String.prototype.format = function() {
    var formatted = this;
    for( var arg in arguments ) {
        formatted = formatted.replace("{" + arg + "}", arguments[arg]);
    }
    return formatted;
    };

    function getAddress(e){
    	var latLong = parseLatLong(e.latlng.toString()).split(",");
    	console.log(latLong);
    	var api_call = "http://nominatim.openstreetmap.org/reverse?format=json&lat={0}&lon={1}&zoom=18&addressdetails=1"
    	var url = api_call.format(latLong[0],latLong[1]);
    	console.log(url);
    	jQuery.getJSON(url).done([function(data){
    			var address = data["display_name"];
					$.ajax({
							type: 'POST',
							url: '/path',
							data: {'lat' : latLong[0],
										'long': latLong[1],
										'addr': address}
							});
    			popup
			.setLatLng(e.latlng)
			.setContent(address)
			.openOn(map);

    			}]);
    }

	map.on('click', getAddress);
