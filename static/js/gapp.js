$(document).ready(function(){
            var data=[];
            var map = L.map('map').setView([19.481924, 19.049447], 3);

        tcount=0;

            L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
                    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>',
                    maxZoom: 18
            }).addTo(map);

    //bright map
    //        L.tileLayer( 'http://{s}.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.png', {
    //        attribution: '&copy; <a href="http://osm.org/copyright" title="OpenStreetMap" target="_blank">OpenStreetMap</a> contributors | Tiles Courtesy of <a href="http://www.mapquest.com/" title="MapQuest" target="_blank">MapQuest</a> <img src="http://developer.mapquest.com/content/osm/mq_logo.png" width="16" height="16">',
    //        subdomains: ['otile1','otile2','otile3','otile4']
    //        }).addTo( map );

             function getColor(d) {
                return d > 0.4  ? '#1A6A34' :
                       d > 0.2  ? '#8CBD31' :
                       d > 0  ? '#FEDE00' :
                       d > -0.1  ? '#FFDB4E' :
                       d > -0.2   ? '#E88A3C' :
                       d > -0.3   ? '#FF4A47' :
                           d > -1   ? '#DA110D' :
                       '#FEDE00' ;
            };

            // Set the dimensions of the canvas / graph
            var margin = {top: 30, right: 20, bottom: 30, left: 30},
                width = 500 - margin.left - margin.right,
                height = 250 - margin.top - margin.bottom;

            // Parse the date / time
            var parseDate = d3.time.format("%d-%b-%y").parse;
                        
            // Set the ranges
            var x = d3.scale.linear().range([0, width]);
            var y = d3.scale.linear().range([height, 0]);

            var yMin = d3.min(data);
            var yMax = d3.max(data);

            // Define the axes
            var xAxis = d3.svg.axis().scale(x)
                .orient("bottom").ticks(5);

            var yAxis = d3.svg.axis().scale(y)
                .orient("left").ticks(5);

            // Define the line
            var valueline = d3.svg.line()
                .x(function(d,i) { return x(i); })
                .y(function(d) { return y(d); });
                
            // Adds the svg canvas
            var svg = d3.select("#chart")
                .append("svg")
                    .attr("width", width + margin.left + margin.right)
                    .attr("height", height + margin.top + margin.bottom)
                .append("g")
                    .attr("transform", 
                          "translate(" + margin.left + "," + margin.top + ")");



            // Scale the range of the data
            x.domain(d3.extent(data, function(d,i) { return i ; }));
            y.domain([0, d3.max(data, function(d) { return d })]);

            // Add the valueline path.
            svg.append("path")
                .attr("class", "line")
                .attr("d", valueline(data));                

            // Add the X Axis
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis)
                .append("text")
                  .attr("x", width)
                  .attr("y", -18)
                  .attr("dy", ".90em")
                  .style("text-anchor", "end")
                  .text("5*Seconds");

            // Add the Y Axis
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis)
                .append("text")
                  .attr("transform", "rotate(-90)")
                  .attr("y", 6)
                  .attr("dy", ".71em")
                  .style("text-anchor", "end")
                  .text("Tweets");



        window.setInterval(function(){
            $.getJSON('/db/pool', function(data) {
    makeGraphs(data)
});
        }, 5000);

    function makeGraphs(projectsJson) {

        speed=projectsJson.length/5;
        $('#speed').html(speed);
        updateData(speed);
        $('#count').html(tcount+=projectsJson.length);
        //L.circleMarker([8,9], geojsonMarkerOptions)
        //            .addTo(map).bindPopup("<div class='row'><div class='col-md-3'><img src=" + msg.profile_image + " class='img-rounded'></div><div class='col-md-9'><h5 style='color:black'>" + msg.username + "</h5><p style='color:grey'>" + msg.status + "</p></div></div>");

        for(i=0; i<projectsJson.length;i++) {
            msg = JSON.parse(projectsJson[i]);
            //    if(msg.coordinates){
            //        alert("haha0");
            //    }

            var geojsonMarkerOptions = {
                radius: 5,
                fillColor: getColor(msg.score),
                color: getColor(msg.score),
                weight: 1,
                opacity: 0.1,
                fillOpacity: 0.5
                };

            var coordinates=[null,null];
            if(msg.coordinates!=null){
                coordinates[1]=msg.coordinates.coordinates[0];
                coordinates[0]=msg.coordinates.coordinates[1];

            }
            else if(msg.place!=null){
                if(msg.place.bounding_box!=null) {
                    coordinates[1] = (msg.place.bounding_box.coordinates[0][0][0] + msg.place.bounding_box.coordinates[0][2][0]) / 2;
                    coordinates[0] = (msg.place.bounding_box.coordinates[0][0][1] + msg.place.bounding_box.coordinates[0][2][1]) / 2;
                }
            }
            $('#log').prepend('<br>Received : ' + msg.text);
            if (coordinates[0]!=null) {
                L.circleMarker(coordinates, geojsonMarkerOptions)
                    .addTo(map).bindPopup("<div class='row'><div class='col-md-3'><img src=" + msg.user.profile_image_url + " class='img-rounded'></div><div class='col-md-9'><h5 style='color:black'>" + msg.user.name + "</h5><p style='color:grey'>" + msg.text + "</p></div></div>");
            }
        }

    }


            //namespace = '/gmonitor'; // change to an empty string to use the global namespace

            // the socket.io documentation recommends sending an explicit package upon connection
            // this is specially important when using the global namespace
            var socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');

            socket.on('connect', function() {
                    socket.emit('joined', {});
                });
            socket.on('status', function(data) {
                    //$('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
                    //$('#chat').scrollTop($('#chat')[0].scrollHeight);
                });
            //socket.on('message', function(data) {
            //        $('#chat').val($('#chat').val() + data.msg + '\n');
            //        $('#chat').scrollTop($('#chat')[0].scrollHeight);
            //    });


            //connect
            //socket.on('connect', function() {
            //    socket.emit('tracking', {});
            //});

            // event handler for server sent data
            // the data is displayed in the "Received" section of the page
            socket.on('my response', function(msg) {
                $('#log').prepend('<br>Received #' + msg.count + ': ' + msg.status);
            });

            //socket.on('error', function(msg) {
            //    $('#log').append('<br>Received #' + msg.count + ': ' + msg);
            //});
            
            socket.on('message', function(msg) {
                //console.log(msg);
                $('#count').html(msg.count);
                if (typeof(msg.speed) != 'undefined') {
                    $('#speed').html(msg.speed);
                    //console.log(msg);
                    updateData(msg.speed);
                    $(".subjetivity").animate({width: msg.subjetivity_avg*100+"%"});    
                    $(".polarity").animate({width: msg.polarity_avg*100+"%"});                        
                                        
                };
                
                
                var geojsonMarkerOptions = {
                radius: 3,
                fillColor: getColor(msg.polarity),
                color: "#FFBE08",
                weight: 1,
                opacity: 0.1,
                fillOpacity: 0.5
                };
                L.circleMarker(msg.coordinates,geojsonMarkerOptions)
                 .addTo(map).bindPopup("<div class='row'><div class='col-md-3'><img src="+msg.profile_image+" class='img-rounded'></div><div class='col-md-9'><h5 style='color:black'>"+msg.username+"</h5><p style='color:grey'>"+msg.status+"</p></div></div>");   
                               
            });    


            function updateData(speed) {

            // Get the data again
            
            data.push(speed);

            // Scale the range of the data again 
            x.domain(d3.extent(data, function(d,i) { return i; }));
            y.domain([0, d3.max(data, function(d) { return d; })]);

            // Select the section we want to apply our changes to
            var svg = d3.select("#chart").transition();

            // Make the changes
                svg.select(".line")   // change the line
                    .duration(200)
                    .attr("d", valueline(data));
                svg.select(".x.axis") // change the x axis
                    .duration(200)
                    .call(xAxis);
                svg.select(".y.axis") // change the y axis
                    .duration(200)
                    .call(yAxis);

            
        };         

       

 });