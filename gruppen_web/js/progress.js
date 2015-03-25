/*
 * Functions that write score grid table from JSON data.
 */

//populate filenames in dropdown
function setDDOptions(data){
    for(var i = 0; i < data.length; i++){
        var opt = document.createElement("option");
        var jsonFile = document.createTextNode(data[i].date)
        opt.appendChild(jsonFile);
        opt.value = data[i].file;
        opt.num = i+1;
        fileSelect.appendChild(opt);
    }
    //select the first option
    fileSelect.options[0].selected = true;
    getProgressData();
    
}

function clearTable(){
    while(scoreTable.lastChild) {
        scoreTable.removeChild(scoreTable.lastChild);
    }
}

//retrieve from json file
function getProgressData(){
    clearTable();
    clearPartSelect();
    historyIndex = fileSelect.options[fileSelect.selectedIndex].num;
    
     //disable reservations on all but the current state
    if(historyIndex > 1){
        reservButton.disabled = true;
    }else{
        reservButton.disabled = false;
    }
    
    var f = fileSelect.options[fileSelect.selectedIndex].value;
    getJSON('./php/read-json.php', "filename="+f, catchProgressData, error); 
}

//create table row
function tableRow(){
    var tr = document.createElement("tr");
    scoreTable.appendChild(tr);
    currentRow = tr;
}

//create table cell other than segment
function tableCell(tdClass, content){
    var td = document.createElement("td");
    if(tdClass){
        td.setAttribute("class", tdClass);
    }
    if(content){
        td.appendChild(content);
    }
    
    //set on row
    currentRow.appendChild(td);
    
    return td;
}

function topRow(segmInfo){
    tableRow();
    tableCell('', '');
    
    for(var i = 0; i < segmInfo.length; i++){
        var segm = segmInfo[i].name;
        var compl = segmInfo[i].completion;
        var sn;
        var segmNumTxt = document.createTextNode(segm);
        
        if(compl.completion == "100.00%"){
            sn = tableCell('completed-segm', segmNumTxt);
        }else{
            sn = tableCell('segm-num', segmNumTxt);
        }
        
        sn.appendChild(topRowToolTip(segm, compl));
        sn.hasToolTip = true;
        
        if(user){
            sn.onclick = clickSegm;
            sn.style.cursor = "pointer";
            sn.segm = segm;
        }
    }
}

function topRowToolTip(segm, compl){
    
    var info = "Completed: " + compl.completion;
    var addInfo = "Segments finished: " + compl.reviewed + " of " + compl.total; 

    return toolTip(segm, '', info, addInfo);
}

function partNameTab(part){
    var pnTxt = document.createTextNode(part.name);
    pn = tableCell("part-name", pnTxt);
    if(user){
        pn.onclick = clickPart;
        pn.style.cursor = "pointer";
    }
    pn.oncontextmenu = showToolTipPartname;
    pn.onmouseout = normalHideToolTip;
    pn.hasToolTip = false;
    pn.part = part;
    return pn;
}

function partNameToSelect(partname, row){
    var opt = document.createElement("option");
    opt.value = row;
    var pn = document.createTextNode(partname);
    opt.appendChild(pn);
    partSelect.appendChild(opt);
}
    
//create segment cell
function segmCell(tdClass, part, segm, name){
    
    var td = document.createElement("td");
    td.setAttribute("class", tdClass);
    
    //add listeners
    if(tdClass == "not-done"){
        if(user){
            td.onmousedown = mouseDownUndone;
        }
        td.onmouseover = mouseOverUndone;
    }else if(tdClass == "deleted"){
        td.onmouseover = mouseOverDeleted;
        td.onclick = showToolTipDeleted;
    }else if(tdClass == "reviewed"){
        td.onmouseover = mouseOverReviewed;
        td.onclick = showToolTipReviewed;
    }else if(tdClass == "entered"){
        td.onmouseover = mouseOverEntered;
        td.onclick = showToolTipEntered;
    }else if(tdClass == "reserved-self"){
        td.onmousedown = mouseDownSelfReserved;
        td.onmouseover = mouseOverSelfReserved;
    }else if(tdClass == "reserved"){
        td.onmouseover = mouseOverReserved;
        td.onclick = showToolTipReserved;
    }else if(tdClass == "ready-for-review"){
        td.onmouseover = mouseOverReadyReview;
        td.onclick = showToolTipReadyReview;
    }
    
    td.onmouseout = mouseOutSegment;
    
    //add reference to where to find the data for this segment
    td.part = part;
    td.segm = segm;
    td.name = name;
    td.hasToolTip = false;
    
    //set on row
    currentRow.appendChild(td);
}

