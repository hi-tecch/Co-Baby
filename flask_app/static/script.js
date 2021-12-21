// DAILY WEATHER CHECKER-FRONT END ONLY: NO CHANGE TO THE BACKEND. JUST WRITTEN INTO HTML AND JS
var apiDiv = document.querySelector("#apis");
var currentCity = ""; // this holds the city we search for as a string. also gets passed in to the async function as a url parameter

function getCity(element) { // this gets the usernames and stores in the variable above
    currentCity = element.value;
}

function makeCityInfo(data) { // allows us to create new HTML so we can display the API response on the page
// our container for the API response. create the HTML elements inside specific to the reponse info we want to display.
    var spot =  `<div id="apis">
                    <p>City: ${data.name}
                    <p>High: ${data.main.temp_max}</p>
                    <p>Low: ${data.main.temp_min}</p>
                    <p>Weather: ${data.weather[0].description}</p>
                </div>`
    console.log(spot)
    return spot; // we want to return it so the HTML can be built.
}

async function showCityAsync(){ // this was used before the functions below 
    // The await keyword lets js know that it needs to wait until it gets a response back to continue.
    var response = await fetch("https://api.openweathermap.org/data/2.5/weather?q="+currentCity+"&units=imperial&appid=ccabb67fa9582da15360454e1ba234f7"); // API Call
    // We then need to convert the data into JSON format.
    var cityData = await response.json(); // converts the searched info to a JSON format
    console.log(cityData);
    apiDiv.innerHTML = makeCityInfo(cityData); // made the response variable equal to this because:
    //innerHTMl, when given a string that looks like HTML, will try to turn the string into HTML.
}
// END OF DAILY WEATHER CHECKER

config={
    enableTime: true,
    dateFormat: "Y-m-d H:i",
    altInput:true,
    altFormat:"F j, Y (h:S K)"
    }
                  
flatpickr("input[type=datetime-local]", config);

