/*
 * Handles ajax calls.
 */

function getJSON(url, postdata, successHandler, errorHandler){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.responseType = 'json';
    
    xhr.onload = function() {
        var status = xhr.status;
        if (status == 200){
            successHandler && successHandler(xhr.response);
        }else{
            errorHandler && errorHandler(status);
        }
    };
    
    if(postdata){
        xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xhr.send(postdata);
    }else{
        xhr.send();
    }
}

function error(status){
    alert('Something went wrong.'+status);
}

function debug(data){
    console.log(data);
}
