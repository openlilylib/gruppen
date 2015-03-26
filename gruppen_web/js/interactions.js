/*
 * Functions that handle interactions with the score table grid
 */

function mouseDownUndone(event){
    event = event || window.event;
    if(event.ctrlKey && historyIndex == 1){
        clearSelections(); //clear all previous selections
        hideToolTip(this);
        editing = true;
        isMouseDown = true;
        toggleSelectUndone(this);
        return false; // prevent text selection
    }else{
        showToolTipUndone(this);
    }
}

function mouseOverUndone(){

    if(isMouseDown){
        toggleSelectUndone(this);
    }else{
        mouseOverSegment(this);
    }
}

function showToolTipUndone(elem){
    
    if(!elem.hasToolTip){
    
        var sd = progressData[elem.part].segments[elem.segm];
        
        var info = "";
        
        var addInfo;
        if(historyIndex == 1){
            addInfo = "Ctrl+Click to reserve";
        }else{
            addInfo = "Change to latest status to reserve.";
        }

        elem.appendChild(toolTip(elem.name, elem.segm, info, addInfo));
                    
        elem.hasToolTip = true;
    }
    showToolTip(elem);
}

function mouseUp(){
    
    isMouseDown = false;
    if(editing){
        editing = false;
        updateReservations();
    }
}

function mouseDownSelfReserved(event){
    event = event || window.event;
    if(event.ctrlKey && historyIndex == 1){
        clearSelections(); //clear all previous selections
        hideToolTip(this);
        editing = true;
        isMouseDown = true;
        toggleUnassigned(this);
        return false; // prevent text selection
    }else{
        showToolTipSelfReserved(this);
    }
}

function mouseOverSelfReserved(){
    
    if(isMouseDown){
        toggleUnassigned(this);
    }else{
        mouseOverSegment(this);
    }
}

function showToolTipSelfReserved(elem){
    
    if(!elem.hasToolTip){
        
        var sd = progressData[elem.part].segments[elem.segm];
        var rd = reservationsJSONarr[elem.part].segments[elem.segm];
        
        var info = "Reserved by: " + rd.user;
        
        var addInfo;
        if(historyIndex == 1){
            addInfo = "Ctrl+Click to unassign";
        }else{
            addInfo = "Change to latest status to unassign";
        }

        elem.appendChild(toolTip(elem.name, elem.segm, info, addInfo));
                    
        elem.hasToolTip = true;
                    
    }
    showToolTip(elem);
}

//Triggered when user clicks on part name in the left column
function clickPart(){
    event = event || window.event;
    if(event.ctrlKey && historyIndex == 1){
        hideToolTip(this);
        var row = this.parentNode.rowIndex;
        //bug in chrome?
        if(row==-1){
            row = this.parentNode.sectionRowIndex;
        }
        checkRowAction(row, this.part);
        updateReservations();
    }else{
        showToolTipPartname(this);
    }
}

function checkRowAction(row, part){
    
    rowSelected = { part: part, user: false };
    if(reservationsJSONarr[part].reserved == user){ //unreserve previous
        highlightRow(row, false);
    }else{ //not reserved previously
        highlightRow(row, true);
        rowSelected.user = user;
    }
}

//Triggered when user clicks on segment in top row
function clickSegm(){
    event = event || window.event;
    if(event.ctrlKey && historyIndex == 1){
        hideToolTip(this);
        checkColAction(this.cellIndex, this.segm);
        updateReservations();
    }else{
        showToolTip(this);
    }
}

function checkColAction(col, segm){
    
    segm = parseInt(segm);
    segm = leadZero(segm);
    colSelected = { segm: segm, user: false };
    if(reservationsJSONarr.allsegm.segments[segm].isReserved == user){ //unreserve previous
        highlightCol(col, false);
    }else{ //not reserved previously
        highlightCol(col, true);
        colSelected.user = user;
    }
}
    
