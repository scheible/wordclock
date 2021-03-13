var currentViewId = 0;
var lastState;


$(document).ready(function(){
	showPage('#pTimezone');

	$('#mWifi').click(menuOnclickWifi);
	$('#mClock').click(menuOnclickClock);
	$('#mSnake').click(menuOnclickSnake);
	$('#mTimezone').click(menuOnclickTimezone);

	$('#btnClockStart').click(appClockStart);


	initState();
	longPolling();
});

function longPolling() {
	console.log("polling viewId=" +  currentViewId);
	$.get("/longpoll", function(data, status){
	    if (status == 'success') {
	    	jData = JSON.parse(data);
	    	if (jData.state == 'ok' && jData.update == 1) {
	    		routeNewStateToApp(jData);
	    	}
	    }
	    longPolling();
	});
}

function initState() {
	$.get("/state", function(data, status){
	    if (status == 'success') {
	    	jData = JSON.parse(data);
	    	routeNewStateToApp(jData);
	    }
	});	
}

function routeNewStateToApp(data) {
	console.log(data.update);
	if (data.state != 'ok')
		return;

	lastState = data;

	stopAllApps();
	switch(data.app.appId) {
		case 0:
			// no app active -> show loading screen
			break;
		case 1:
			// clock app active -> switch to clock
			//$('#mClock').click();
			startApp('#pClock');
			processClockState(data.app);
			break;
		case 2:
			//snake
			startApp('#pSnake');
			break;
	}

}

function processClockState(appData) {
	$('#cAppDefaultProfile #bodyBrightness').val(appData.defaultProfile.brightnessBody);
	$('#cAppDefaultProfile #bodyColor').val(hRGB2HEX(appData.defaultProfile.colorBodyRGB));

	$('#cAppDefaultProfile #frameBrightness').val(appData.defaultProfile.brightnessBorder);
	$('#cAppDefaultProfile #frameColor').val(hRGB2HEX(appData.defaultProfile.colorBorderRGB));

	$('#cAppDefaultProfile #minutesBrightness').val(appData.defaultProfile.brightnessMinute);
	$('#cAppDefaultProfile #minutesColor').val(hRGB2HEX(appData.defaultProfile.colorMinuteRGB));

	$('#cAppDefaultProfile #secondsBrightness').val(appData.defaultProfile.brightnessSecond);
	$('#cAppDefaultProfile #secondsColor').val(hRGB2HEX(appData.defaultProfile.colorSecondRGB));
}

function changeDefaultProfile(key, value) {
	console.log(key);
	console.log(key)
	dataToChange = {
			"commandType": "set",
			"dat": {
				"defaultProfile": {}
				}
			};

	dataToChange.dat.defaultProfile[key] = value;

	$.ajax({
			  type: "POST",
			  url: "/set",
			  contentType: "application/json",
			  data: JSON.stringify(dataToChange),
			  dataType: "json"
			});
}




// ---- View Management -----------------------------------

function stopAllApps() {
	$('.applicationPane').hide();
	$('.applicationStartButton').show();
}

function startApp(pageViewId) {
	$(pageViewId + ' .applicationPane').show();
	$(pageViewId + ' .applicationStartButton').hide();
}

function hideAllPages() {
	$('.page').hide();
}

function showPage(id) {
	hideAllPages();
	$(id).show();
	currentViewId = id;
}

// ---- Loading of single pages ---------------------------

function menuOnclickWifi(){
	showPage('#pWifi');

	// Get a list with all wifi networks from the server
	$.get("/listwifi", function(data, status){
	    if (status == 'success') {
	    	$('#wifiSpinner').hide();
	    	$('#wifiName option').each(function(){$(this).remove();});
	    	jData = JSON.parse(data);
	    	for (i=0; i<jData.length; i++) {
				hAddOption('#wifiName', jData[i], jData[i]);
	    	}
	    }
	});
}

function menuOnclickClock(){
	showPage('#pClock');
}
function menuOnclickSnake(){
	showPage('#pSnake');
}
function menuOnclickTimezone(){
	showPage('#pTimezone');
}

function appClockStart() {
	alert("starting clock application...");
}

// ---- Helper Functions ---------------------------------

function hAddOption(elementId, optionText, optionValue) {
	$('#wifiName').append(`<option value="${optionValue}"> 
	                           ${optionText} 
	                      </option>`);	
}

function hRGB2HEX(rgb) {
	r = rgb[0].toString(16);
	g = rgb[1].toString(16);
	b = rgb[2].toString(16);

	if (r.length == 1)
	r = "0" + r;
	if (g.length == 1)
	g = "0" + g;
	if (b.length == 1)
	b = "0" + b;

	return "#" + r + g + b;
}

function hHEX2RGB (hex) {
    if (hex.charAt(0) === '#') {
        hex = hex.substr(1);
    }
    if ((hex.length < 2) || (hex.length > 6)) {
        return false;
    }
    var values = hex.split(''),
        r,
        g,
        b;

    if (hex.length === 2) {
        r = parseInt(values[0].toString() + values[1].toString(), 16);
        g = r;
        b = r;
    } else if (hex.length === 3) {
        r = parseInt(values[0].toString() + values[0].toString(), 16);
        g = parseInt(values[1].toString() + values[1].toString(), 16);
        b = parseInt(values[2].toString() + values[2].toString(), 16);
    } else if (hex.length === 6) {
        r = parseInt(values[0].toString() + values[1].toString(), 16);
        g = parseInt(values[2].toString() + values[3].toString(), 16);
        b = parseInt(values[4].toString() + values[5].toString(), 16);
    } else {
        return false;
    }
    return [r, g, b];
}