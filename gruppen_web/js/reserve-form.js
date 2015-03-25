/*
 * Functions that handle reservations.
 */

function checkUser(){
    
    //Set stored user
    setUserFromStorage();
}

function loginUser(){

    if(user){
        
        reserveDiv.style.display = "block";
    
        userSpan.appendChild(document.createTextNode(user));

        partSelect.onchange = formSelPart;
        segments.oninput = parseInput;
        reservButton.onclick = clickConfirm;
        resetButton.onclick = resetAll;
    }
}

//Set user if stored 
function setUserFromStorage(){
    
    var propUser, password, postdata;
    
    if(typeof(Storage) != "undefined"){    
        propUser = localStorage.getItem("user");
        password = localStorage.getItem("password");
    }
    
    postdata = "user=" + propUser + "&password=" + password;
    
    getJSON("./php/check-pass.php", postdata, checkLogin, error);
    
}

function clearPartSelect(){
    var first = partSelect.childNodes[1];
    var next = nextElement(first);
    while(next) {
        partSelect.removeChild(next);
        next = nextElement(first);
    }
}

function nextElement(node){
    var next = node.nextSibling;
    while(next && next.nodeType != 1) {
        next = next.nextSibling;
    }
    return next;
}

function clickConfirm(){

    updateReservations();
    resetForm();
}

//Select row from form.
function formSelPart(){

    if(segments.value){
        parseInput();
    }else{
        clearSelections();
        clearRowAndColSelections();
        var row = parseInt(partSelect.options[partSelect.selectedIndex].value);
        var part = partSelect.options[partSelect.selectedIndex].text;
        checkRowAction(row, part);
    }
}

/*
 * Parse the input from the form.
 */
 
function parseInput(){

    if(segments.value){        
        clearSelections();
        clearRowAndColSelections();
        
        var segmArr = segments.value.split(" ");
        parseInputArray(segmArr);

    }else{
        formSelPart();
    }
}

function parseInputArray(arr){
    
    var row = parseInt(partSelect.options[partSelect.selectedIndex].value);

    for(var i = 0; i < arr.length; i++){
            
        newArr = parseHyphenInput(arr[i]);
        if(newArr){
            parseInputArray(newArr);
        }else{ 
            var col = parseInt(arr[i]);
            if(row && col){
                selectSingle(row, col);
            }else if(col){
                checkColAction(col, arr[i]);
            }
        }
    }
}

function parseHyphenInput(inp){
    
    var patt = /[0-9]-[0-9]/;
    
    if(patt.test(inp)){
        var ends = inp.split("-");
        var newArr = Array();
        for (var i = ends[0]; i <= ends[1]; i++) {
            newArr.push(i);
        }
        return newArr;
    }else{
        return false;
    }
}

//Reset form and clear all selections
function resetForm(){
    
    partSelect.selectedIndex = 0;
    segments.value = '';
}

function resetAll(){
    
    resetForm();
    clearSelections();
    clearRowAndColSelections();
}

function reserveSelected(){
    
    var arr = [];
    
    //first check who is reserving
    if(user){
        //check selected
        if(selectArr.length > 0){
            //Do the reservation.
            for(var i = 0; i < selectArr.length; i++){

                if(selectArr[i].doReserve){
                    makeReservation(selectArr[i].td);
                }else{
                    undoReservation(selectArr[i].td);
                }
            }            
            checkRowAndColSelection();
            saveReservations();
            clearSelections();
        }
    }else{
        
        alert("You are not authorized as contributor to this project!");
    }
}

function checkRowAndColSelection(){

    if(rowSelected){
        reservationsJSONarr[rowSelected.part].reserved = rowSelected.user;
        updateData[rowSelected.part].reserved = rowSelected.user;
        rowSelected = false;
    }
    
    if(colSelected){
        reservationsJSONarr.allsegm.segments[colSelected.segm].isReserved = colSelected.user;
        if(!('allsegm' in updateData)){
            updateData.allsegm = { segments: {} };
            updateData.allsegm.segments[colSelected.segm] = {};
        }
        updateData.allsegm.segments[colSelected.segm].isReserved = colSelected.user;
        colSelected = false;
    }
}

function clearRowAndColSelections(){
    
    rowSelected = false;
    colSelected = false;
}
    

//Make the reservation. Don't forget to save it afterwards!
function makeReservation(rCell){
    
    rCell.setAttribute("class", "reserved-self");
    rCell.onmousedown = mouseDownSelfReserved;
    rCell.onmouseover = mouseOverSelfReserved;
    if(rCell.hasToolTip){
        removeToolTip(rCell);
        rCell.hasToolTip = false;
    }
    
    var sCell = progressData[rCell.part].segments[rCell.segm];
    
    var jCell = reservationsJSONarr[rCell.part].segments[rCell.segm];
    var compCell = reservCompare[rCell.part].segments[rCell.segm];
    
    //set reservation data
    if(!jCell.isReserved){
        jCell.user = user;
        jCell.isReserved = true;
        if(!(rCell.part in updateData)){
            updateData[rCell.part] = { segments: {} };
        }
        updateData[rCell.part].segments[rCell.segm] = jCell;
    }else{ //better update data on screen

        getProgressData();
    }
}

