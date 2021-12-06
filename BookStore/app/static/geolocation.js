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