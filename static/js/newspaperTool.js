/**
 * Created by Yuan on 2016/1/20.
 */
function analyze(stackname,link_hash){
    var articleAPI = "/db/article/"+stackname+"/"+link_hash;
    $.getJSON( articleAPI, {
    link_hash: link_hash
  })
    .done(function( data ) {
      $.each( data, function( i, news ) {
          $("#pop_text").text(article.text)
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