var currentViewId = 0;
var lastState;


$(document).ready(function(){
	$('#mWifi').click(menuOnclickWifi);
	$('#mClock').click(menuOnclickClock);
	$('#mSnake').click(menuOnclickSnake);
	$('#mTimezone').click(menuOnclickTimezone);

	$('#btnClockStart').click(appClockStart);

	stopAllApps();;
	initState();
	longPolling();

	$('#mClock').click();
});

function longPolling() {
	$.ajax({
		url: "/longpoll",
		success: function(data, status){
		    	jData = JSON.parse(data);
		    	if (jData.state == 'ok' && jData.update == 1) {
		    		routeNewStateToApp(jData);
		    	}
			    longPolling();
			},
		timeout: 7000,
		error: function(data, status){
			alert("Verbindung mit der Uhr verloren. Bitte lade die Seite neu.");
		}
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
	if (data.state != 'ok')  {
		alert("Interner Fehler. Bitte starte die Uhr neu!");
		return;
	}

	app = data.data.applications[0];

	stopAllApps();
	switch(app.appId) {
		case 0:
			// no app active -> show loading screen
			break;
		case 1:
			// clock app active -> switch to clock
			//$('#mClock').click();
			startApp('#pClock');
			processClockState(app);
			break;
		case 2:
			//snake
			startApp('#pSnake');
			break;
	}

}

function processClockState(appData) {
	$('#cAppTotalBrightness #totalBrightness').val(appData.brightness);

	$('#cAppDefaultProfile #bodyBrightness').val(appData.defaultProfile.brightnessBody);
	$('#cAppDefaultProfile #bodyColor').val(hRGB2HEX(appData.defaultProfile.colorBodyRGB));

	$('#cAppDefaultProfile #frameBrightness').val(appData.defaultProfile.brightnessBorder);
	$('#cAppDefaultProfile #frameColor').val(hRGB2HEX(appData.defaultProfile.colorBorderRGB));

	$('#cAppDefaultProfile #minutesBrightness').val(appData.defaultProfile.brightnessMinute);
	$('#cAppDefaultProfile #minutesColor').val(hRGB2HEX(appData.defaultProfile.colorMinuteRGB));

	$('#cAppDefaultProfile #secondsBrightness').val(appData.defaultProfile.brightnessSecond);
	$('#cAppDefaultProfile #secondsColor').val(hRGB2HEX(appData.defaultProfile.colorSecondRGB));

	//process the user defined profiles
	$(".userProfile").remove();

	for (i=0;i<appData.userProfiles.length;i++) {
		processClockUserProfile(appData.userProfiles[i], i);
	}
}

function processClockUserProfile(profileData, i) {

	profileElement = createProfile(i);
	profileElement.show();

	hEnableToggle(profileElement.find("#profileActiveToggle i"), profileData.userProfileEnabled);
	
	profileElement.find("#cProfileStart").val(hTimeToString(profileData.startTime));
	profileElement.find("#cProfileEnd").val(hTimeToString(profileData.stopTime));

	profileElement.find('#bodyBrightness').val(profileData.config.brightnessBody);
	profileElement.find('#bodyColor').val(hRGB2HEX(profileData.config.colorBodyRGB));

	profileElement.find('#frameBrightness').val(profileData.config.brightnessBorder);
	profileElement.find('#frameColor').val(hRGB2HEX(profileData.config.colorBorderRGB));

	profileElement.find('#minutesBrightness').val(profileData.config.brightnessMinute);
	profileElement.find('#minutesColor').val(hRGB2HEX(profileData.config.colorMinuteRGB));

	profileElement.find('#secondsBrightness').val(profileData.config.brightnessSecond);
	profileElement.find('#secondsColor').val(hRGB2HEX(profileData.config.colorSecondRGB));
}


function changeAppConfig(key, value) {
	dataToChange = {
			"commandType": "set",
			"dat": {
				"applications": [
					{
						"appId": 1,
					}
				]
				}
			};
	dataToChange.dat.applications[0][key] = value;

	$.ajax({
			  type: "POST",
			  url: "/set",
			  contentType: "application/json",
			  data: JSON.stringify(dataToChange),
			  dataType: "json"
			});

}

function changeDefaultProfile(key, value) {
	dataToChange = {
			"commandType": "set",
			"dat": {
				"applications": [
					{
						"appId": 1,
						"defaultProfile": {}
					}
				]
				}
			};

	dataToChange.dat.applications[0].defaultProfile[key] = value;

	$.ajax({
			  type: "POST",
			  url: "/set",
			  contentType: "application/json",
			  data: JSON.stringify(dataToChange),
			  dataType: "json"
			});
}

function changeProfile(key, value, profile) {
	profileIndex = profile.parent('.groupBox').attr('profileIndex');

	dataToChange = {
		"commandType": "set",
		"dat": {
			"applications": [
				{
					"appId": 1,
					"userProfiles": []
				}
			]
		}
	}

	//create an empty array to point to the right profile
	for (i=0;i<=profileIndex;i++) {
		dataToChange.dat.applications[0].userProfiles.push({});
	}

	dataToChange.dat.applications[0].userProfiles[profileIndex]['config'] = {};
	dataToChange.dat.applications[0].userProfiles[profileIndex]['config'][key] = value;

	$.ajax({
		  type: "POST",
		  url: "/set",
		  contentType: "application/json",
		  data: JSON.stringify(dataToChange),
		  dataType: "json"
		});
}

function changeProfileMeta(key, value, profile) {
	profileIndex = profile.parent('.groupBox').attr('profileIndex');

	dataToChange = {
		"commandType": "set",
		"dat": {
			"applications": [
				{
					"appId": 1,
					"userProfiles": []
				}
			]
		}
	}

	//create an empty array to point to the right profile
	for (i=0;i<=profileIndex;i++) {
		dataToChange.dat.applications[0].userProfiles.push({});
	}

	dataToChange.dat.applications[0].userProfiles[profileIndex] = {};
	dataToChange.dat.applications[0].userProfiles[profileIndex][key] = value;

	$.ajax({
		  type: "POST",
		  url: "/set",
		  contentType: "application/json",
		  data: JSON.stringify(dataToChange),
		  dataType: "json"
		});
}

function changeProfileTime(key, value, profile) {
	profileIndex = profile.parent('.groupBox').attr('profileIndex');

	dataToChange = {
		"commandType": "set",
		"dat": {
			"applications": [
				{
					"appId": 1,
					"userProfiles": []
				}
			]
		}
	}

	//create an empty array to point to the right profile
	for (i=0;i<=profileIndex;i++) {
		dataToChange.dat.applications[0].userProfiles.push({});
	}

	dataToChange.dat.applications[0].userProfiles[profileIndex] = {};
	dataToChange.dat.applications[0].userProfiles[profileIndex][key] = {
		"hours": hGetHours(value),
		"minutes": hGetMinutes(value)
	};

	$.ajax({
	  type: "POST",
	  url: "/set",
	  contentType: "application/json",
	  data: JSON.stringify(dataToChange),
	  dataType: "json"
	});

}

function enableProfileClick(toggle) {
	profileIndex = toggle.parent('.groupBox').attr('profileIndex');
	toggleIcon = toggle.find("i");

	hEnableToggle(toggleIcon, toggleIcon.hasClass('fa-toggle-off'));
	changeProfileMeta('userProfileEnabled',toggleIcon.hasClass('fa-toggle-on'),toggleIcon.parent());
}

function removeProfileClick(trash) {
	if (confirm("Profil wirklich löschen?")) {
		profileIndex = trash.parent('.groupBox').attr('profileIndex');

		dataToChange = {
			"commandType": "remove",
			"dat": 
			{
	    		"applications": [
	        		{
	        			"appId": 1,
	        			"userProfiles":  {"index": parseInt(profileIndex)}
	    			}
				]
			}
		}

		$.ajax({
			  type: "POST",
			  url: "/set",
			  contentType: "application/json",
			  data: JSON.stringify(dataToChange),
			  dataType: "json"
			});
	}
}

function addProfileClick() {
	command = {
		"commandType": "add",
		"dat": 
		{
    		"applications": [
        		{
        			"appId": 1,
        			"userProfiles":  "dummy"
    			}
			]
		}
	}

	$.ajax({
		  type: "POST",
		  url: "/set",
		  contentType: "application/json",
		  data: JSON.stringify(command),
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
	hLoadDropdownFromServer('#timezoneCategory', "/timesettings/timezonecategories");
}

// ----- Page functions -----------------------------------

function timezoneUpdateTimezones() {
	var category = $('#timezoneCategory').val();
	hLoadDropdownFromServer('#timezone', '/timesettings/timezones/' + category);
}

function setTimezone() {
	var data = {'category': $('#timezoneCategory').val(), 'timezone': $('#timezone').val()};

	$.ajax({
		  type: "POST",
		  url: "/timesettings/timezone",
		  contentType: "application/json",
		  data: JSON.stringify(data),
		  dataType: "json"
		}).done(function() {alert("Zeitzone gesetzt");});
}

function appClockStart() {
	alert("starting clock application... (not implemented yet)");
}

function connectToWifi() {
	data = {'ssid': $('#wifiName').val(), 'pw': $('#wifiPassword').val()};

	if (confirm("Die Uhr wird versuchen sich mit dem WiFi zu verbinden. Diese Seite wird danach nicht mehr reagieren!")) {
		showPage('#pLoading');
		$.ajax({
		  type: "POST",
		  url: "/wifisetup",
		  contentType: "application/json",
		  data: JSON.stringify(data),
		  dataType: "json"
		});
	}	
}

function createProfile(i) {
	template = $('#cAppProfile_template').clone();
	template.attr('id','cAppProfile_' + i);
	template.attr('profileIndex', i);
	template.appendTo('#pClock #profiles');
	template.addClass('userProfile');
	template.find('.heading').text("Nutzerprofil " + (i + 1));

	return template
}

// ---- Helper Functions ---------------------------------

function hAddOption(elementId, optionText, optionValue) {
	$(elementId).append(`<option value="${optionValue}"> 
	                           ${optionText} 
	                      </option>`);	
}

function hLoadDropdownFromServer(dropdownId, url) {
	$.get(url, function(data, status){
	    if (status == 'success') {
	    	$(dropdownId + ' option').each(function(){$(this).remove();});
	    	jData = JSON.parse(data);
	    	for (i=0; i<jData.length; i++) {
				hAddOption(dropdownId, jData[i], jData[i]);
	    	}
	    	$(dropdownId).change();
	    }
	});		
}
function hEnableToggle(toggleElement, state) {
	if (state) {
		toggleElement.removeClass('fa-toggle-off');
		toggleElement.addClass('fa-toggle-on');
	} else {
		toggleElement.removeClass('fa-toggle-on');
		toggleElement.addClass('fa-toggle-off');
	}
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

function hTimeToString(time) {
	var hours;
	var minutes;

	hours = time.hours;
	if (hours <= 9)
		hours = "0" + hours;

	minutes = time.minutes;
	if (minutes <= 9)
		minutes = "0" + minutes;

	return (hours + ":" + minutes);

}

function hGetHours(strTime) {
	return parseInt(strTime.split(':')[0]);
}

function hGetMinutes(strTime) {
	return parseInt(strTime.split(':')[1]);
}