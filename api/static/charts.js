var chart1; // global

function requestData(addr, ser, tout) {
    $.ajax({
        url: addr,
        success: function(resp) {
            var point = JSON.parse(resp);
            var series = chart1.series[ser],
                x = (new Date()).getTime(),
                y = point["root"],
                shift = series.data.length > 30;
            // var d = new Date();
            // console.log("fetched date: " + d.getHours()+ "-" + d.getMinutes() + "-" + d.getSeconds());
            chart1.series[ser].addPoint([x, y], true, shift);
            setTimeout(requestData(addr, ser, tout), tout);
        },
        cache: false
    });
}

$(document).ready(function() {
    //Highcharts.chart('cpu', {
    var host_id = $('#host_id').data("host");
    var ram_url = "/util/single/ram/"+host_id;
    var cpu_url = "/util/single/cpu/"+host_id;
    console.log(host_id);
    console.log(ram_url);
    chart1 = new Highcharts.chart('cpu', {
        chart: {
            type: 'spline',
            animation: Highcharts.svg, // don't animate in old IE
            marginRight: 10,
            events: {
                load: requestData(ram_url, 0, 10000),
                load: requestData(cpu_url, 1, 10000)
            }
        },
        title: {
            text: 'Live RAM utilization data'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150
        },
        yAxis: {
            title: {
                text: '% utilization'
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            formatter: function() {
                return '<b>' + this.series.name + '</b><br/>' +
                    Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                    Highcharts.numberFormat(this.y, 2);
            }
        },
        plotOptions: {
            spline: {
                lineWidth: 1.5,
                states: {
                    hover: {
                        lineWidth: 1.5
                    }
                },
                marker: {
                    enabled: false
                }
            }
        },
        legend: {
            enabled: true
        },
        exporting: {
            enabled: false
        },
        series: [{
            name: 'cpu percent',
            type: 'spline',
            data: []
        }, {
            name: 'ram percent',
            data: []
        }]
    });

    //################################################################################//

    /*
        //Highcharts.chart('ram', {
        $('#ram').highcharts({
            chart: {
                type: 'spline',
                animation: Highcharts.svg, // don't animate in old IE
                marginRight: 10,
                events: {
                    load: function() {

                        // set up the updating of the chart each second

                        var series = this.series[0];
                        setInterval(function() {
                            $.get('/api/ram', function(resp) {
                                var json = JSON.parse(resp);
                                var x = (new Date()).getTime(), // current time
                                    y = json["utilization"];
                                series.addPoint([x, y], true, true);
                            });
                        }, 15000);
                    }
                }
            },
            title: {
                text: 'Live ram_percent data'
            },
            xAxis: {
                type: 'datetime',
                tickPixelInterval: 150
            },
            yAxis: {
                title: {
                    text: 'Value'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                formatter: function() {
                    return '<b>' + this.series.name + '</b><br/>' +
                        Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                        Highcharts.numberFormat(this.y, 2);
                }
            },
            legend: {
                enabled: false
            },
            exporting: {
                enabled: false
            },
            series: [{
                name: 'ram_percent',
                data: (function() {
                    // query first value
                    var data = [],
                        time = (new Date()).getTime(),
                        i;
                    /*var respon = $.get('/api/cpu', function(resp) {
                        var json = JSON.parse(resp);
                        return json["utilization"]
                    });
                    for (i = -19; i <= 0; i += 1) {
                        data.push({
                            x: time + i * 1000,
                            y: $.get('/api/ram', function(resp) {
                                var json = JSON.parse(resp);
                                return json["utilization"]
                            })
                        });
                    }
                    return data;
                }())
            }]
        });

    */






    // var cpuChart = Highcharts.chart('cpu', {});
    /*
    function updateStatus() {
        $.get('/api/cpu', function(resp) {
            console.log(resp);
            // cpuChart.update(resp.data)
            // sth with resp.data -> highcharts
        });
    }
    */









    //updateStatus(); setInterval(updateStatus, 30000);

    /*Highcharts.chart('container', {

        title: {
            text: 'Solar Employment Growth by Sector, 2010-2016'
        },

        subtitle: {
            text: 'Source: thesolarfoundation.com'
        },

        yAxis: {
            title: {
                text: 'Number of Employees'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },

        plotOptions: {
            series: {
                pointStart: 2010
            }
        },

        series: [{
            name: 'Installation',
            data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
        }, {
            name: 'Manufacturing',
            data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
        }, {
            name: 'Sales & Distribution',
            data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
        }, {
            name: 'Project Development',
            data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
        }, {
            name: 'Other',
            data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
        }]

    });*/
});
