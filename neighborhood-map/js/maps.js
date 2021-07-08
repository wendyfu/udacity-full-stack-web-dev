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
    let marker = new google.maps.Marker({
      position: { lat: parseFloat(item.lat), lng: parseFloat(item.lng) },
      map: map,
      animation: google.maps.Animation.DROP,
      title: item.name
    })    
    markers.push(marker);
  });

  markers.forEach(marker => {
    marker.addListener("click", function() {
      markers.filter(_marker => _marker !== marker)
        .forEach(_marker => _marker.setAnimation(null))
      onMarkerClick(marker)
    });
  })
}

// Rerender markers
function updateMarkers(_locations) {
  markers.forEach(marker => {
    marker.setMap(null);
  })

  markers = []

  _locations.forEach(item => {
    let marker = new google.maps.Marker({
      position: { lat: parseFloat(item.lat()), lng: parseFloat(item.lng()) },
      map: map,
      animation: google.maps.Animation.DROP,
      title: item.name()
    })
    markers.push(marker);
  });

  markers.forEach(marker => {
    marker.addListener("click", function() {
      markers.filter(_marker => _marker !== marker)
        .forEach(_marker => _marker.setAnimation(null))
      onMarkerClick(marker)
    });
  })
}

// Listener to list item click
function onListItemClick(location) {
  onMarkerClick(markers.find(marker => marker.getTitle() === location.name()))
}

// Function to run when marker clicked
function onMarkerClick(target) {
  if (target.getAnimation() !== null) {
    target.setAnimation(null);
  } else {
    target.setAnimation(google.maps.Animation.BOUNCE);
  }

  loadInfoWindow(target.getTitle(), target)
}

// Fetch data from 3rd party
function loadInfoWindow(title, marker) {
    let nyTimesUrl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q=' + title + '&api-key=API_KEY';

    let contentString =
      '<h3>'+ title +'</h3>' +
      '<div id="bodyContent">';

    $.getJSON(nyTimesUrl, function(data){
      console.log('success')
      contentString += '<h5>New York Times Articles About: ' + title + '</h5>';
      contentString += '<ul class="list-group list-group-flush">'
      articles = data.response.docs;
      for( var i=0; i<articles.length; i++) {
        var article = articles[i];
        contentString += '<li class=""list-group-item">' +
          '<a href="'+ article.web_url + '">' + article.headline.main + '</a>' +
          '<p>' + article.snippet +'</p>' +
          '</li>';
      }
      contentString += '</ul></div>';
      const infowindow = new google.maps.InfoWindow({
        content: contentString,
      });
      infowindow.open({
        anchor: marker,
        map,
        shouldFocus: false
      });
    }).error(function(e){
      contentString += '<div class="text-danger">New York Times Articles Could Not be Loaded</div>';
      contentString += '</div>';
      const infowindow = new google.maps.InfoWindow({
        content: contentString
      });
      infowindow.open({
        anchor: marker,
        map,
        shouldFocus: false
      });
    });

    return false;
  };