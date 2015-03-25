/*
 * Init reservations.
 */
var reservationsJSONarr;
var reservCompare;
var updateData = {};

var user;

var reserveDiv = document.getElementById("reservediv");
var userSpan = document.getElementById("auth-usr");
var partSelect = document.getElementById("part-select");
var segments = document.getElementById("segm-txt-inp");
var reservButton = document.getElementById("reserv-button");
var resetButton = document.getElementById("reset-sel");
var topInfo = document.getElementById("top-info");

//Start by checking user
checkUser();

/*
 * Init interactions with the score table grid
 */

var isMouseDown = false;
var editing = false;
var rowSelected = false;
var colSelected = false;
var selectArr = [];

window.onmouseup = mouseUp;

/*
 * Init score grid table from JSON data.
 */

var progressData;
var metadata;
var historyIndex;
var scoreTable = document.getElementById("score-tab");
var currentRow;
var fileSelect = document.getElementById("file-select");
var stateHeader = document.getElementById("status");
var stateDate = document.getElementById("state-date");

/*
 * Extra
 */
 var leftAbove = document.getElementById("left-above");
 leftAbove.onclick = hideAllOpenToolTips;
 
 var timer;

