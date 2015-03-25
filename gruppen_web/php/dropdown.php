<?php
    //sort function
    function sortDates( $a, $b ) {
        return strtotime($b["date"]) - strtotime($a["date"]);
    }
    //get the files in folder
    $files = glob('../json/status-data/*.json');
    $dates = array();
    //get the dates
    foreach($files as $file){
        $json = file_get_contents($file);
        $json_data = json_decode($json, true);
        $dates[] = array("file" => $file, 
            "date" => $json_data['metadata']['dateTime']);
    }
    //sort the dates
    usort($dates, "sortDates");
    echo json_encode($dates);
?>
