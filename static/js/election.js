/**
 * Created by Yuan on 2016/2/14.
 */

function update_total() {

    window.setInterval(function () {
        $.getJSON('/election_api/total', function (data) {
            odometer.innerHTML = data.total;
        });
    }, 5000);
}
var summary = new Object();
function get_impact_init() {
    $.getJSON('/election_api/impact_lastday', function (data) {
        summary = data
        loadGoogleChart();

    });
}

function get_impact_last_day() {
    $.getJSON('/election_api/impact_lastday', function (data) {
        summary = data
        drawStuff();
    });
}

function get_impact_last_3day() {
    $.getJSON('/election_api/impact_last3day', function (data) {
        summary = data
        drawStuff();
    });
}


function get_impact_last_week() {
    $.getJSON('/election_api/impact_week', function (data) {
        summary = data
        drawStuff();
    });
}


function get_impact_max() {
    $.getJSON('/election_api/impact', function (data) {
        summary = data
        drawStuff();
    });
}


function loadGoogleChart() {
    google.charts.load('current', {'packages': ['bar']});
    google.charts.setOnLoadCallback(drawStuff);
}


function drawStuff() {

    var data = new google.visualization.arrayToDataTable([
        ['Candidate', 'Plain Score', 'Adjusted Impact Score'],
        ['Donald Trump', summary.Trump.score, summary.Trump.impact],
        ['Hillary Clinton', summary.Clinton.score, summary.Clinton.impact],
        ['Bernie Sanders', summary.Sanders.score, summary.Sanders.impact],
        ['Ted Cruz', summary.Cruz.score, summary.Cruz.impact]
    ]);


    var options = {
        width: 900,
        chart: {
            title: 'Twitter Sentiment',
            subtitle: 'Plain Score on the left, Adjusted Impact Score on the right'
        },
        series: {
            0: {axis: 'Plain Score'}, // Bind series 0 to an axis named 'distance'.
            1: {axis: 'Adjusted Impact Score'} // Bind series 1 to an axis named 'brightness'.
        },
        axes: {
            y: {
                distance: {label: 'Plain Score'}, // Left y-axis.
                brightness: {side: 'right', label: 'Adjusted Impact Score'} // Right y-axis.
            }
        }
    };

    var chart = new google.charts.Bar(document.getElementById('dual_y_div'));
    chart.draw(data, options);
    $("#loading").hide();

};

function show_cloud(wordscount) {
    $('#individual_cloud').jQCloud(wordscount, {
        shape: 'rectangular',
        classPattern: null,
        fontSize: {
            from: 0.1,
            to: 0.02
        }
    });
}


function show_individual_cloud(candidate) {
    url='/api/election_frequent/'+candidate;
    $.getJSON(url, function (data) {
        show_cloud(data)
    });
}


$(document).ready(function () {
    $("#tab1,#tab2,#tab3,#tab4").click(function () {
        $("#tab1").removeClass("active");
        $("#tab2").removeClass("active");
        $("#tab3").removeClass("active");
        $("#tab4").removeClass("active");
        $(this).addClass("active");
        $("#loading").show();
    });
});


update_total();
get_impact_init();


