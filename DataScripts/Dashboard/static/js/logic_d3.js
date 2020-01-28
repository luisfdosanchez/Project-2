function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

function getDataDash3() {
    let vdisagg = d3.select("#disagg").property("value");
    arrDash3=[vdisagg];
    console.log(arrDash3);
    //console.log(geojsonData);
    dash3(arrDash3);
  }

  let dash3=(arrDash3)=>{
    d3.json("/api/dash3", {
        method: "POST",
        body: JSON.stringify({
            valueDisagg: arrDash3[0]
        }),
        headers:{
            "Content-type":"application/json"
        }
    }).then((d)=>{
        //console.log(d);
        d3.json("/static/data/estaciones-de-ecobici.geojson").then(f =>{
            //console.log(f.features);
            //console.log(f.features[1].properties.id);
            //console.log(d[1].station_begin);
            //console.log(d[1].station_end);
            var largo=d.length;
            var largogeoj=f.features.length;

            var startname=[];
            var startlat=[];
            var startlon=[];
            var endname=[];
            var endlat=[];
            var endlon=[];
            var trips=[];
            var time=[];
    
            for (var i = 0; i < largo; i++) {
                time.push(d[i].triptime);
                trips.push(d[i].tot);
                for (var j=0; j< largogeoj; j++) {
                    if (f.features[j].properties.id === d[i].station_begin) {
                        //console.log('begin');
                        //console.log(f.features[1].properties.id);
                        //console.log(d[1].station_begin); 
                        startname.push(f.features[j].properties.address);
                        startlat.push(f.features[j].properties.location_lat);
                        startlon.push(f.features[j].properties.location_lon);
                    } else if (f.features[j].properties.id === d[i].station_end) {
                        //console.log('end');
                        //console.log(f.features[1].properties.id);
                        //console.log(d[1].station_end); 
                        endname.push(f.features[j].properties.address);
                        endlat.push(f.features[j].properties.location_lat);
                        endlon.push(f.features[j].properties.location_lon);
                    } else {
                    }
                }
            }
            console.log(startname);
            console.log(time);
            console.log(endname); 
            for (var i = 0; i < largo; i++) {
            // Agregar rutas de cicloestación a cicloestación (parejas de quiebre)
            var line = [
                [startlat[i],startlon[i]],
                [endlat[i],endlon[i]],
            ]
            var avgtime=time[i].substr(14,2)+' m '+Math.round(10*parseFloat(time[i].substr(17)))/10+' s';
            // Plot every line (1, 2, 3, .....)
            var polyline = L.polyline(line, {
                color: "purple"
            }).bindPopup(`<h3>Start: ${startname[i]}</h3> <h3>End: ${endname[i]}</h3> <hr><h3>Trips ${numberWithCommas(trips[i])}</h3> <h3>Avg. time ${avgtime}</h3>`)
            .addTo(mymap);
        }
        })
    })
};


// Creating map object
var mymap = L.map('map', {
    center: [19.42,-99.16],
    zoom: 13
});

// Adding tile layer to the map
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    accessToken: API_KEY
}).addTo(mymap);

d3.json("/static/data/estaciones-de-ecobici.geojson").then(d =>{
    console.log(d.features);
    console.log(d.features[1].properties.id);
// Arreglo de markes con stations (looping through the DB)
    var bikeStations = d.features.map(M=>{
        L.marker([M.properties.location_lat, M.properties.location_lon])
        .bindPopup("<h3>" + M.properties.name + "</h3>" + "<hr>" + "<h3>" + M.properties.districtname + "</h3>", {
            maxWidth : "5px",
        }).addTo(mymap)
    })
});


//`<h3>${M.properties.address}</h3> <hr> <h3>${M.properties.districtname}</h3>`



// --------------------------
// --------------------------
// ESCUCHADORES
// --------------------------
// --------------------------

d3.select("#buttondash3").on("click", getDataDash3);