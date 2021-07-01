var initialCats = [
	{
		clickCount: 0,
		name: 'Tabby',
		imgSrc: 'img/434164568_fea0ad4013_z.jpg',
		nicknames: ['Kucing', 'Cat', 'Neko', 'Mao'],
	},
	{
		clickCount: 0,
		name: 'Tole',
		imgSrc: 'img/22252709_010df3379e_z.jpg',
		nicknames: ['Kempel'],
	},
	{
		clickCount: 0,
		name: 'Orange',
		imgSrc: 'img/9648464288_2516b35537_z.jpg',
		nicknames: ['Kimplung'],
	}
];

var Cat = function(data) {
	this.clickCount = ko.observable(data.clickCount);
	this.name = ko.observable(data.name);
	this.imgSrc = ko.observable(data.imgSrc);
	this.nicknames = ko.observableArray(data.nicknames);
	this.catLevel = ko.computed(function() {
		if (this.clickCount() < 10) {
			return 'Newborn';
		}

		if (this.clickCount() < 20) {
			return 'Infant';
		}

		return 'Teen';
	}, this);
}

var ViewModel = function() {
	var self = this;

	this.catList = ko.observableArray([]);

	initialCats.forEach(function(item) {
		self.catList.push(new Cat(item));
	})

	this.currentCat = ko.observable(this.catList()[0]);

	this.incrementCounter = function() {
		self.currentCat().clickCount(self.currentCat().clickCount() + 1);
	};

	this.selectCat = function(cat) {
		self.currentCat(cat);
	};
};

ko.applyBindings(new ViewModel());