function highlightRow(row, doReserve){
    
    var rows = scoreTable.rows;
    var rowTDs = rows[row].cells;

    for(i=0; i < rowTDs.length; i++){
        
        if(doReserve){
            if(rowTDs[i].getAttribute("class") == "not-done"){
                toggleSelectUndone(rowTDs[i]);
            }
        }else{
            
            if(rowTDs[i].getAttribute("class") == "reserved-self"){
                toggleUnassigned(rowTDs[i]);
            }
        }
    }
}

function highlightCol(col, doReserve){
    
    var rows = scoreTable.rows;
    
    for(i=0; i < rows.length; i++){
        
        var ci = rows[i].cells[col];
        
        if(doReserve){
        
            if(ci.getAttribute("class") == "not-done"){
                toggleSelectUndone(ci);
            }
        }else{
            
            if(ci.getAttribute("class") == "reserved-self"){
                toggleUnassigned(ci);
            }
        }
    }
}

function selectSingle(r, c){
    
    var rows = scoreTable.rows;
    var ci = rows[r].cells[c];
    
    if(ci.getAttribute("class") == "not-done"){
        toggleSelectUndone(ci);
    }else if(ci.getAttribute("class") == "reserved-self"){
        toggleUnassigned(ci);
    }
}

function toggleSelectUndone(elem){

    if(elem.getAttribute("class") == "not-done"){
        elem.setAttribute("class", "highlighted");
        var selObj = { td: elem, doReserve: true };
        var index = pushToSelectArr(selObj);
        elem.selIndex = index;
    }else{
        elem.setAttribute("class", "not-done");
        var index = elem.selIndex;
        if (index > -1) {
            selectArr.splice(index, 1);
        }
    }
}

function toggleUnassigned(elem){

    if(elem.getAttribute("class") == "reserved-self"){
        elem.setAttribute("class", "unassigning");
        var selObj = { td: elem, doReserve: false };
        var index = pushToSelectArr(selObj);
        elem.selIndex = index;
    }else{
        elem.setAttribute("class", "reserved-self");
        var index = elem.selIndex;
        if (index > -1) {
            selectArr.splice(index, 1);
        }
    }
}

function pushToSelectArr(obj){
    
    var len = selectArr.length;

    selectArr[len] = obj;
    
    //return index
    return len;
}

function showToolTipPartname(elem){
    
    if(!elem.hasToolTip){

        var partdata = elem.part;
        var compl = partdata.completion;
        
        var info = "Completed: " + compl.completion;
        var addInfo = "Segments finished: " + compl.reviewed + " of " + compl.total;
        
        var del;
        
        if(elem.getAttribute("class") == "removed"){
            del = "**REMOVED**";
        }else{
            del = "";
        }

        elem.appendChild(toolTip(elem.textContent, del, info, addInfo));
                    
        elem.hasToolTip = true;
    }
    showToolTip(elem);
    return false;
}

function mouseOverDeleted(){
    
    mouseOverSegment(this);
}

function showToolTipDeleted(){
    
    if(!this.hasToolTip){

        var sd = progressData[this.part].segments[this.segm];
        
        var info = "Deleted by: " + sd['deleted-by'];
        var addInfo = "";

        this.appendChild(toolTip(this.name, this.segm, info, addInfo));
                    
        this.hasToolTip = true;
    }
    showToolTip(this);
    return false;
}

function mouseOverReviewed(){
    
    mouseOverSegment(this);
}

function showToolTipReviewed(){
    
    if(!this.hasToolTip){

        var sd = progressData[this.part].segments[this.segm];
        
        var info = "Entered by: " + sd['entered-by'] + 
            " (" + sd['entry-date'] + ")";
        var addInfo = "Proofread by: " + sd['proofread-by'] + 
            " (" + sd['proof-date'] + ")"; 

        this.appendChild(toolTip(this.name, this.segm, info, addInfo));
                    
        this.hasToolTip = true;
                    
    }
    showToolTip(this);
}

function mouseOverEntered(){
    
    mouseOverSegment(this);
}

function showToolTipEntered(){
    
    if(!this.hasToolTip){

        var sd = progressData[this.part].segments[this.segm];
        
        var info = "Entered by: " + sd['entered-by'] + 
            " (" + sd['entry-date'] + ")";
        var addInfo = "Proofread by: " + sd['proofread-by'] + 
            " (" + sd['proof-date'] + ")"; 

        this.appendChild(toolTip(this.name, this.segm, info, addInfo));
                    
        this.hasToolTip = true;
                    
    }
    showToolTip(this);
}

