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
			'label': c.name + "\n" + c.number.toString(),
			'hidden': false
		})));

		var edges = new vis.DataSet(data['edges'].map(t => ({
			'from': t[0],
			'to': t[1],
			'hidden': false
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

		while (nextLayerIds.length !== 0) {
			var nextLayerEdges = edges.get(options={
				filter: function(item) { return nextLayerIds.includes(item.from) }
			});
			layer += 1;
			var doneThisRound = [];
			for (e of nextLayerEdges) {
				var nextColor = nodes.get(e.from).color;
				if (doneThisRound.includes(e.to)) {
					nextColor = getRandomColor();
				}
				nodes.update({
					id: e.to,
					color: nextColor,
					level: layer
				})
			}
			nextLayerIds = nextLayerEdges.map(function(e) {return e.to});
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

		function toggleSubtree(nodeId) {
			var ee = edges.get({
				filter: function(item) {
					return item.from == nodeId
				}
			})
			for (e of ee) {
				n = nodes.get(e.to)
				console.log(n)
				edges.update([{id: e.id, hidden: !e.hidden}])
				toggleSubtree(n.id)
				nodes.update([{id: n.id, hidden: !n.hidden}])
				//var insertedEdges = edges.get({
				//	filter: function(item) {
				//		return item.to == nodeId && item.hidden == true
				//	}})
				//if (insertedEdges.length == 0) {
				//	var n = nodes.get(e.to)
				//	nodes.update({id: n.id, hidden: !n.hidden})
				//}
			}
		}
		// initialize your network!
		var network = new vis.Network(container, data, options);
		// TODO: hide network upon single click
		//network.on( 'click', function(properties) {
		//	var n = nodes.get(properties.nodes)[0];
		//	toggleSubtree(n.id)
		//});
		// Open course site upon double click :)
		network.on( 'doubleClick', function(properties) {
			var clickedNode = nodes.get(properties.nodes)[0];
			window.open('https://ug3.technion.ac.il/rishum/course/' + clickedNode.id, '_blank');
		});
	})

}

function onTextBoxPress(e) {
	if (e.KeyCode == 13 || e.which == 13) {
		onDrawClick();
		return true;
	}
	return false;
}