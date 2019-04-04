function changeVisibility(anID) {
		var groups = document.getElementsByTagName('g');
		var text = document.getElementById('coursetext' + anID);
		for (var x=0; x < groups.length; x++) {
			var group = groups[ x ]
			if (group.getAttribute('name') != ('coursegroup' + anID)) {
			    continue;
			}
			if  (group.getAttribute('opacity') == '0') {
			    var t = text.textContent
			    if (t.indexOf('+', t.length - 1) !== -1) {
			        text.textContent = t.substring(0,  (t.length - 1));
			    }
				group.setAttribute( 'opacity' , '100');
			} else {
			    var t = text.textContent
			    if (t.indexOf('+', t.length - 1) == -1) {
			        text.textContent = t + '+';
			    }
				group.setAttribute( 'opacity' , '0');
			}	
		}
}