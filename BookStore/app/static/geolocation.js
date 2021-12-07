// geolocation.js

// Geolocation
localStorage.setItem("lat", -1);
localStorage.setItem("long", -1);

function getLocation() {
  if(localStorage.getItem("lat") == -1 && localStorage.getItem("long") == -1) {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(setLocalCoords);
    }
  }
}

// Save current location in session storage
function setLocalCoords(position) {
  localStorage.setItem("lat", position.coords.latitude);
  localStorage.setItem("long", position.coords.longitude);
}

// Company's location
var CompanyLocationLat = 46.194796609701655
var CompanyLocationLong = 21.2969915903303
// Compute distance between current location and the company's location
function distanceToCompany() {
  const R = 6371e3; // metres
  const φ1 = CompanyLocationLat * Math.PI/180; // φ, λ in radians
  const φ2 = localStorage.getItem("lat") * Math.PI/180;
  const Δφ = (localStorage.getItem("lat")-CompanyLocationLat) * Math.PI/180;
  const Δλ = (localStorage.getItem("long")-CompanyLocationLong) * Math.PI/180;
  const a = Math.sin(Δφ/2) * Math.sin(Δφ/2) +
  Math.cos(φ1) * Math.cos(φ2) *
  Math.sin(Δλ/2) * Math.sin(Δλ/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const distance = Math.round((R * c)/1000); // in km
  return distance;
}

function writeDistanceToCompany() {
  if (localStorage.getItem("lat") == -1 && localStorage.getItem("long") == -1) {
    document.getElementById("distance").innerHTML = 
    "You cannot complete the delivery if you don't share your location!"
  } else {
    var distance = distanceToCompany()
    // 2500km from the company's headquarters in Romania covers most of Europe
    if (distance < 2500) {
      document.getElementById("distance").innerHTML = "<p>You are " + distance + 
      " km away from our company's headquarters. We can ship to your location for £2.</p>"
      document.getElementById("fin").style.display = "block";
    } else {
      document.getElementById("distance").innerHTML = "<div class=\"row border border-secondary\"></div><br>" + 
      "<p>You are " + distance + " km away from our company's headquarters.</p>" + 
      "<p class=\"text-danger\">Oh no! You're too far away! We can't ship to your current location! :( </p>"
    }
  }
}
