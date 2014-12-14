L.mapbox.accessToken = 'pk.eyJ1IjoidmFyZ2ZyYW4iLCJhIjoiRW44bEMyQSJ9.i3kosn_djpsoR6Qy4TO0Vw#15';
var southWest = L.latLng(55.874962, -3.404167),
    northEast = L.latLng(55.988625, -3.096550),
    bounds = L.latLngBounds(southWest, northEast);
var map = L.mapbox.map('map', 'vargfran.b9bd48fd', {
				    maxBounds: bounds,
				    maxZoom: 19,
				    minZoom: 10
				}).setView([ 55.944, -3.192], 15);
var featureGroup = L.featureGroup().addTo(map);
var clickCount = 0;
var craftPath = false;
var coords = [];
var walk = [];
var linePresance = 0;
var polyline = 0;

var circle_options = {
  color: '#fff',      // Stroke color
  opacity: 1,         // Stroke opacity
  weight: 1,         // Stroke weight
  fillColor: '#F00',  // Fill color
  fillOpacity: 1    // Fill opacity
};

// var circle_one = L.circle([ 55.944, -3.192], 20, circle_options).addTo(featureGroup);
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
	// var bol =  {{ path_bool }} ;
	// console.log(bol);
	// console.log(p);
	var bol = $.parseJSON(p[0]);
	// console.log(bol);
	// console.log(craftPath);
	// console.log(clickCount);
	// console.log(bol);
	var latLong = parseLatLong(e.latlng.toString()).split(",");
	var api_call = "http://nominatim.openstreetmap.org/reverse?format=json&lat={0}&lon={1}&zoom=18&addressdetails=1"
	var url = api_call.format(latLong[0],latLong[1]);
	if (craftPath) {
		clickCount += 1;
	}
	if (clickCount == 2 && bol && craftPath){
		console.log(craftPath);
		document.getElementById('enter_edge').style.display = 'none';
		document.getElementById('rank_in').style.display = 'block';
		clickCount = 0;
	    }
    else{
    	
    	if(craftPath){
    		document.getElementById('rank_in').style.display = 'none';
    		document.getElementById('enter_edge').style.display = 'block';}
    		coords = [];
   		}
	jQuery.getJSON(url).done([function(data){
		var address = data["display_name"];
		if (bol && craftPath){
			coords.push({'lat' : latLong[0],
									'long': latLong[1],
									'addr': address});
		}
		// console.log(JSON.stringify(coords));
		// $.ajax({
		// 		type: 'POST',
		// 		url: 'main',
		// 		data: {'lat' : latLong[0],
		// 					'long': latLong[1],
		// 							'addr': address}
		// 				});
				// console.log(p)
			popup
		.setLatLng(e.latlng)
		.setContent(address)
		.openOn(map);

			}]);

}
function showEdge1(){
	// console.log('YES');
	if(!craftPath){
		document.getElementById('enter_edge').style.display = 'block';
		craftPath = true;
		// console.log(craftPath);
	}
}
// function showEdge2(p){
// 	// console.log(p);
// 	 if (p[0]==="true"){
// 		document.getElementById('rank_in').style.display = 'block';}
// }
function enterRankz(){
	if (craftPath){
		// console.log("WHAT");
		var edgeRank = parseInt(document.getElementById('the_rank').value);
		enterRank = true;
		// console.log(edgeRank);
		$.ajax({
				type: 'POST',
				url: 'main',
				data: {'start' : coords[0],
					   'end': coords[1],
					   'rank': edgeRank,
					   'craft': 1}
							});
		// console.log("WHAT");
	    }
	    document.getElementById('rank_in').style.display = 'none';

	    document.getElementById('enter_edge').style.display = 'block';
	    var points = [[parseFloat(coords[0]['lat']),parseFloat(coords[0]['long'])],
	                  [parseFloat(coords[1]['lat']),parseFloat(coords[1]['long'])]];
	    // console.log(coords[0]['lat']);
	    // console.log(points[1]);
	    var polyline = L.polyline(points, {color: 'green'}).addTo(map);
}

function randomWalk(){
	
	var api_call1 = "http://nominatim.openstreetmap.org/search/{0},%20Edinburgh,%20Scotland,%20?format=json&addressdetails=1&limit=1&polygon_svg=1";
	var start = document.getElementById('start_point').value;
	var end = document.getElementById('end_point').value;
	var url1 = api_call1.format(start);
	var url2 = api_call1.format(end);
	// console.log(url1);
	$.getJSON(url1).done([function(data){
		// console.log(data);
		var lat1 = data[0]['lat'];
		var lon1 = data[0]['lon'];
		// console.log(lat1);
		$.getJSON(url2).done([function(data2){
			// console.log(data2);
			var lat2 = data2[0]['lat'];
			var lon2 = data2[0]['lon'];
			$.ajax({
					type: 'POST',
					url: 'main',
					data: {'lat1' : lat1,
						   'long1': lon1,
						   'addr1': start,
						   'lat2' : lat2,
						   'long2': lon2,
						   'addr2': end,
						   'walk' : 1}
							});
		}]);
	}]);
	(function worker() {
  $.ajax({
  	dataType: "json",
    url: '/get_walk', 
    success: function(data) {
      // console.log(data);
      if (linePresance == 1) {
		console.log("REMOVE");
        map.removeLayer(polyline);
      }
      walk = data;
      polyline = L.polyline(data['walk'], {color: 'red'}).addTo(map);
      linePresance = 1;
    },
    // complete: function() {
    //   // Schedule the next request when the current one's complete
    //   setTimeout(worker, 5000);
    // }
  });
})();
}




map.on('click', getAddress);
