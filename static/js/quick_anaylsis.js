/**
 * Created by Yuan on 2016/1/21.
 */
function submit_text(){
    var text = $("#text_content")[0].value;
    $.post( "/api/quick/", { type: "text", content: text })
  .done(function( data ) {
        draw_analysis(data);
  });
}

function draw_analysis(data){
    var table_content = "";
    data=JSON.parse(data);
    for (i=0;i<data.length-1;i++){
        var row = "<tr><td>"+data[i].text+"</td><td>"+data[i].weight+"</td></tr>"
        table_content=table_content+row;
    }

    $("#wordtable")[0].innerHTML=table_content;

    p.refresh(data[data.length-1].pa_polarity*10);
    s.refresh(data[data.length-1].pa_subjectivity*10);

}



var s = new JustGage({
    id: "subjectivity",
    value: 6,
    min: -10,
    max: 10,
    title: "Subjectivity"
  });

var p = new JustGage({
    id: "polarity",
    value: 7,
    min: -10,
    max: 10,
    title: "Polarity",
    reverse:true
  });