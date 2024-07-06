let map = L.map('map').setView([20, 0], 2); // Initial view set to world map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
let marker;

// Initialize Google Places Autocomplete
function initAutocomplete() {
    const input = document.getElementById('location');
    const autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.setFields(['geometry', 'name']);

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (!place.geometry) {
            alert("No details available for input: '" + place.name + "'");
            return;
        }

        const lat = place.geometry.location.lat();
        const lng = place.geometry.location.lng();

        map.setView([lat, lng], 13); // Zoom to the specified location

        if (marker) {
            marker.setLatLng([lat, lng]);
        } else {
            marker = L.marker([lat, lng]).addTo(map);
        }
    });
}

// Show the selected location on the map
function showLocation() {
    const location = document.getElementById('location').value;
    fetch('/get_spots', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ location })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const lat = parseFloat(data.lat);
            const lon = parseFloat(data.lon);

            map.setView([lat, lon], 13); // Zoom to the specified location

            if (marker) {
                marker.setLatLng([lat, lon]);
            } else {
                marker = L.marker([lat, lon]).addTo(map);
            }
        }
    });
}

// Find tourist spots near the selected location
function findSpots() {
    const location = document.getElementById('location').value;
    fetch('/get_spots', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ location })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const spots = data.spots;
            const spotsList = document.getElementById('spots');
            spotsList.innerHTML = '';
            spots.forEach(spot => {
                const li = document.createElement('li');
                li.textContent = spot;
                spotsList.appendChild(li);
            });
        }
    });
}

// Initialize the map and autocomplete once the page is fully loaded
window.onload = () => {
    initAutocomplete();
};
