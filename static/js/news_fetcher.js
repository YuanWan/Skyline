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
          var article_url = "<a href="+news.url+">";
          var a_end = "</a>";
          var panel='<div class="panel panel-primary">';
          var panel_heading='<div class="panel-heading">';
          var panel_body='<div class="panel-body">';
          var title = '<h3 class="panel-title">'+ news.title +"</h3>";
          var text= news.text.substr(0,500);
          var div_end = '</div>';
          var keywords="";
          if(news.keywords[0]!=""){
              keywords="<div class='panel-footer'>"+"Keywords: "+news.keywords+"</div>";
          }
          var source="<div class='panel-footer'> Source: <a href="+news.source+">"+news.source+"</a></div>";
          $("#news_list").prepend(
              panel+panel_heading+title+div_end+article_url+panel_body+text+div_end+a_end+keywords+source+div_end
          )
      });
    });