const locations = [
  { name: 'Tokyo Tower', lat: 35.6585848, lng: 139.7432442 },
  { name: 'Shinjuku Gyoen National Garden', lat: 35.6851806, lng: 139.707863 },
  { name: 'Tokyo DisneySea', lat: 35.6267151, lng: 139.8828892 },
  { name: 'Sensō-ji Temple', lat: 35.7147694, lng: 139.7944666 },
  { name: 'Tokyo Skytree', lat: 35.710067, lng: 139.8085117 },
];

var Location = function(data) {
	this.name = ko.observable(data.name);
	this.lat = ko.observable(data.lat);
	this.lng = ko.observable(data.lng);
}

var ViewModel = function() {
	var self = this;

	this.query = ko.observable("")

	this.query.subscribe(function(_query) {
		_query = _query.toLowerCase()
		self.locationList([])
		self.locationList(
			locations.filter(item => item.name.toLowerCase().includes(_query))
				.map(item => new Location(item))
		)
		updateMarkers(self.locationList())
	});

	this.locationList = ko.observableArray([]);

	locations.forEach(function(item) {
		self.locationList.push(new Location(item));
	})

	this.clickedLocation = ko.observable();

	this.onLocationClick = function(location) {
		self.clickedLocation(location);
		onListItemClick(location)
	};
}

ko.applyBindings(new ViewModel());