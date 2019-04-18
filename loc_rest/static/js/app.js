function getApiData(addressline1, addressline2, zipcode, cuisine) {
  var scrape_url = "apiScrape"
  // var source_url = "apiSource"
  var scrape_url = `${scrape_url}/${addressline1}/${addressline2}/${zipcode}/${cuisine}`
  // var source_udrl = `${source_url}/${addressline1}/${addressline2}/${zipcode}/${cuisine}`

  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function(){
    if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
      // createGraph1(JSON.parse(xhr.responseText))
      createGraph(JSON.parse(xhr.responseText))
      // createAntpath(JSON.parse(xhr.responseText))
    } 
  }; 
  xhr.open("GET", scrape_url, true); 
  xhr.send("");
};

// function createGraph1(graphdata){
//   console.log(`In Graph1`)
//   console.log(graphdata)
//   console.log(`1`)
//   console.log(graphdata[0])
//   console.log(`2`)
//   console.log(graphdata[0].source)
//   console.log(`3`)
//   console.log(graphdata[1].detail)

//   detaildata = graphdata[1].detail
//   console.log(`4`)
//   console.log(detaildata[1].address)

//   sourcedata = graphdata[0].source
//   console.log(`5`)
//   console.log(sourcedata.zipcode)

// }

function createGraph(graphdata){
  sourcedata = graphdata[0].source
  detaildata = graphdata[1].detail
  // console.log(sourcedata)
  // console.log(sourcedata.lat)
  // console.log(detaildata)

  var myMap = L.map("map-id", {
    center: [sourcedata.lat, sourcedata.lng],
    zoom: 10
  });
  
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 14,
    id: "mapbox.streets",
    accessToken: API_KEY
  }).addTo(myMap);

  var redMarker = new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    // shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    // iconSize: [25, 41],
    // iconAnchor: [12, 41],
    // popupAnchor: [1, -34],
    // shadowSize: [41, 41]
  });

  var greenMarker = new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    // shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    // iconSize: [25, 41],
    // iconAnchor: [12, 41],
    // popupAnchor: [1, -34],
    // shadowSize: [41, 41]
  });

  // Add source data
  var sourcemarker = L.marker([sourcedata.lat, sourcedata.lng], {
    draggable: false,
    icon : greenMarker,
    // markerColor:'green',
    // fillColor: 'green'
  })
  .bindPopup("<h5> Starting Point </h5>")
  .addTo(myMap);

  // Add resteraunt data
  for (var i = 0; i < detaildata.length; i++) {
      var destinationmarker = L.marker([detaildata[i].lat, detaildata[i].lng], {
        draggable: false,
        icon : redMarker,
        // markerColor:"red",
      })
      .bindPopup("<h5>" + detaildata[i].resteraunt + "<hr> Distance: " + detaildata[i].distance + "<br> Duration: " + detaildata[i].duration + "</br> </h5>")
      .addTo(myMap);
  }
};

function createAntpath(graphdata){
  sourcedata = graphdata[0].source
  detaildata = graphdata[1].detail

  var myMap = L.map("map-id", {
    center: [sourcedata.lat, sourcedata.lng],
    zoom: 10
  });
  
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href='https://www.openstreetmap.org/'>OpenStreetMap</a> contributors, <a href='https://creativecommons.org/licenses/by-sa/2.0/'>CC-BY-SA</a>, Imagery © <a href='https://www.mapbox.com/'>Mapbox</a>",
    maxZoom: 14,
    id: "mapbox.streets",
    accessToken: API_KEY
  }).addTo(myMap);

  var redMarker = new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png'
  });

  var greenMarker = new L.Icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png'
  });

  // Add source data
  var sourcemarker = L.marker([sourcedata.lat, sourcedata.lng], {
    draggable: false,
    icon : greenMarker,
  })
  .bindPopup("<h5> Starting Point </h5>")
  .addTo(myMap);

  // Add resteraunt data
  for (var i = 0; i < detaildata.length; i++) {
      var destinationmarker = L.marker([detaildata[i].lat, detaildata[i].lng], {
        draggable: false,
        icon : redMarker,
      })
      .bindPopup("<h5>" + detaildata[i].resteraunt + "<hr> Distance: " + detaildata[i].distance + "<br> Duration: " + detaildata[i].duration + "</br> </h5>")
      .addTo(myMap);
  }

  latlngs = [
    [sourcedata.lat, sourcedata.lng],
    [detaildata[0].lat, detaildata[0].lng]
  ]

  const path = L.polyline.antPath(latlngs, {
  // const path = L.polyline(latlngs, {
    "pulseColor": "#FFFFFF",
    "paused": false,
    "reverse": false,
    "hardwareAccelerated": true,
    "dashArray": [
      50,
      50
    ],
    "delay": 500,
    "weight": 6,
    "color": "#002AFF"
  });

  myMap.addLayer(path);
  myMap.fitBounds(path.getBounds());
};

function validateInput(){
  // console.log(`validateInput Function`);

  // d3.event.preventDefault();

  var addressline1Element = d3.select("#addressLine1");
  var addressline2Element = d3.select("#addressLine2");
  var zipcodeElement = d3.select("#zipcode");
  var cuisineElement = d3.select("#cuisine");

  var inputaddressline1 = addressline1Element.property("value");
  var inputaddressline2 = addressline2Element.property("value");
  var inputzipcode = zipcodeElement.property("value");
  var inputcuisine = cuisineElement.property("value");

  if (inputaddressline2 == '' || inputaddressline2 == " ") {
    inputaddressline2 = " "
  }
  // console.log(`Input Data`);
  // console.log(inputaddressline1);
  // console.log(inputaddressline2);
  // console.log(inputzipcode);
  // console.log(inputcuisine);
  
  getApiData(inputaddressline1, inputaddressline2, inputzipcode, inputcuisine);
};

