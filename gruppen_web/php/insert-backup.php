<?php
    $realfile = "../json/reservations.json";
    $backupfile = "../json/backup/reservations.json.bak";

    copy($backupfile, $realfile);
    
?>
