(function () {
    "use strict";

    /* basic polar area chart */
    const basicoptions = {
        series: [14, 23, 21, 17, 15, 10, 12, 17, 21],
        chart: {
            type: 'polarArea',
            height: 300
        },
        title: {
            text: 'سری',
            align: 'center',
            style: {
                fontSize: '16px',
                fontFamily: 'SHABNAM',
                color: '#333'
            }
        },
        stroke: {
            colors: ['#fff']
        },
        fill: {
            opacity: 0.8
        },
        legend: {
            position: 'bottom'
        },
        colors: ['#985ffd', '#ff49cd', '#fdaf22', '#32d484', '#00c9ff', '#ff6757', 'rgba(53, 181, 170,1)', 'rgb(190, 43, 235)'],
        responsive: [{
            breakpoint: 480,
            options: {
                chart: {
                    width: 200
                },
                legend: {
                    position: 'bottom'
                }
            }
        }]
    };

    const basicchart = new ApexCharts(document.querySelector("#polararea-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* polar area monochrome chart */
    const monochromeoptions = {
        series: [42, 47, 52, 58, 65],
        chart: {
            height: 300,
            type: 'polarArea'
        },
        labels: ['رز اول', 'رز دوم', 'رز سوم', 'رز چهارم', 'رز پمجم'],
        fill: {
            opacity: 1
        },
        stroke: {
            width: 1,
            colors: undefined
        },
        yaxis: {
            show: false
        },
        legend: {
            position: 'bottom'
        },
        plotOptions: {
            polarArea: {
                rings: {
                    strokeWidth: 0
                },
                spokes: {
                    strokeWidth: 0
                },
            }
        },
        theme: {
            monochrome: {
                enabled: true,
                shadeTo: 'light',
                shadeIntensity: 0.6,
                color: "#985ffd",
            }
        }
    };
    const monochromechart = new ApexCharts(document.querySelector("#polararea-monochrome"), monochromeoptions);
    if(monochromechart) monochromechart.render();

})();