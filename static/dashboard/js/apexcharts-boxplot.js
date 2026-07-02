(function () {
    "use strict";

    /* basic boxplot chart */
    const basicoptions = {
        series: [
            {
                type: 'boxPlot',
                data: [
                    {
                        x: 'مهر 1395',
                        y: [54, 66, 69, 75, 88]
                    },
                    {
                        x: 'مهر 1396',
                        y: [43, 65, 69, 76, 81]
                    },
                    {
                        x: 'مهر 1397',
                        y: [31, 39, 45, 51, 59]
                    },
                    {
                        x: 'مهر 1398',
                        y: [39, 46, 55, 65, 71]
                    },
                    {
                        x: 'مهر 1399',
                        y: [29, 31, 35, 39, 44]
                    },
                    {
                        x: 'مهر 1400',
                        y: [41, 49, 58, 61, 67]
                    },
                    {
                        x: 'مهر 1401',
                        y: [54, 59, 66, 71, 88]
                    }
                ]
            }
        ],
        chart: {
            type: 'boxPlot',
            height: 320
        },
        title: {
            text: 'نمودار نقشه اصلی جعبه',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        grid: {
            borderColor: '#f2f5f7',
        },
        plotOptions: {
            boxPlot: {
                colors: {
                    upper: '#985ffd',
                    lower: '#ff49cd'
                }
            }
        },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        }
    };
    const basicchart = new ApexCharts(document.querySelector("#boxplot-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* boxplot with scatter chart */
    const boxplotoptions = {
        series: [
            {
                name: 'box',
                type: 'boxPlot',
                data: [
                    {
                        x: new Date('2017-01-01').getTime(),
                        y: [54, 66, 69, 75, 88]
                    },
                    {
                        x: new Date('2018-01-01').getTime(),
                        y: [43, 65, 69, 76, 81]
                    },
                    {
                        x: new Date('2019-01-01').getTime(),
                        y: [31, 39, 45, 51, 59]
                    },
                    {
                        x: new Date('2020-01-01').getTime(),
                        y: [39, 46, 55, 65, 71]
                    },
                    {
                        x: new Date('2021-01-01').getTime(),
                        y: [29, 31, 35, 39, 44]
                    }
                ]
            },
            {
                name: 'outliers',
                type: 'scatter',
                data: [
                    {
                        x: new Date('2017-01-01').getTime(),
                        y: 32
                    },
                    {
                        x: new Date('2018-01-01').getTime(),
                        y: 25
                    },
                    {
                        x: new Date('2019-01-01').getTime(),
                        y: 64
                    },
                    {
                        x: new Date('2020-01-01').getTime(),
                        y: 27
                    },
                    {
                        x: new Date('2020-01-01').getTime(),
                        y: 78
                    },
                    {
                        x: new Date('2021-01-01').getTime(),
                        y: 15
                    }
                ]
            }
        ],
        chart: {
            type: 'boxPlot',
            height: 320
        },
        colors: ['#985ffd', '#ff49cd'],
        grid: {
            borderColor: '#f2f5f7',
        },
        title: {
            text: 'طرح جعبه - نمودار پراکندگی',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        plotOptions: {
            boxPlot: {
                colors: {
                    upper: '#985ffd',
                    lower: '#ff49cd'
                }
            }
        },
        xaxis: {
            type: 'datetime',
            tooltip: {
                formatter: function (val) {
                    return new Date(val).getFullYear()
                }
            },
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        },
        tooltip: {
            shared: false,
            intersect: true
        },
        legend: {
            show: false
        }
    };
    const boxplotchart = new ApexCharts(document.querySelector("#boxplot-scatter"), boxplotoptions);
    if(boxplotchart) boxplotchart.render();

    /* horizontal boxplot chart */
    const horizontaloptions = {
        series: [
            {
                data: [
                    {
                        x: 'دسته 1',
                        y: [54, 66, 69, 75, 88]
                    },
                    {
                        x: 'دسته 2',
                        y: [43, 65, 69, 76, 81]
                    },
                    {
                        x: 'دسته 3',
                        y: [31, 39, 45, 51, 59]
                    },
                    {
                        x: 'دسته 4',
                        y: [39, 46, 55, 65, 71]
                    },
                    {
                        x: 'دسته 5',
                        y: [29, 31, 35, 39, 44]
                    },
                    {
                        x: 'دسته 6',
                        y: [41, 49, 58, 61, 67]
                    },
                    {
                        x: 'دسته 7',
                        y: [54, 59, 66, 71, 88]
                    }
                ]
            }
        ],
        chart: {
            type: 'boxPlot',
            height: 320
        },
        title: {
            text: 'نمودار طرح جعبه افقی',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        plotOptions: {
            bar: {
                horizontal: true,
                barHeight: '50%'
            },
            boxPlot: {
                colors: {
                    upper: '#e9ecef',
                    lower: '#f8f9fa'
                }
            }
        },
        grid: {
            borderColor: '#f2f5f7',
        },
        xaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-xaxis-label',
                },
            }
        },
        yaxis: {
            labels: {
                show: true,
                style: {
                    colors: "#8c9097",
                    fontSize: '11px',
                    fontWeight: 600,
                    cssClass: 'apexcharts-yaxis-label',
                },
            }
        },
        stroke: {
            colors: ['#6c757d']
        }
    };
    const horizontalchart = new ApexCharts(document.querySelector("#boxplot-horizontal"), horizontaloptions);
    if(horizontalchart) horizontalchart.render();

})();