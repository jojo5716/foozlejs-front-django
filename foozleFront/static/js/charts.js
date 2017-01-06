google.charts.setOnLoadCallback(drawMultSeries);

function drawMultSeries() {
    var data = google.visualization.arrayToDataTable([
        ['Day', 'Errors'],
       {% for timestamp, values in chart_urls.items %}
            ['{{timestamp}}', {{values.errors}}]
         {% endfor%}
      ]);

    var options = {
        chartArea: {width: '50%'},
        hAxis: {
          title: 'Total issues',
          minValue: 0
        }
        
      };

      var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
      chart.draw(data, options);
    }