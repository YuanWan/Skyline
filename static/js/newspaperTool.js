/**
 * Created by Yuan on 2016/1/20.
 */

function draw_analysis(data){
    var table_content = "";
    data=JSON.parse(data);
    for (i=0;i<data.length-1;i++){
        var row = "<tr><td>"+data[i].text+"</td><td>"+data[i].weight+"</td></tr>"
        table_content=table_content+row;
    }

    $("#wordtable")[0].innerHTML=table_content;

    //p.refresh(data[data.length-1].pa_polarity*10);
    //s.refresh(data[data.length-1].pa_subjectivity*10);

}


function analyze(link_hash){
    //var stackname = $("#stackname")[0].value;
    var articleAPI = "/db/article/"+'spacex'+"/"+link_hash;
    var text;
    $.getJSON( articleAPI, {
    link_hash: link_hash
  })
    .done(function( data ) {
      $.each( data, function( i, news ) {
          text=news.text;
          $("#pop_text").text(text);
              $.post( "/api/quick/", { type: "text", content: text }).done(function( data ) {
            draw_analysis(data);
      });
    });

  });

    strtBlackout();
}

//This is the function that closes the pop-up
function endBlackout(){
$(".blackout").css("display", "none");
$(".msgbox").css("display", "none");
}

//This is the function that starts the pop-up
function strtBlackout(){
$(".msgbox").css("display", "block");
$(".blackout").css("display", "block");
}

//Sets the buttons to trigger the blackout on clicks
$(document).ready(function(){
$(".blackout").click(endBlackout); // close if click outside of popup
$(".closeBox").click(endBlackout); // close if close btn clicked

});