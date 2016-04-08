/**
 * Created by Yuan on 2016/1/19.
 */
page=parseInt(window.location.href.slice(-1));
//var hiddenobj = document.getElementById("stackname");
//var stackname = hiddenobj.value;
var newsAPI = "/db/news/"+page;
  $.getJSON( newsAPI, {
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
          var source_site=news.source.substr(news.source.indexOf('.')+1,news.source.indexOf('.',3))
          var source="<div class='panel-footer'> Source: <a href="+news.source+">"+source_site+"</a></div>";
          var info_btn='<button id="'+news.link_hash+'"type="button" class="btn btn-info" onclick="analyze(this.id)">Info</button>';
          $("#news_list").prepend(
              panel+panel_heading+title+div_end+article_url+panel_body+text+div_end+a_end+keywords+source+info_btn+div_end
          )
      });
    });


page=parseInt(window.location.href.slice(-1));
var l1=""
var l2=""
if(page>1){
    l1 ='<li  id="'+(page-1)+'"><a href="./'+(page-1)+'" data-original-title="" title="">'+(page-1)+'</a></li>';
}
if(page>2){
    l2 ='<li  id="'+(page-2)+'"><a href="./'+(page-2)+'" data-original-title="" title="">'+(page-2)+'</a></li>';
}
//var l2 ='<li id="'+(page-2)+'"><a href="./'+(page-2)+'" data-original-title="" title="">'+(page-2)+'</a></li>';
var c0 ='<li class="active" id="'+page+'"><a href="./'+page+'" data-original-title="" title="">'+page+'</a></li>';
var r1 ='<li id="'+(page+1)+'"><a href="./'+(page+1)+'" data-original-title="" title="">'+(page+1)+'</a></li>';
var r2 ='<li id="'+(page+2)+'"><a href="./'+(page+2)+'" data-original-title="" title="">'+(page+2)+'</a></li>';
var r3 ='<li id="'+(page+3)+'"><a href="./'+(page+3)+'" data-original-title="" title="">'+(page+3)+'</a></li>';

$("#paging").prepend(l2+l1+c0+r1+r2+r3)