if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(function(position) {
      var latitudeInput = document.getElementById('latitude');
      var longitudeInput = document.getElementById('longitude');

      // Set latitude and longitude values in hidden inputs
      latitudeInput.value = position.coords.latitude;
      longitudeInput.value = position.coords.longitude;
  });
} else {
  console.error('Geolocation is not supported by this browser');
}