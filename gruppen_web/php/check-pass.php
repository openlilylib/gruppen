<?php

    $user = $_POST['user'];
    $clrTxtPassword = $_POST['password'];
    
    $login = false;

    //Encrypt password
    $cryptPassword = crypt($clrTxtPassword, base64_encode($clrTxtPassword));

    $passwstring = file_get_contents(".btfscsswd");
    
    $lines = explode("\n", $passwstring);
    
    foreach($lines as $l){
    
        $d = explode(':', $l);
        
        if($d[0] == $user && $d[1] == $cryptPassword){
            
            $login = true;
        }
    }
    
    echo json_encode($login);

?>
