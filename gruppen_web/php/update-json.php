<?php
    $realfile = "../json/reservations.json";
    $bakfile = "../json/reservations.json.bak";
    
    //create a backup
    copy($realfile, $bakfile);
    
    //read existing reservations
    $string = file_get_contents($realfile);
    $reserv_data = json_decode($string, true);
    
    //new reservations
    $data = $_POST['data'];
    $new_data = json_decode($data, true);
    
    if($new_data){
        
        foreach($new_data as $part => $partdata){
            
            foreach($partdata as $cat => $catdata){
                
                if(is_array($catdata)){ 
            
                    foreach($catdata as $sub => $val){
                        
                        //check first if it's a reservetion
                        if(array_key_exists("isReserved", $reserv_data[$part][$cat][$sub])
                        && array_key_exists("isReserved", $val)){
                        
                            if(!$val["isReserved"] || 
                                !$reserv_data[$part][$cat][$sub]["isReserved"]){
                
                                $reserv_data[$part][$cat][$sub] = $val;
                            }
                        }
                    }
                }else{
                    
                    $reserv_data[$part][$cat] = $catdata;
                }
            }
        }
        
        $updated_data = json_encode($reserv_data, JSON_PRETTY_PRINT);
        
        $success = file_put_contents($realfile, $updated_data, LOCK_EX);
        
    }else{

        $success = 0;
    } 

    echo json_encode($success);
?>
