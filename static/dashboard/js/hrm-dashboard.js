(function () {
  'use strict';

  /* Candidate Statistics */
  const options = {
    series: [
      {
        name: "نامزدهای استخدام شده",
        data: [13, 23, 20, 25, 10, 13, 13, 15, 13, 23, 20, 25],
        type: "column",
      },
      {
        name: "پاسخ دریافت کرد",
        data: [20, 30, 25, 50, 25, 30, 20, 35, 20, 30, 25, 50],
        type: "column",
      },
    ],
    chart: {
      type: "line",
      height: 320,
      toolbar: {
        show: false,
      },
      zoom: {
        enabled: true,
      },
      stacked: true,
    },
    grid: {
      show: true,
      borderColor: "rgba(119, 119, 142, 0.1)",
      strokeDashArray: 4,
    },
    colors: ["var(--primary-color)", "var(--primary02)"],
    stroke: {
      curve: 'smooth',
      width: ['0', '0'],
      dashArray: ['0', '0']
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: "40%",
        borderRadius: "3",
      },
    },
    dataLabels: {
      enabled: false,
    },
    xaxis: {
      categories: [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
      ],
      labels: {
        show: true,
        style: {
          colors: "#8c9097",
          fontSize: "11px",
          fontWeight: 600,
          cssClass: "apexcharts-xaxis-label",
        },
      },
    },
    legend: {
      show: true,
      position: "bottom",
      offsetX: 0,
      offsetY: 10,
      markers: {
        width: 10,
        height: 10,
        strokeWidth: 0,
        strokeColor: "#fff",
        fillColors: undefined,
        radius: 12,
        customHTML: undefined,
        onClick: undefined,
        offsetX: 0,
        offsetY: 0,
      },
    },
    yaxis: {
      labels: {
        show: true,
        style: {
          colors: "#8c9097",
          fontSize: "11px",
          fontWeight: 600,
          cssClass: "apexcharts-xaxis-label",
        },
      },
    },
  };
  const chart = new ApexCharts(document.querySelector("#candidate-statistics"), options);
  if(chart) chart.render();
  /* Candidate Statistics */

  /* Attedance Overview */
  const options2 = {
    series: [1754, 878, 634, 470],
    labels: ["Present", "Late", "Permission", "Absent"],
    chart: {
      height: 260,
      type: 'donut',
    },
    dataLabels: {
      enabled: false,
    },

    legend: {
      show: false,
    },
    stroke: {
      show: true,
      curve: 'smooth',
      lineCap: 'round',
      colors: "#fff",
      width: 4,
      dashArray: 0,
    },
    plotOptions: {
      pie: {
        startAngle: -90,
        endAngle: 90,
        offsetY: 10,
        expandOnClick: false,
        donut: {
          size: '80%',
          background: 'transparent',
          labels: {
            show: true,
            name: {
              show: true,
              fontSize: '20px',
              color: '#495057',
              offsetY: -30
            },
            value: {
              show: true,
              fontSize: '15px',
              color: undefined,
              offsetY: -25,
              formatter: function (val) {
                return val + "%"
              }
            },
            total: {
              show: true,
              showAlways: true,
              label: 'مجموع',
              fontSize: '22px',
              fontWeight: 600,
              color: '#495057',
            }

          }
        }
      }
    },
    grid: {
      padding: {
        bottom: -100
      }
    },
    colors: ["var(--primary-color)", "rgba(50, 212, 132, 1)", "rgba(253, 175, 34, 1)", "rgba(255, 103, 87, 1)"],
  };
    // تنظیمات نمودار
    const options3 = {
        series: [{
            data: [462, 451, 350, 530, 470, 500, 485],
            name: 'تعداد کارمندان',
        }],
        chart: {
            type: 'bar',
            height: 367,
            toolbar: { show: false },
        },
        plotOptions: {
            bar: {
                horizontal: true,
                distributed: true,
                barHeight: '50%',
                borderRadius: 3,
            }
        },
        legend: { show: false },
        dataLabels: { enabled: false },
        grid: {
            borderColor: '#eee',
            strokeDashArray: 3,
        },
        colors: ["var(--primary-color)"],
        xaxis: {
            categories: [
                'فناوری اطلاعات',
                'بازاریابی',
                'عمل',
                'دارایی',
                'فروش',
                'خدمات مشتری',
                'منابع انسانی'
            ],
            position: 'bottom',
            labels: {
                style: { fontFamily: 'inherit', fontSize: '12px' },
            },
            axisBorder: { show: true, color: '#ccc' },
            axisTicks: { show: true, color: '#ccc' },
        },
        yaxis: {
            opposite: true,   // محور در سمت راست
            reversed: true,   // ترتیب بالا به پایین
            labels: {
                show: true,
                style: { fontFamily: 'inherit', fontSize: '13px' },
            },
        },
        tooltip: { theme: "dark" },
    };

    // ساخت نمودار
    const chart3 = new ApexCharts(document.querySelector("#employee-department"), options3);

    chart3.render().then(() => {
        const svg = document.querySelector("#employee-department svg");
        if (!svg) return;

        // فاصله امن متن‌های محور y با dx
        const padding = 10; // فاصله از نمودار، می‌تونی کم و زیاد کنی
        svg.querySelectorAll('.apexcharts-yaxis text').forEach(text => {
            text.setAttribute('dx', padding);
            text.setAttribute('text-anchor', 'end'); // راست‌چین
            text.setAttribute('direction', 'rtl');
        });

        // عددهای محور x زیر نمودار
        svg.querySelectorAll('.apexcharts-xaxis text').forEach(text => {
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('direction', 'ltr');
        });
    });


})();