/**
 * Created by Yuan on 2016/2/14.
 */

function update_total(){

        window.setInterval(function(){
            $.getJSON('/election_api/total', function(data) {
            odometer.innerHTML=data.total;
            });
        }, 5000);
}

update_total();

