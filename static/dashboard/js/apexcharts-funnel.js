(function () {
    "use strict";

    /* funnel chart */
    const funneloptions = {
        series: [
            {
                name: "Funnel Series",
                data: [1380, 1100, 990, 880, 740, 548, 330, 200],
            },
        ],
        chart: {
            type: 'bar',
            height: 350,
        },
        plotOptions: {
            bar: {
                borderRadius: 0,
                horizontal: true,
                barHeight: '80%',
                isFunnel: true,
            },
        },
        colors: [
            '#985ffd',
        ],
        dataLabels: {
            enabled: true,
            formatter: function (val, opt) {
                return opt.w.globals.labels[opt.dataPointIndex] + ':  ' + val
            },
            dropShadow: {
                enabled: true,
            },
        },
        title: {
            text: 'قیف استخدام',
            align: 'middle',
        },
        xaxis: {
            categories: [
                'دارای منبع',
                'نمایشی',
                'ارزیابی شده',
                'مصاحبه حضوری',
                'فنی',
                'تأیید شده',
                'ارائه شده',
                'استخدام شده',
            ],
        },
        legend: {
            show: false,
        },
    };
    const funnelchart = new ApexCharts(document.querySelector("#funnel-chart"), funneloptions);
    if(funnelchart) funnelchart.render();
    /* funnel chart */

    /* pyramid chart */
    const pyramidoptions = {
        series: [
            {
                name: "",
                data: [200, 330, 548, 740, 880, 990, 1100, 1380],
            },
        ],
        chart: {
            type: 'bar',
            height: 350,
        },
        plotOptions: {
            bar: {
                borderRadius: 0,
                horizontal: true,
                distributed: true,
                barHeight: '80%',
                isFunnel: true,
            },
        },
        colors: [
            '#985ffd', '#ff49cd', '#fdaf22', '#32d484', '#00c9ff', '#ff6757', 'rgba(53, 181, 170,1)','rgb(190, 43, 235)'
        ],
        dataLabels: {
            enabled: true,
            formatter: function (val, opt) {
                return opt.w.globals.labels[opt.dataPointIndex]
            },
            dropShadow: {
                enabled: true,
            },
        },
        title: {
            text: 'نمودار هرمی',
            align: 'middle',
        },
        xaxis: {
            categories: ['شیرینی', 'غذاهای فرآوری شده', 'چربی های سالم', 'گوشت', 'لوبیا و حبوبات', 'لبنیات', 'میوه و سبزیجات', 'غلات'],
        },
        legend: {
            show: false,
        },
    };

    const pyramidchart = new ApexCharts(document.querySelector("#pyramid-chart"), pyramidoptions);
    if(pyramidchart) pyramidchart.render();
    /* pyramid chart */

})();