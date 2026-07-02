(function () {
    "use strict";

    /* basic radar chart */
    const basicoptions = {
        series: [{
            name: 'Series 1',
            data: [80, 50, 30, 40, 100, 20],
        }],
        chart: {
            height: 320,
            type: 'radar',
        },
        title: {
            text: 'نمودار رادار اساسی',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        colors: ["#985ffd"],
        xaxis: {
            categories: ['مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        }
    };
    const basicchart = new ApexCharts(document.querySelector("#radar-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* radar chart with multiple series */
    const multipleoptions = {
        series: [{
            name: 'سری 1',
            data: [80, 50, 30, 40, 100, 20],
        }, {
            name: 'سری 2',
            data: [20, 30, 40, 80, 20, 80],
        }, {
            name: 'سری 3',
            data: [44, 76, 78, 13, 43, 10],
        }],
        chart: {
            height: 320,
            type: 'radar',
            dropShadow: {
                enabled: true,
                blur: 1,
                left: 1,
                top: 1
            }
        },
        title: {
            text: 'نمودار رادار - سری چند',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        colors: ['#985ffd', '#ff49cd', '#fdaf22'],
        stroke: {
            width: 2
        },
        fill: {
            opacity: 0.1
        },
        markers: {
            size: 0
        },
        xaxis: {
            categories: ['2011', '2012', '2013', '2014', '2015', '2016']
        }
    };
    const multiplechart = new ApexCharts(document.querySelector("#radar-multiple"), multipleoptions);
    if(multiplechart) multiplechart.render();

    /* radar chart polygn fill */
    const polygnoptions = {
        series: [{
            name: 'سری 1',
            data: [20, 100, 40, 30, 50, 80, 33],
        }],
        chart: {
            height: 320,
            type: 'radar',
        },
        dataLabels: {
            enabled: true
        },
        plotOptions: {
            radar: {
                size: 80,
                polygons: {
                    strokeColors: '#e9e9e9',
                }
            }
        },
        title: {
            text: 'رادار با پر کردن چند ضلعی',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        colors: ['#ff49cd'],
        markers: {
            size: 4,
            colors: ['#fff'],
            strokeColor: '#ff49cd',
            strokeWidth: 2,
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val
                }
            }
        },
        xaxis: {
            categories: ['یک شنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه']
        },
        yaxis: {
            tickAmount: 7,
            labels: {
                formatter: function (val, i) {
                    if (i % 2 === 0) {
                        return val
                    } else {
                        return ''
                    }
                }
            }
        }
    };
    const polygnchart = new ApexCharts(document.querySelector("#radar-polygon"), polygnoptions);
    if(polygnchart) polygnchart.render();

})();