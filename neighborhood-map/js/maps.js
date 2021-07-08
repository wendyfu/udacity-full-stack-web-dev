let map;
let markers = []

// Initialize and add the map
function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: { lat: 35.6928206, lng: 139.8410004 },
    styles: [{"featureType":"administrative","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"administrative.province","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"landscape","elementType":"all","stylers":[{"saturation":-100},{"lightness":65},{"visibility":"on"}]},{"featureType":"poi","elementType":"all","stylers":[{"saturation":-100},{"lightness":"50"},{"visibility":"simplified"}]},{"featureType":"road","elementType":"all","stylers":[{"saturation":"-100"}]},{"featureType":"road.highway","elementType":"all","stylers":[{"visibility":"simplified"}]},{"featureType":"road.arterial","elementType":"all","stylers":[{"lightness":"30"}]},{"featureType":"road.local","elementType":"all","stylers":[{"lightness":"40"}]},{"featureType":"transit","elementType":"all","stylers":[{"saturation":-100},{"visibility":"simplified"}]},{"featureType":"water","elementType":"geometry","stylers":[{"hue":"#ffff00"},{"lightness":-25},{"saturation":-97}]},{"featureType":"water","elementType":"labels","stylers":[{"lightness":-25},{"saturation":-100}]}]
  });

  locations.forEach(item => {
    markers.push(
      new google.maps.Marker({
        position: { lat: parseFloat(item.lat), lng: parseFloat(item.lng) },
        map: map,
      })
    );
  });
}

// Rerender markers
function updateMarkers(_locations) {
  markers.forEach(marker => {
    marker.setMap(null);
  })

  markers = []
  _locations.forEach(item => {
    markers.push(
      new google.maps.Marker({
        position: { lat: parseFloat(item.lat()), lng: parseFloat(item.lng()) },
        map: map,
      })
    );
  });
}