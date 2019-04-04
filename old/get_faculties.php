<?php
	$lines = file("technion_faculties.txt");
	if ($lines == false) {
		return NULL;
	}

	foreach($lines as $line) 
	{
		if (strpos($line,"--startfaculty--") !== false) {
			$name = "";
			$values = array()
		}
		elseif (strpos($line,"fac_name") !== false) {
			$name = explode("=", $line, 2)[1];
		}
		elseif (strpos($line,"fac_num=") !== false) {
			$values[] = explode("=", $line, 2)[1];
		}
		elseif (strpos($line,"--endfaculty--") !== false) {
			$arr[$name] = $values
		}
	}
	return $arr;
?>
