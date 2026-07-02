(function () {
    "use strict";

    /* basic range area chart */
    const basicoptions = {
        series: [
            {
                name: 'New York Temperature',
                data: [
                    {
                        x: 'خرداد',
                        y: [-2, 4]
                    },
                    {
                        x: 'تیر',
                        y: [-1, 6]
                    },
                    {
                        x: 'مرداد',
                        y: [3, 10]
                    },
                    {
                        x: 'شهریور',
                        y: [8, 16]
                    },
                    {
                        x: 'مهر',
                        y: [13, 22]
                    },
                    {
                        x: 'آبان',
                        y: [18, 26]
                    },
                    {
                        x: 'آذر',
                        y: [21, 29]
                    },
                    {
                        x: 'دی',
                        y: [21, 28]
                    },
                    {
                        x: 'بهمن',
                        y: [17, 24]
                    },
                    {
                        x: 'اسفند',
                        y: [11, 18]
                    },
                    {
                        x: 'فروردین',
                        y: [6, 12]
                    },
                    {
                        x: 'اردیبهشت',
                        y: [1, 7]
                    }
                ]
            }
        ],
        chart: {
            height: 350,
            type: 'rangeArea'
        },
        stroke: {
            curve: 'straight'
        },
        title: {
            text: 'دمای تهران (در تمام طول سال)'
        },
        colors: ["#985ffd"],
        markers: {
            hover: {
                sizeOffset: 5
            }
        },
        dataLabels: {
            enabled: false
        },
        yaxis: {
            labels: {
                formatter: (val) => {
                    return val + '°C'
                }
            }
        }
    };
    const basicchart = new ApexCharts(document.querySelector("#rangearea-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* combo range area chart */
    const combooptions = {
        series: [
            {
                type: 'rangeArea',
                name: 'Team B Range',

                data: [
                    {
                        x: 'فروردین',
                        y: [1100, 1900]
                    },
                    {
                        x: 'اردیبهشت',
                        y: [1200, 1800]
                    },
                    {
                        x: 'خرداد',
                        y: [900, 2900]
                    },
                    {
                        x: 'تیر',
                        y: [1400, 2700]
                    },
                    {
                        x: 'مرداد',
                        y: [2600, 3900]
                    },
                    {
                        x: 'شهریور',
                        y: [500, 1700]
                    },
                    {
                        x: 'مهر',
                        y: [1900, 2300]
                    },
                    {
                        x: 'آبان',
                        y: [1000, 1500]
                    }
                ]
            },

            {
                type: 'rangeArea',
                name: 'Team A Range',
                data: [
                    {
                        x: 'فروردین',
                        y: [3100, 3400]
                    },
                    {
                        x: 'اردیبهشت',
                        y: [4200, 5200]
                    },
                    {
                        x: 'خرداد',
                        y: [3900, 4900]
                    },
                    {
                        x: 'تیر',
                        y: [3400, 3900]
                    },
                    {
                        x: 'مرداد',
                        y: [5100, 5900]
                    },
                    {
                        x: 'شهریور',
                        y: [5400, 6700]
                    },
                    {
                        x: 'مهر',
                        y: [4300, 4600]
                    },
                    {
                        x: 'آبان',
                        y: [2100, 2900]
                    }
                ]
            },

            {
                type: 'line',
                name: 'Team B Median',
                data: [
                    {
                        x: 'فروردین',
                        y: 1500
                    },
                    {
                        x: 'اردیبهشت',
                        y: 1700
                    },
                    {
                        x: 'خرداد',
                        y: 1900
                    },
                    {
                        x: 'تیر',
                        y: 2200
                    },
                    {
                        x: 'مرداد',
                        y: 3000
                    },
                    {
                        x: 'شهریور',
                        y: 1000
                    },
                    {
                        x: 'مهر',
                        y: 2100
                    },
                    {
                        x: 'آبان',
                        y: 1200
                    },
                    {
                        x: 'آذر',
                        y: 1800
                    },
                    {
                        x: 'دی',
                        y: 2000
                    }
                ]
            },
            {
                type: 'line',
                name: 'Team A Median',
                data: [
                    {
                        x: 'فروردین',
                        y: 3300
                    },
                    {
                        x: 'اردیبهشت',
                        y: 4900
                    },
                    {
                        x: 'خرداد',
                        y: 4300
                    },
                    {
                        x: 'تیر',
                        y: 3700
                    },
                    {
                        x: 'مرداد',
                        y: 5500
                    },
                    {
                        x: 'شهریور',
                        y: 5900
                    },
                    {
                        x: 'مهر',
                        y: 4500
                    },
                    {
                        x: 'آبان',
                        y: 2400
                    },
                    {
                        x: 'آذر',
                        y: 2100
                    },
                    {
                        x: 'دی',
                        y: 1500
                    }
                ]
            }
        ],
        chart: {
            height: 350,
            type: 'rangeArea',
            animations: {
                speed: 500
            }
        },
        colors: ['#985ffd', '#ff49cd', '#985ffd', '#ff49cd'],
        dataLabels: {
            enabled: false
        },
        fill: {
            opacity: [0.24, 0.24, 1, 1]
        },
        forecastDataPoints: {
            count: 2
        },
        stroke: {
            curve: 'straight',
            width: [0, 0, 2, 2]
        },
        legend: {
            show: true,
            customLegendItems: ['تیم دوم', 'تیم اول'],
            inverseOrder: true
        },
        title: {
            text: 'منطقه محدوده با خط پیش بینی (دسته کوچک موسیقی جاز)'
        },
        markers: {
            hover: {
                sizeOffset: 5
            }
        }
    };
    const combochart = new ApexCharts(document.querySelector("#rangearea-combo"), combooptions);
    if(combochart) combochart.render();

})();