function mouseOverReserved(){
    
    mouseOverSegment(this);
}

function showToolTipReserved(){
    
    if(!this.hasToolTip){
        
        var sd = progressData[this.part].segments[this.segm];
        var rd = reservationsJSONarr[this.part].segments[this.segm];
        
        var info = "Reserved by: " + rd.user;
        var addInfo = '';

        this.appendChild(toolTip(this.name, this.segm, info, addInfo));
                    
        this.hasToolTip = true;
                    
    }
    showToolTip(this);
}

function mouseOverReadyReview(){
    
    mouseOverSegment(this);
}

function showToolTipReadyReview(){
    
    if(!this.hasToolTip){
        
        var sd = progressData[this.part].segments[this.segm];
        
        var info = "Entered by: " + sd['entered-by'] + 
            " (" + sd['entry-date'] + ")";
        var addInfo = "Review branch: " + sd['review-branch']; 

        this.appendChild(toolTip(this.name, this.segm, info, addInfo));
                    
        this.hasToolTip = true;
                    
    }
    showToolTip(this);
}

//Highlight row and column of the segment
function mouseOverSegment(td){
    
    setCurrCordsHighlgth(td, "15px solid yellow", "yellow");
}

//Remove highlightning
function mouseOutSegment(){
    
    setCurrCordsHighlgth(this, "15px solid white", "initial");
}
    
function setCurrCordsHighlgth(td, brdr, bgcol){
    
    var currCords = getCurrentCoords(td);
    
    var r = currCords[0];
    var c = currCords[1];
    
    var rows = scoreTable.rows;
    
    
    var partcell = rows[r].cells[0];
    var segmcell = rows[0].cells[c];
    
    if(bgcol == "initial"){
        //fetch inital
        partBgcol = partcell.bgcol;
        segmBgcol = segmcell.bgcol;
    }else{
        //store initial
        partcell.bgcol = partcell.style.backgroundColor;
        segmcell.bgcol = segmcell.style.backgroundColor;
        
        partBgcol = segmBgcol = bgcol;
    }
    
    //highlight row    
    partcell.style.borderLeft = brdr;
    partcell.style.backgroundColor = partBgcol;
    
    //highlight col
    segmcell.style.borderTop = brdr;
    segmcell.style.backgroundColor = segmBgcol;
}

function getCurrentCoords(segm){
    
    var r = segm.parentNode.rowIndex;
    //bug in chrome?
    if(r==-1){
        r = segm.parentNode.sectionRowIndex;
    }
    
    var c = segm.cellIndex;
    
    return [r, c];
}        

function showToolTip(elem){
    //Only display one tooltip at a time
    hideAllOpenToolTips();
    
    //Open selected tooltip
    var div = elem.getElementsByTagName("div")[0];
    var span = div.getElementsByTagName("span")[0];
    span.style.display = "inline";
}

function hideToolTip(elem){
    if(elem.hasToolTip){
        var div = elem.getElementsByTagName("div")[0];
        var span = div.getElementsByTagName("span")[0];
        span.style.display = "none";
    }
}

function hideAllOpenToolTips(){
    
    var tds = document.getElementsByTagName("td");
    
    for(var t = 0; t < tds.length; t++){
        
        hideToolTip(tds[t]);
    }
}

function normalHideToolTip(){
    
    hideToolTip(this);
}

function clearSelections(){
    
    var rows = scoreTable.rows;
    
    for(r=0; r < rows.length; r++){
        for(c=0; c < rows[r].cells.length; c++){
            
            var ci = rows[r].cells[c]; 
                       
            if(ci.getAttribute("class") == "highlighted"){
                ci.setAttribute("class", "not-done");
            }
            if(ci.getAttribute("class") == "unassigning"){
                ci.setAttribute("class", "reserved-self");
            }
        }
    }
    selectArr = [];
}
    
