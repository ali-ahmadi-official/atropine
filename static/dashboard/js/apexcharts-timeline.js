(function () {
    "use strict";

    /* basic timeline chart */
    const basicoptions = {
        series: [
            {
                data: [
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-02').getTime(),
                            new Date('2019-03-04').getTime()
                        ]
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-04').getTime(),
                            new Date('2019-03-08').getTime()
                        ]
                    },
                    {
                        x: 'اعتبار سنجی',
                        y: [
                            new Date('2019-03-08').getTime(),
                            new Date('2019-03-12').getTime()
                        ]
                    },
                    {
                        x: 'اعزام',
                        y: [
                            new Date('2019-03-12').getTime(),
                            new Date('2019-03-18').getTime()
                        ]
                    }
                ]
            }
        ],
        chart: {
            height: 320,
            type: 'rangeBar'
        },
        grid: {
            borderColor: '#f2f5f7',
        },
        plotOptions: {
            bar: {
                horizontal: true
            }
        },
        colors: ["#985ffd"],
        xaxis: {
            type: 'datetime',
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
    const basicchart = new ApexCharts(document.querySelector("#timeline-basic"), basicoptions);
    if(basicchart) basicchart.render();

    /* multiple colors timeline chart */
    const multipleoptions = {
        series: [
            {
                data: [
                    {
                        x: 'تجزیه',
                        y: [
                            new Date('2019-02-27').getTime(),
                            new Date('2019-03-04').getTime()
                        ],
                        fillColor: '#985ffd'
                    },
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-04').getTime(),
                            new Date('2019-03-08').getTime()
                        ],
                        fillColor: '#ff49cd'
                    },
                    {
                        x: 'برنامه نویسی',
                        y: [
                            new Date('2019-03-07').getTime(),
                            new Date('2019-03-10').getTime()
                        ],
                        fillColor: '#fdaf22'
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-08').getTime(),
                            new Date('2019-03-12').getTime()
                        ],
                        fillColor: '#32d484'
                    },
                    {
                        x: 'اعزام',
                        y: [
                            new Date('2019-03-12').getTime(),
                            new Date('2019-03-17').getTime()
                        ],
                        fillColor: '#00c9ff'
                    }
                ]
            }
        ],
        chart: {
            height: 320,
            type: 'rangeBar'
        },
        plotOptions: {
            bar: {
                horizontal: true,
                distributed: true,
                dataLabels: {
                    hideOverflowingLabels: false
                }
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val, opts) {
                const label = opts.w.globals.labels[opts.dataPointIndex]
                const a = moment(val[0])
                const b = moment(val[1])
                const diff = b.diff(a, 'days')
                return label + ': ' + diff + (diff > 1 ? ' روزها' : ' روز')
            },
            style: {
                colors: ['#f3f4f5', '#fff']
            }
        },
        xaxis: {
            type: 'datetime',
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
            show: false
        },
        grid: {
            borderColor: '#f2f5f7',
        }
    };
    const multiplechart = new ApexCharts(document.querySelector("#timeline-colors"), multipleoptions);
    if(multiplechart) multiplechart.render();

    /* multi series timeline chart */
    const multiseriesoptions = {
        series: [
            {
                name: 'بچه',
                data: [
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-05').getTime(),
                            new Date('2019-03-08').getTime()
                        ]
                    },
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-08').getTime(),
                            new Date('2019-03-11').getTime()
                        ]
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-11').getTime(),
                            new Date('2019-03-16').getTime()
                        ]
                    }
                ]
            },
            {
                name: 'جو',
                data: [
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-02').getTime(),
                            new Date('2019-03-05').getTime()
                        ]
                    },
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-06').getTime(),
                            new Date('2019-03-09').getTime()
                        ]
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-10').getTime(),
                            new Date('2019-03-19').getTime()
                        ]
                    }
                ]
            }
        ],
        chart: {
            height: 320,
            type: 'rangeBar'
        },
        plotOptions: {
            bar: {
                horizontal: true
            }
        },
        dataLabels: {
            enabled: true,
            formatter: function (val) {
                const a = moment(val[0])
                const b = moment(val[1])
                const diff = b.diff(a, 'days')
                return diff + (diff > 1 ? ' روزها' : ' روز')
            }
        },
        colors: ["#985ffd", "#ff49cd"],
        grid: {
            borderColor: '#f2f5f7',
        },
        fill: {
            type: 'gradient',
            gradient: {
                shade: 'light',
                type: 'vertical',
                shadeIntensity: 0.25,
                gradientToColors: undefined,
                inverseColors: true,
                opacityFrom: 1,
                opacityTo: 1,
                stops: [50, 0, 100, 100]
            }
        },
        xaxis: {
            type: 'datetime',
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
        legend: {
            position: 'top'
        }
    };
    const multiserieschart = new ApexCharts(document.querySelector("#timeline-multi"), multiseriesoptions);
    if(multiserieschart) multiserieschart.render();

    /* advanced timeline chart */
    const advancedoptions = {
        series: [
            {
                name: 'بچه',
                data: [
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-05').getTime(),
                            new Date('2019-03-08').getTime()
                        ]
                    },
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-02').getTime(),
                            new Date('2019-03-05').getTime()
                        ]
                    },
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-05').getTime(),
                            new Date('2019-03-07').getTime()
                        ]
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-03').getTime(),
                            new Date('2019-03-09').getTime()
                        ]
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-08').getTime(),
                            new Date('2019-03-11').getTime()
                        ]
                    },
                    {
                        x: 'اعتبار سنجی',
                        y: [
                            new Date('2019-03-11').getTime(),
                            new Date('2019-03-16').getTime()
                        ]
                    },
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-01').getTime(),
                            new Date('2019-03-03').getTime()
                        ],
                    }
                ]
            },
            {
                name: 'جو',
                data: [
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-02').getTime(),
                            new Date('2019-03-05').getTime()
                        ]
                    },
                    {
                        x: 'تست',
                        y: [
                            new Date('2019-03-06').getTime(),
                            new Date('2019-03-16').getTime()
                        ],
                        goals: [
                            {
                                name: 'Break',
                                value: new Date('2019-03-10').getTime(),
                                strokeColor: '#CD2F2A'
                            }
                        ]
                    },
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-03').getTime(),
                            new Date('2019-03-07').getTime()
                        ]
                    },
                    {
                        x: 'اعزام',
                        y: [
                            new Date('2019-03-20').getTime(),
                            new Date('2019-03-22').getTime()
                        ]
                    },
                    {
                        x: 'طراحی',
                        y: [
                            new Date('2019-03-10').getTime(),
                            new Date('2019-03-16').getTime()
                        ]
                    }
                ]
            },
            {
                name: 'وت',
                data: [
                    {
                        x: 'رمز',
                        y: [
                            new Date('2019-03-10').getTime(),
                            new Date('2019-03-17').getTime()
                        ]
                    },
                    {
                        x: 'اعتبار سنجی',
                        y: [
                            new Date('2019-03-05').getTime(),
                            new Date('2019-03-09').getTime()
                        ],
                        goals: [
                            {
                                name: 'Break',
                                value: new Date('2019-03-07').getTime(),
                                strokeColor: '#CD2F2A'
                            }
                        ]
                    },
                ]
            }
        ],
        chart: {
            height: 320,
            type: 'rangeBar'
        },
        plotOptions: {
            bar: {
                horizontal: true,
                barHeight: '80%'
            }
        },
        colors: ["#985ffd", "#ff49cd", "#fdaf22"],
        xaxis: {
            type: 'datetime',
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
        grid: {
            borderColor: '#f2f5f7',
        },
        stroke: {
            width: 1
        },
        fill: {
            type: 'solid',
            opacity: 0.6
        },
        legend: {
            position: 'top',
            horizontalAlign: 'center'
        }
    };
    const advancedchart = new ApexCharts(document.querySelector("#timeline-advanced"), advancedoptions);
    if(advancedchart) advancedchart.render();

    /* timeline-grouped charts */
    const groupedoptions = {
        series: [
            // George Washington
            {
                name: 'جورج واشنگتن',
                data: [
                    {
                        x: 'رئیس جمهور',
                        y: [
                            new Date(1789, 3, 30).getTime(),
                            new Date(1797, 2, 4).getTime()
                        ]
                    },
                ]
            },
            // John Adams
            {
                name: 'جان آدامز',
                data: [
                    {
                        x: 'رئیس جمهور',
                        y: [
                            new Date(1797, 2, 4).getTime(),
                            new Date(1801, 2, 4).getTime()
                        ]
                    },
                    {
                        x: 'معاون رئیس جمهور',
                        y: [
                            new Date(1789, 3, 21).getTime(),
                            new Date(1797, 2, 4).getTime()
                        ]
                    }
                ]
            },
            // Thomas Jefferson
            {
                name: 'توماس جفرسون',
                data: [
                    {
                        x: 'رئیس جمهور',
                        y: [
                            new Date(1801, 2, 4).getTime(),
                            new Date(1809, 2, 4).getTime()
                        ]
                    },
                    {
                        x: 'معاون رئیس جمهور',
                        y: [
                            new Date(1797, 2, 4).getTime(),
                            new Date(1801, 2, 4).getTime()
                        ]
                    },
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1790, 2, 22).getTime(),
                            new Date(1793, 11, 31).getTime()
                        ]
                    }
                ]
            },
            // Aaron Burr
            {
                name: 'هارون بور',
                data: [
                    {
                        x: 'معاون رئیس جمهور',
                        y: [
                            new Date(1801, 2, 4).getTime(),
                            new Date(1805, 2, 4).getTime()
                        ]
                    }
                ]
            },
            // George Clinton
            {
                name: 'جورج کلینتون',
                data: [
                    {
                        x: 'معاون رئیس جمهور',
                        y: [
                            new Date(1805, 2, 4).getTime(),
                            new Date(1812, 3, 20).getTime()
                        ]
                    }
                ]
            },
            // John Jay
            {
                name: 'جان جی',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1789, 8, 25).getTime(),
                            new Date(1790, 2, 22).getTime()
                        ]
                    }
                ]
            },
            // Edmund Randolph
            {
                name: 'ادموند راندولف',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1794, 0, 2).getTime(),
                            new Date(1795, 7, 20).getTime()
                        ]
                    }
                ]
            },
            // Timothy Pickering
            {
                name: 'تیموتی پیکرینگ',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1795, 7, 20).getTime(),
                            new Date(1800, 4, 12).getTime()
                        ]
                    }
                ]
            },
            // Charles Lee
            {
                name: 'چارلز لی',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1800, 4, 13).getTime(),
                            new Date(1800, 5, 5).getTime()
                        ]
                    }
                ]
            },
            // John Marshall
            {
                name: 'جان مارشال',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1800, 5, 13).getTime(),
                            new Date(1801, 2, 4).getTime()
                        ]
                    }
                ]
            },
            // Levi Lincoln
            {
                name: 'لوی لینکلن',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1801, 2, 5).getTime(),
                            new Date(1801, 4, 1).getTime()
                        ]
                    }
                ]
            },
            // James Madison
            {
                name: 'جیمز مدیسون',
                data: [
                    {
                        x: 'وزیر امور خارجه',
                        y: [
                            new Date(1801, 4, 2).getTime(),
                            new Date(1809, 2, 3).getTime()
                        ]
                    }
                ]
            },
        ],
        chart: {
            height: 320,
            type: 'rangeBar'
        },
        plotOptions: {
            bar: {
                horizontal: true,
                barHeight: '50%',
                rangeBarGroupRows: true
            }
        },
        colors: [
            "#985ffd", "#ff49cd", "#f4a742", "#fe5454", "#7b76fe",
            "#3F51B5", "#546E7A", "#D4526E", "#8D5B4C", "#F86624",
            "#D7263D", "#1B998B", "#2E294E", "#F46036", "#E2C044"
        ],
        grid: {
            borderColor: '#f2f5f7',
        },
        fill: {
            type: 'solid'
        },
        xaxis: {
            type: 'datetime',
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
        legend: {
            position: 'right'
        },
        tooltip: {
            custom: function ({ series, seriesIndex, dataPointIndex, w }) {
                const fromYear = new Date(w.globals.seriesRangeStart[seriesIndex][dataPointIndex]).getFullYear();
                const toYear = new Date(w.globals.seriesRangeEnd[seriesIndex][dataPointIndex]).getFullYear();
                const name = w.globals.series[seriesIndex].name;
                return `
                `;
            },
        },
    };
    const groupedchart = new ApexCharts(document.querySelector("#timeline-grouped"), groupedoptions);
    if(groupedchart) groupedchart.render();

    /* dumbbell chart */
    const dumbbelloptions = {
        series: [
        {
          data: [
            {
              x: 'عمل',
              y: [2800, 4500]
            },
            {
              x: 'موفقیت مشتری',
              y: [3200, 4100]
            },
            {
              x: 'مهندسی',
              y: [2950, 7800]
            },
            {
              x: 'بازاریابی',
              y: [3000, 4600]
            },
            {
              x: 'محصول',
              y: [3500, 4100]
            },
            {
              x: 'علم داده ها',
              y: [4500, 6500]
            },
            {
              x: 'فروش',
              y: [4100, 5600]
            }
          ]
        }
      ],
        chart: {
        height: 320,
        type: 'rangeBar',
        zoom: {
          enabled: false
        }
      },
      colors: ["#985ffd", "#ff49cd"],
      plotOptions: {
        bar: {
          horizontal: true,
          isDumbbell: true,
          dumbbellColors: [["#985ffd", "#ff49cd"]]
        }
      },
      title: {
          text: 'نمودار دمبل'
      },
      legend: {
        show: true,
        showForSingleSeries: true,
        position: 'top',
        horizontalAlign: 'left',
        customLegendItems: ['زن', 'مرد']
      },
      fill: {
        type: 'gradient',
        gradient: {
          gradientToColors: ['#ff49cd'],
          inverseColors: false,
          stops: [0, 100]
        }
      },
      grid: {
        xaxis: {
          lines: {
            show: true
          }
        },
        yaxis: {
          lines: {
            show: false
          }
        }
      }
    };
    const dumbbellchart = new ApexCharts(document.querySelector("#dumbbell-chart"), dumbbelloptions);
    if(dumbbellchart) dumbbellchart.render();

})();