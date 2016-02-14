/**
 * Created by Yuan on 2016/2/14.
 */

function update_total(){

    var API = "/election_api/total";
    $.getJSON( API, {
  })
    .done(function( data ) {
        odometer.innerHTML=data.total;
    });
}

window.setTimeout(update_total(), 5000);