<?php
    $filename = $_POST['filename'];
    if($filename){
        $string = file_get_contents($filename);
        $json = json_decode($string);
        echo json_encode($json);
    }else{
        header("HTTP/1.0 404 Not Found");
    }
?>
