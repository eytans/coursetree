function setToMiddle() {
	var myDiv = document.getElementById("graph_img");
	var scrollto = myDiv.offset().top + (myDiv.height() / 2);
	myDiv.animate({ scrollTop: scrollto });
}

function getRandomColor() {
	var letters = '89ABCDEF';
	var color = '#';
	for (var i = 0; i < 6; i++) {
	  color += letters[Math.floor(Math.random() * 8)];
	}
	return color;
  }

function onDrawClick() {
	var imageUri = document.getElementById("course_id").value;

	var inputs = document.getElementsByTagName('input');
	// var faculties = '';
	// for (var x=0; x < inputs.length; x++) {
	// 	if((inputs[x].getAttribute("type") == "checkbox") && inputs[x].checked) {
	// 		faculties += inputs[x].value + "|"
	// 	}
	// }
	$.get('db/', { 'coursenum': imageUri }, function (data, status) {
		if (!data['nodes']) return;
		sourceId = Number(imageUri)

		var nodes = new vis.DataSet(data['nodes'].map(c => ({
			'id': c.number,
			'label': c.name + "\n" + c.number.toString()
		})));

		var edges = new vis.DataSet(data['edges'].map(t => ({
			'from': t[0],
			'to': t[1]
		})));

		// color the nodes
		nodes.update({
			id: sourceId, 
			color: {
				background: 'white',
				border: "black"
			},
			level: 0
		});

		var nextLayerIds = edges.get(options={
			filter: function(item) { return item.from == sourceId }
		}).map(function(item) { return item.to });

		var layer = 1;
		for (id of nextLayerIds) {
			nodes.update({
				id: id,
				color: {
					background: getRandomColor(),
					border: "black"
				},
				level: layer
			})
		};

		while (nextLayerIds.length != 0) {
			var temp = nextLayerIds
			nextLayerIds = edges.get(options={
				filter: function(item) { return temp.includes(item.from) }
			})
			layer += 1
			var doneThisRound = []
			for (e of nextLayerIds) {
				var nextColor = nodes.get(e.from).color;
				if (doneThisRound.includes(e.to)) {
					nextColor = getRandomColor();
				}
				nodes.update({
					id: e.to,
					color: nextColor,
					level: layer
				})
			};
		}

		var container = document.getElementById('mynetwork');

		// provide the data in the vis format
		var data = {
			nodes: new vis.DataSet(nodes.get({filter: function(item){return item['level'] !== undefined}})),
			edges: edges
		};

		var options = {
			"layout": {
				"hierarchical": {
					"direction": 'UD',
					"sortMethod": 'directed' //hubsize, directed.
				}
			},
			edges: {
				arrows: 'to',
				color: 'red',
				font: '12px arial #ff0000',
				scaling: {
					label: true,
				},
				shadow: true,
				smooth: true,
			},
			"physics": {
				"enabled": true,
				"hierarchicalRepulsion": {
					"nodeDistance": 220
				}
			}
		};

		// initialize your network!
		var network = new vis.Network(container, data, options);
	})

}

function onTextBoxPress(e) {
	if (e.KeyCode == 13 || e.which == 13) {
		onDrawClick();
		return true;
	}
	return false;
}