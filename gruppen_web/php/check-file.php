<?php

    $json = file_exists("../json/reservations.json");
    
    echo json_encode($json);
?>
