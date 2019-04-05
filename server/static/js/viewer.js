function setToMiddle() {
	var myDiv = document.getElementById("graph_img");
	var scrollto = myDiv.offset().top + (myDiv.height() / 2);
	myDiv.animate({ scrollTop: scrollto });
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
	$.get('/?coursenum=' + imageUri, function (data, status) {
		if (!data['nodes']) return;
		source = nodes[imageUri]
		
		var nodes = new vis.DataSet(data['nodes'].map(c => ({
			'id': c.number, 
			'label': c.name
		})));
		var edges = new vis.DataSet(data['edges'].map(t => ({
			'from': t[0], 
			'to': t[1]
		})));

		var container = document.getElementById('mynetwork');

		// provide the data in the vis format
		var data = {
			nodes: nodes,
			edges: edges
		};
		var options = {
			"layout": {
				"hierarchical": true
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