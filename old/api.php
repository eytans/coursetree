<?php
/*************************************************************
 * This basic API interface checks for argument validity
 * and then calls the Python script which returns a raw
 * byte stream of the PNG image. The stream is sent directly
 * to the user over HTTP and displayed as an image by the
 * browser thanks to the custom Content-Type header
 *************************************************************/
	$BASE_PATH = '/u1/023/eytan.s/.www/courses-tree';

	// Check that the course_id exists and is a 6-digit string (basic protection against injection)

	if(isset($_GET['course_id'])) {
		if(!empty($_GET['course_id']) && preg_match("/\d{6}/i",$_GET['course_id'])) {
			$param = $_GET['course_id'];
		} else {
			echo "ERROR: Invalid API parameter (did you remember to fill the course_id param?)";
			exit(0);
		}
		
		if(!empty($_GET['tree_depth'])) {
                        $param .= " --depth " . $_GET['tree_depth'];
		}

		if(!empty($_GET['faculties'])) {
			$arr = explode("|", $_GET['faculties'], 300);
			foreach($arr as $a) {
				if($a == '') {
					continue;
				}
				$param .= " -f " . $a;
			}
                }
	

		$command = 'python ' . $BASE_PATH . '/course_graph_maker.py ' . $param; // Tip: add 2>&1 here when debugging
		header("Content-Type: image/svg+xml");
		$pid = popen($command, "r");
	
		while(!feof($pid)) {
			echo fread($pid, 256);
			flush();
			ob_flush();
		}

		pclose($pid);
	}
?>