//Undo reservation/unassign.  Don't forget to save it afterwards!               
function undoReservation(rCell){
    
    rCell.setAttribute("class", "not-done");
    rCell.onmousedown = mouseDownUndone;
    rCell.onmouseover = mouseOverUndone;
    if(rCell.hasToolTip){
        removeToolTip(rCell);
        rCell.hasToolTip = false;
    }
    
    var jCell = { isReserved: false };
        
    reservationsJSONarr[rCell.part].segments[rCell.segm] = jCell;
    
    if(!(rCell.part in updateData)){
        updateData[rCell.part] = { segments: {} };
    }
    updateData[rCell.part].segments[rCell.segm] = jCell;
}

//Save reservations to file
function saveReservations(){
    
    //Inform user that save is ongoing
    topInfo.textContent = "Saving...";
    
    var d = JSON.stringify(updateData);
    getJSON('./php/update-json.php', "data="+d, informOnSave, error);
    
    //reset update data
    updateData = {};
}

//Do backup
function backupReservations(){
    
    var d = JSON.stringify(reservationsJSONarr);
    getJSON('./php/save-json.php', "data="+d+"&dobackup=t", getSaveInfo, error);
}

//Get data from file saving
function informOnSave(data){
    
    if(data){
    
        //Inform user that save is performed
        topInfo.textContent = "Reservations saved!";
        
        //reset timer
        clearInterval(timer);
        
        //remove info again after a while
        timer = setInterval(function(){
            topInfo.innerHTML = '\xA0';
            },11000);
    }else{
        //Inform user that save was unsuccesful
        topInfo.textContent = "Warning: Reservations not saved!!!!";
    }
}

//Get data from file saving
function getSaveInfo(data){
    
    //Nothing so far...
}

/*
 * Update reservations to get latest data
 */

function updateReservations(){
    
    var fr = "../json/reservations.json";
    getJSON('./php/read-json.php', "filename="+fr, performUpdateBeforeChange, error);
}
    
function performUpdateBeforeChange(data){

    if(data){
        reservCompare = data;
    }
    reserveSelected();
}

/*
 * Initial fetch of data from JSON-file.
 * If no data exists a clean array is built.
 */

function initReservations(){

    var fr = "../json/reservations.json";
    getJSON('./php/read-json.php', "filename="+fr, setReservations, error);
}
    
function setReservations(data){
    
    if(data){
        reservationsJSONarr = data;
        //do backup of read data
        backupReservations();
        parseData();
    }else{
        getJSON('./php/check-file.php', '', checkFile, error);
    }
}

function checkFile(fileExists){
    
    if(fileExists){
        var alertMess = "Something went wrong, please reload the page!";
        alert(alertMess);
        //reset from backup
        getJSON('./php/insert-backup.php', '', getSaveInfo, error);

    }else{
        //The user should know when reservations are reset
        var r = confirm("Reservations file not found. Do you want a create a new file?");
        if(r == true){
            resetReservations();
            var d = JSON.stringify(reservationsJSONarr, null, "    ");
            getJSON('./php/save-json.php', "data="+d, informOnSave, error);
            parseData();
        }  
    }
}
    
//Create an initial array for the reservations.
function resetReservations(){
    
    reservationsJSONarr = {};
    
    for(var part in progressData){
        var segments = progressData[part].segments;
        
        newReservePart(part, segments);
    }
    //"part" that holds data for whole segments
    newReservePart("allsegm", segments);

}

//Create a new part in the reservations data
function newReservePart(part, segments){
    
    reservationsJSONarr[part] = { 
        removed: false, 
        reserved: false,
        segments: {} };
        
    for(var segm in segments){
    
        var jCell = { isReserved: false };
    
        reservationsJSONarr[part].segments[segm] = jCell;
    }
}

/*
 * Check if any parts in the reservation data 
 * has been removed in the progress data
 */
function checkReserveParts(){
    
    for(var part in reservationsJSONarr){
        
        if(!(part in progressData)){
            
            //handle the mismatch
            reservationsJSONarr[part].removed = historyIndex;
        }
    }
    //saveReservations();
}
 
function unsetRemoved(part){
    
    reservationsJSONarr[part].removed = false;
    //saveReservations();
}
    
function checkLogin(isLoggedIn){

    if(isLoggedIn){
        if(typeof(Storage) != "undefined"){    
            user = localStorage.getItem("user");
        }
    loginUser();
    }
    //Fetch data after user is checked
    fileSelect.onchange = getProgressData;
    getJSON('./php/dropdown.php', '', setDDOptions, error);
}
        
