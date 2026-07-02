(function () {
    "use strict";

    /* basic heatmap chart */
    function generateData(count, yrange) {
        let i = 0;
        const series = [];
        while (i < count) {
            const x = 'w' + (i + 1).toString();
            const y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }
    const basicoptions = {
        series: [{
            name: 'متریک 1',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 2',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 3',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 4',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 5',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 6',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 7',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 8',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 9',
            data: generateData(18, {
                min: 0,
                max: 90
            })
        }
        ],
        chart: {
            height: 350,
            type: 'heatmap',
        },
        dataLabels: {
            enabled: false
        },
        colors: ["#985ffd"],
        grid: {
            borderColor: '#f2f5f7',
        },
        title: {
            text: 'نمودار نقشه گرما (تک رنگ)',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
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
    const basicchart = new ApexCharts(document.querySelector("#heatmap-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* multi series heatmap chart */
    function generateData(count, yrange) {
        let i = 0;
        const series = [];
        while (i < count) {
            const x = (i + 1).toString();
            const y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }
    const data = [
        {
            name: 'W1',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W2',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W3',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W4',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W5',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W6',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W7',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W8',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W9',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W10',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W11',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W12',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W13',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W14',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'W15',
            data: generateData(8, {
                min: 0,
                max: 90
            })
        }
    ]
    data.reverse()
    const colors = ['#985ffd', '#ff49cd', '#fdaf22', '#32d484', '#00c9ff', '#ff6757', 'rgba(53, 181, 170,1)','rgb(190, 43, 235)', '#2176FF', '#33A1FD', '#7A918D', '#BAFF29']
    colors.reverse()
    const heatmapoptions = {
        series: data,
        chart: {
            height: 350,
            type: 'heatmap',
        },
        dataLabels: {
            enabled: false
        },
        colors: colors,
        title: {
            text: 'نمودار نقشه گرما (سایه های رنگی مختلف برای هر سری)',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        grid: {
            padding: {
                right: 20
            },
            borderColor: '#f2f5f7',
        },
        xaxis: {
            type: 'category',
            categories: ['10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '01:00', '01:30'],
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
    const heatmapchart = new ApexCharts(document.querySelector("#heatmap-multiseries"), heatmapoptions);
    if(heatmapchart) heatmapchart.render();

    /* color range heatmap */
    function generateData(count, yrange) {
        let i = 0;
        const series = [];
        while (i < count) {
            const x = (i + 1).toString();
            const y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }
    const coloroptions = {
        series: [
            {
                name: 'فروردین',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'اردیبهشت',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'خرداد',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'تیر',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'مرداد',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'شهریور',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'مهر',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'آبان',
                data: generateData(20, { min: -30, max: 55 })
            },
            {
                name: 'آذر',
                data: generateData(20, { min: -30, max: 55 })
            }
        ],
    }

        chart: {
            height: 350,
            type: 'heatmap',
        },
        plotOptions: {
            heatmap: {
                shadeIntensity: 0.5,
                radius: 0,
                useFillColorAsStroke: true,
                colorScale: {
                    ranges: [{
                        from: -30,
                        to: 5,
                        name: 'low',
                        color: '#985ffd'
                    },
                    {
                        from: 6,
                        to: 20,
                        name: 'medium',
                        color: '#ff49cd'
                    },
                    {
                        from: 21,
                        to: 45,
                        name: 'high',
                        color: '#fdaf22'
                    },
                    {
                        from: 46,
                        to: 55,
                        name: 'extreme',
                        color: '#32d484'
                    }
                    ]
                }
            }
        },
        dataLabels: {
            enabled: false
        },
        grid: {
            borderColor: '',
        },
        stroke: {
            width: 1
        },
        title: {
            text: 'نمودار نقشه گرما با دامنه رنگ',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
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
    const colorchart = new ApexCharts(document.querySelector("#heatmap-colorrange"), coloroptions);
    if(colorchart) colorchart.render();

    /* heatmap range without shades */
    const rangeoptions = {
        series: [{
            name: 'متریک 1',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 2',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 3',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 4',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 5',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 6',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 7',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 8',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        },
        {
            name: 'متریک 9',
            data: generateData(20, {
                min: 0,
                max: 90
            })
        }
        ],
        chart: {
            height: 350,
            type: 'heatmap',
        },
        stroke: {
            width: 0
        },
        plotOptions: {
            heatmap: {
                radius: 30,
                enableShades: false,
                colorScale: {
                    ranges: [{
                        from: 0,
                        to: 50,
                        color: '#985ffd'
                    },
                    {
                        from: 51,
                        to: 100,
                        color: '#ff49cd'
                    },
                    ],
                },

            }
        },
        grid: {
            borderColor: '#f2f5f7',
        },
        dataLabels: {
            enabled: true,
            style: {
                colors: ['#fff']
            }
        },
        xaxis: {
            type: 'category',
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
        title: {
            text: 'گرد (دامنه بدون سایه)',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
    };
    const rangechart = new ApexCharts(document.querySelector("#heatmap-range"), rangeoptions);
    if(rangechart) rangechart.render();

})();