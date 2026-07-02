(function () {
    "use strict";

    /* basic treemap chart */
    const basicoptions = {
        series: [
            {
                data: [
                    {
                        x: 'تهران',
                        y: 218
                    },
                    {
                        x: 'تبریز',
                        y: 149
                    },
                    {
                        x: 'شیراز',
                        y: 184
                    },
                    {
                        x: 'مراغه',
                        y: 55
                    },
                    {
                        x: 'مشهد',
                        y: 84
                    },
                    {
                        x: 'اهواز',
                        y: 31
                    },
                    {
                        x: 'مرکزی',
                        y: 70
                    },
                    {
                        x: 'قزوین',
                        y: 30
                    },
                    {
                        x: 'آستارا',
                        y: 44
                    },
                    {
                        x: 'راسمر',
                        y: 68
                    },
                    {
                        x: 'اورمیه',
                        y: 28
                    },
                    {
                        x: 'زنجان',
                        y: 19
                    },
                    {
                        x: 'سنندج',
                        y: 29
                    }
                ]
            }
        ],
        legend: {
            show: false
        },
        chart: {
            height: 350,
            type: 'treemap'
        },
        colors: ["#985ffd"],
        title: {
            text: 'درختی پایه',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
    };
    const basicchart = new ApexCharts(document.querySelector("#treemap-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* multi dimensional treemap chart */
    const dimensionaloptions = {
        series: [
            {
                name: 'دسکتاپ',
                data: [
                    {
                        x: 'لنوو',
                        y: 10
                    },
                    {
                        x: 'ایسوس',
                        y: 60
                    },
                    {
                        x: 'اچ پی',
                        y: 41
                    }
                ]
            },
            {
                name: 'موبایل',
                data: [
                    {
                        x: 'اپل',
                        y: 10
                    },
                    {
                        x: 'سامسونگ',
                        y: 20
                    },
                    {
                        x: 'نوکیا',
                        y: 51
                    },
                    {
                        x: 'شیائومی',
                        y: 30
                    },
                    {
                        x: 'هواوی',
                        y: 20
                    },
                    {
                        x: 'سونی',
                        y: 30
                    }
                ]
            }
        ],
        colors: ["#985ffd", "#ff49cd"],
        legend: {
            show: false
        },
        chart: {
            height: 350,
            type: 'treemap'
        },
        title: {
            text: 'درختی چندبعدی',
            align: 'center',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
    };
    const dimensionalchart = new ApexCharts(document.querySelector("#treemap-multi"), dimensionaloptions);
    if(dimensionalchart) dimensionalchart.render();

    /* distributed treemap chart */
    const distributedoptions = {
        series: [
            {
                data: [
                    {
                        x: 'تهران',
                        y: 218
                    },
                    {
                        x: 'تبریز',
                        y: 149
                    },
                    {
                        x: 'سنندج',
                        y: 184
                    },
                    {
                        x: 'مراغه',
                        y: 55
                    },
                    {
                        x: 'رامسر',
                        y: 84
                    },
                    {
                        x: 'آستارا',
                        y: 31
                    },
                    {
                        x: 'شیراز',
                        y: 70
                    },
                    {
                        x: 'اهواز',
                        y: 30
                    },
                    {
                        x: 'مشهد',
                        y: 44
                    },
                    {
                        x: 'بلوچستان',
                        y: 68
                    },
                    {
                        x: 'زنجان',
                        y: 28
                    },
                    {
                        x: 'قزوین',
                        y: 19
                    },
                    {
                        x: 'اورمیه',
                        y: 29
                    }
                ]
            }
        ],
        legend: {
            show: false
        },
        chart: {
            height: 350,
            type: 'treemap'
        },
        title: {
            text: 'درختی توزیع‌شده (رنگ متفاوت برای هر سلول)',
            align: 'center',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        colors: [
           '#985ffd', '#ff49cd', '#fdaf22', '#32d484', '#00c9ff', '#ff6757', 'rgba(53, 181, 170,1)','rgb(190, 43, 235)'
        ],
        plotOptions: {
            treemap: {
                distributed: true,
                enableShades: false
            }
        }
    };
    const distributedchart = new ApexCharts(document.querySelector("#treemap-distributed"), distributedoptions);
    if(distributedchart) distributedchart.render();

    /* treemap chart with color ranges */
    const treemapoptions = {
        series: [
            {
                data: [
                    {
                        x: 'INTC',
                        y: 1.2
                    },
                    {
                        x: 'GS',
                        y: 0.4
                    },
                    {
                        x: 'CVX',
                        y: -1.4
                    },
                    {
                        x: 'GE',
                        y: 2.7
                    },
                    {
                        x: 'CAT',
                        y: -0.3
                    },
                    {
                        x: 'RTX',
                        y: 5.1
                    },
                    {
                        x: 'CSCO',
                        y: -2.3
                    },
                    {
                        x: 'JNJ',
                        y: 2.1
                    },
                    {
                        x: 'PG',
                        y: 0.3
                    },
                    {
                        x: 'TRV',
                        y: 0.12
                    },
                    {
                        x: 'MMM',
                        y: -2.31
                    },
                    {
                        x: 'NKE',
                        y: 3.98
                    },
                    {
                        x: 'IYT',
                        y: 1.67
                    }
                ]
            }
        ],
        legend: {
            show: false
        },
        chart: {
            height: 350,
            type: 'treemap'
        },
        title: {
            text: 'درختی با محدوده رنگ‌ها',
            align: 'left',
            style: {
                fontSize: '13px',
                fontWeight: 'bold',
                color: '#8c9097'
            },
        },
        dataLabels: {
            enabled: true,
            style: {
                fontSize: '12px',
            },
            formatter: function (text, op) {
                return [text, op.value]
            },
            offsetY: -4
        },
        plotOptions: {
            treemap: {
                enableShades: true,
                shadeIntensity: 0.5,
                reverseNegativeShade: true,
                colorScale: {
                    ranges: [
                        {
                            from: -6,
                            to: 0,
                            color: '#985ffd'
                        },
                        {
                            from: 0.001,
                            to: 6,
                            color: '#ff49cd'
                        }
                    ]
                }
            }
        }
    };
    const treemapchart = new ApexCharts(document.querySelector("#treemap-colorranges"), treemapoptions);
    if(treemapchart) treemapchart.render();

})();

    function englishToPersianDigits(str) {
            const persianDigits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
            return str.replace(/[0-9]/g, d => persianDigits[d]);
        }
    function convertEnglishNumbersToPersian(element = document.body) {
          
            const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    while (walker.nextNode()) {
                const node = walker.currentNode;
    node.nodeValue = englishToPersianDigits(node.nodeValue);
            }
        }
    document.addEventListener("DOMContentLoaded", function () {
        convertEnglishNumbersToPersian();
        });
