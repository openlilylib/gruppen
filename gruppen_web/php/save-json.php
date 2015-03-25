<?php
    $realfile = "../json/reservations.json";
    $bakfile = "../json/reservations.json.bak";
    $do_copy = false;
    $data = $_POST['data'];
    
    if(json_decode($data)) {
        if(isset($_POST['dobackup'])){
            $file = "../json/backup/reservations.json.bak";
        }else{
            $file = $realfile;
        }
        $success = file_put_contents($file, $data, LOCK_EX);
    }else{

        $success = 0;
    } 

    echo json_encode($success);
?>