function toolTip(code, segm, info, addInfo){
    var tt = document.createElement("div");
    tt.setAttribute("class", "tooltip");
    
    var span = document.createElement("span");
    
    //call out img
    span.appendChild(calloutImg());
    
    //part
    var b = document.createElement("b");
    var codeElem = document.createElement("code");
    var codeTN = document.createTextNode(code + ' ' + segm);
    codeElem.appendChild(codeTN);
    b.appendChild(codeElem);
    span.appendChild(b);
    
    span.appendChild(br());
    span.appendChild(hr());
    
    //info-row 1
    var enterTxt = document.createTextNode(info)
    span.appendChild(enterTxt);
    
    if(addInfo){
        span.appendChild(br());
        
        //info-row 2
        var revTxt = document.createTextNode(addInfo)
        span.appendChild(revTxt);
    }
    
    tt.onmouseover = function(){
        var span = this.getElementsByTagName("span")[0];
        span.style.display = "none";
    };
    
    tt.appendChild(span);
    
    return tt;
}

function removeToolTip(td){
    var tt = td.getElementsByTagName("div")[0];
    td.removeChild(tt);
}

function calloutImg(){
    var img = document.createElement("img");
    img.setAttribute("class", "callout");
    img.setAttribute("src", "callout.gif");
    return img;
}

function nbsp(){
    return document.createTextNode("\u00A0");
}

function br(){
    return document.createElement("br");
}

function hr(){
    return document.createElement("hr");
} 
       
function leadZero(num){
    var s = "0" + num;
    if(s.length>2){ //delete zero again
        return s.substr(1-s.length);
    }else{
        return s;
    }
}        

//catch data from JSON file
function catchProgressData(data){
    progressData = data.data;
    metadata = data.metadata;
    
    initReservations();
}

//parse data
function parseData(){
    setMetaData();
    var segmInfo = metadata.segmentsInfo;
    
    topRow(segmInfo);
    var r = 0;

    for(var part in progressData){
        
        var pdPart = progressData[part];
        tableRow();
        var partTd = partNameTab(pdPart);
        
        r++;

        if(pdPart.completion.completion == "100.00%"){
            partTd.setAttribute("class", "completed-part");
        }else{
            partNameToSelect(pdPart.name, r);
        }
        if(!(part in reservationsJSONarr)){
            newReservePart(part, pdPart.segments);
        }

        var rdPart = reservationsJSONarr[part];
        
        if(rdPart.removed){
            
            if(rdPart.removed >= historyIndex){
                //unlikely that a removed part would return but it could happen
                unsetRemoved(part);
            }else{
                //Show that the part has been removed in a later state
                partTd.setAttribute("class", "removed");
            }
        }
        
        for(var c = 0; c < segmInfo.length; c++){
            var segm = segmInfo[c].name;
            var pdSegm = pdPart.segments[segm];
            
            if(!pdSegm){ //segment not done
                pdSegm = { status: "not-done" };
                pdPart.segments[segm] = pdSegm;
            }
            
            var rdSegm = rdPart.segments[segm];
            
            if(!rdSegm){ //segment not done
                rdSegm = { isReserved: false };
                rdPart.segments[segm] = rdSegm;
            }
            
            //Check if the cell is reserved
            if(rdSegm.isReserved && pdSegm.status=="not-done"){
 
                if(rdSegm.user == user){
                    segmCell("reserved-self", part, segm, pdPart.name);
                }else{
                    segmCell("reserved", part, segm, pdPart.name);
                }
            }else{
            
                segmCell(pdSegm.status, part, segm, pdPart.name);
            }
        }
    }

    //check if part is removed
    if(historyIndex == 1){ //only do this check on the latest state
        checkReserveParts();
    }
}

//Parse metadata
function setMetaData(){
    
    //Change state header
    if(historyIndex > 1){
        
        stateHeader.textContent = "Older status of music entry";
    }else{
        stateHeader.textContent = "Current status of music entry";
    }
    
    stateDate.textContent = metadata["date-time"];

}
    
     
