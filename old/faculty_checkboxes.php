<?php
	$faculties = include 'get_faculties.php';
	echo $faculties;
	$fac_keys = array_keys($faculties);
	for($i=1;$i < count($faculties);$i += 1) {
		echo "<span>$key</span>"
		$vals = '';
		foreach ($faculties[$fac_keys[$i]] as $v) {
			$vals .= $v . "|";
		}
	echo '<input id="$key" type="checkbox" name="faculties[] "value="$vals"/>'
	}
?>