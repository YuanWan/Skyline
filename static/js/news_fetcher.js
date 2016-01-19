/**
 * Created by Yuan on 2016/1/19.
 */


var newsAPI = "/db/news";
  $.getJSON( newsAPI, {
    tags: "mount rainier",
    tagmode: "any",
    format: "json"
  })
    .done(function( data ) {
      $.each( data, function( i, news ) {
          var anchor = "<a href="+news.url+">";
          var a_end = "</a>";
          var panel='<div class="panel panel-primary">';
          var panel_heading='<div class="panel-heading">';
          var panel_body='<div class="panel-body">'
          var title = "<h3 class='panel-title'>"+ news.title +"";
          var text= news.text.substr(0,500);
          var div_end = '</div>';
          $("#news_list").prepend(
              anchor+panel+panel_heading+title+div_end+panel_body+text+div_end+div_end+a_end
          )
      });
    });