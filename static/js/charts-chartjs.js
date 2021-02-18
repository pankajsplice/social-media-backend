/*
** Chartjs JS
*** @version v1.4.0
**** @copyright 2018 Pepdev.
*/
var seller_count= []
var chart_sync = null
$(document).ready(function(){
    
    $.ajax({
        type:'GET',
        async: false,
        url: '/api/v1/seller-count',
        success: function (data) {
            for (i = 0; i < 12; i++) {
                if(!!data.monthwise_seller_stats[i]){
                    seller_count.push(data.monthwise_seller_stats[i])
                } else {
                    seller_count.push(0);
                }
            }
        },
    });

    $.ajax({
        type:'GET',
        async: false,
        url: '/api/v1/chart-sync',
        success: function (data) {
            console.log(data)
            chart_sync = data
        },
    });
})

$(function() {

    // ============================================================== 
    // Chart js Charts
    // ==============================================================
    window.chartColors = {
        primary: 'rgb(52, 131, 255)',
        success: 'rgb(11, 195, 110)',
        warning: 'rgb(254, 193, 7)',
        danger: 'rgb(255,0,0)',
        secondary: 'rgb(205, 15, 216)',
        dark: 'rgb(85, 85, 85)',
        grey: 'rgb(201, 203, 207)' 
    };

    var color = Chart.helpers.color;

    var init_chart1 = function () {
        var config = {
            type: 'line',
            data: {
                labels: ["Oct","Nov","Dec","Jan","Feb","Mar"],
                datasets: [{
                    label: 'Sales',
                    backgroundColor: color(window.chartColors.primary).alpha(0.7).rgbString(),
                    borderColor: window.chartColors.primary,
                    borderWidth: 2,
                    data: [10, 14, 12, 16, 9, 11, 13, 9, 13, 15],
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                elements: {
                    line: {
                        tension: 0.00000001,
                    }
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                },
            }
        };
        if(document.getElementById("chart1")){
            var ctx = document.getElementById("chart1").getContext("2d");
            window.myLine = new Chart(ctx, config);
        }
    }

    var init_chart2 = function () {
       var url_loan_data = "/api/loan_collected/";
       var months = ["Oct","Nov","Dec","Jan","Feb","Mar"];
       var months_data = [10, 14, 12, 16, 9, 11, 13, 9, 13, 15];
       $.ajax({
            url: url_loan_data,
            type: 'get',
            crossDomain: true, // tell browser to allow cross domain
            headers: {
                // 'Authorization': auth
            },
            dataType: 'json',
            done: (function (data) {
                console.log("Data Loaded: " + data);
            }),
            success: (function (response, status, error) {
                    months =  response[0].month;
                    months_data = response[0].month_data;
                    var config = {
                            type: 'line',
                            data: {
                                    labels: months,
                                    datasets: [{
                                        label: 'Loan Collected',
                                        backgroundColor: color(window.chartColors.primary).alpha(0.7).rgbString(),
                                        borderColor: window.chartColors.primary,
                                        borderWidth: 2,
                                        data: months_data,
                                        fill: false
                                    }]
                                },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                legend: {
                                    display: false
                                },
                                elements: {
                                    line: {
                                        tension: 0.00000001,
                                    }
                                },
                                scales: {
                                    yAxes: [{
                                        ticks: {
                                            beginAtZero: true
                                        }
                                    }]
                                },
                            }
                        };
                    console.log("done with data", months);
                    if(document.getElementById("chart2")){
                        var ctx = document.getElementById("chart2").getContext("2d");
                        window.myLine = new Chart(ctx, config);
                    }
            })
        });

        // {
        //     labels: months,
        //     datasets: [{
        //         label: 'Loan Collected',
        //         backgroundColor: color(window.chartColors.primary).alpha(0.7).rgbString(),
        //         borderColor: window.chartColors.primary,
        //         borderWidth: 2,
        //         data: months_data,
        //         fill: false
        //     }]
        // }
        // console.log("========================",chart_data);
        // var config = {
        //     type: 'line',
        //     data: {
        //             labels: months,
        //             datasets: [{
        //                 label: 'Loan Collected',
        //                 backgroundColor: color(window.chartColors.primary).alpha(0.7).rgbString(),
        //                 borderColor: window.chartColors.primary,
        //                 borderWidth: 2,
        //                 data: months_data,
        //                 fill: false
        //             }]
        //         },
        //     options: {
        //         responsive: true,
        //         maintainAspectRatio: false,
        //         legend: {
        //             display: false
        //         },
        //         elements: {
        //             line: {
        //                 tension: 0.00000001,
        //             }
        //         },
        //         scales: {
        //             yAxes: [{
        //                 ticks: {
        //                     beginAtZero: true
        //                 }
        //             }]
        //         },
        //     }
        // };


    }

    var init_chart8 = function () {

        var url_loan_data = "/api/seller_statuscount";
       var months = []; //["Oct","Nov","Dec","Jan","Feb","Mar"];
       var enquiry_seller_count =  []; // [10, 14, 12, 16, 9, 11, 13, 9, 13, 15];
       var active_seller_count =  []; // [10, 14, 12, 16, 9, 11, 13, 9, 13, 15];
       var closed_seller_count =  []; // [10, 14, 12, 16, 9, 11, 13, 9, 13, 15];
       $.ajax({
            url: url_loan_data,
            type: 'get',
            crossDomain: true, // tell browser to allow cross domain
            headers: {
                // 'Authorization': auth
            },
            dataType: 'json',
            done: (function (data) {
                console.log("Data Loaded: " + data);
            }),
            success: (function (response, status, error) {
                console.log("response", response);
                    months =  response[0]['months'];
                    enquiry_seller_count = response[0].enquiry_seller_count;
                    active_seller_count = response[0].active_seller_count;
                    closed_seller_count = response[0].closed_seller_count;
                    console.log("response[0].closed_seller_count", response[0].closed_seller_count);
                    console.log("response[0].enquiry_seller_count", response[0].enquiry_seller_count);
                    console.log("response[0].active_seller_count", response[0].active_seller_count);
                    config = {
                                type: 'bar',
                                data: {
                                    labels: months,
                                    datasets: [{
                                        label: 'Enquiry',
                                        backgroundColor: window.chartColors.primary,
                                        borderColor: window.chartColors.primary,
                                        data: enquiry_seller_count,
                                    }, {
                                        label: 'Active Seller',
                                        backgroundColor: window.chartColors.success,
                                        borderColor: window.chartColors.success,
                                        data: active_seller_count,
                                    }, {
                                        label: 'Closed Seller',
                                        backgroundColor: window.chartColors.danger,
                                        borderColor: window.chartColors.danger,
                                        data: closed_seller_count,
                                    }]
                                },
                                options: {
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    title: {
                                        display: false,
                                        text: 'Chart.js Bar Chart - Stacked'
                                    },
                                    legend: {
                                        display: false
                                    },
                                    tooltips: {
                                        mode: 'index',
                                        intersect: false
                                    },
                                    scales: {
                                        xAxes: [{
                                            stacked: true,
                                        }],
                                        yAxes: [{
                                            stacked: true
                                        }]
                                    }
                                }
                            };
                            if(document.getElementById('chart8')){
                                var ctx = document.getElementById('chart8').getContext('2d');
                                window.myLine = new Chart(ctx, config);
                            }
            })
        });



        // var config = {
        //     type: 'bar',
        //     data: {
        //         labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October','November','December'],
        //         datasets: [{
        //             label: 'Primary',
        //             backgroundColor: window.chartColors.danger,
        //             borderColor: window.chartColors.danger,
        //             data: [ ],
        //         }, {
        //             label: 'Secondary',
        //             backgroundColor: window.chartColors.primary,
        //             borderColor: window.chartColors.primary,
        //             data: [],
        //         }, {
        //             label: 'success',
        //             backgroundColor: window.chartColors.success,
        //             borderColor: window.chartColors.success,
        //             data: seller_count,
        //         }]
        //     },
        //     options: {
        //         responsive: true,
        //         maintainAspectRatio: false,
        //         title: {
        //             display: false,
        //             text: 'Chart.js Bar Chart - Stacked'
        //         },
        //         legend: {
        //             display: false
        //         },
        //         tooltips: {
        //             mode: 'index',
        //             intersect: false
        //         },
        //         scales: {
        //             xAxes: [{
        //                 stacked: true,
        //             }],
        //             yAxes: [{
        //                 stacked: true
        //             }]
        //         }
        //     }
        // };
        //
        // var ctx = document.getElementById('chart8').getContext('2d');
        // window.myLine = new Chart(ctx, config);
    }

    //Chartjs Doughnut Chart
    var init_chart11 = function () {
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [chart_sync.paymentsync.good, chart_sync.paymentsync.bad],
                    backgroundColor: [
                        window.chartColors.success,
                        window.chartColors.danger
                    ],
                    label: 'Dataset 1'
                }],
                labels: ['Good', 'Bad']
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
        if(document.getElementById('payment_sync')){
            var ctx = document.getElementById('payment_sync').getContext('2d');
            window.myPie = new Chart(ctx, config);
        }
    }

    var init_chart12 = function () {
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [chart_sync.ordersync.good, chart_sync.ordersync.bad],
                    backgroundColor: [
                        window.chartColors.success,
                        window.chartColors.danger,
                    ],
                    label: 'Dataset 1'
                }],
                labels: ['Good', 'Bad']
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
        if(document.getElementById('order_sync')){
            var ctx = document.getElementById('order_sync').getContext('2d');
            window.myPie = new Chart(ctx, config);
        }
    }

    var init_chart13 = function () {
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [chart_sync.productsync.good, chart_sync.productsync.bad],
                    backgroundColor: [
                        window.chartColors.success,
                        window.chartColors.danger,
                    ],
                    label: 'Dataset 1'
                }],
                labels: ['Good', 'Bad']
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
        if(document.getElementById('product_sync')){
            var ctx = document.getElementById('product_sync').getContext('2d');
            window.myPie = new Chart(ctx, config);
        }
    }

    var init_chart14 = function () {
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [chart_sync.plaidsync.good, chart_sync.plaidsync.bad],
                    backgroundColor: [
                        window.chartColors.success,
                        window.chartColors.danger,
                    ],
                    label: 'Dataset 1'
                }],
                labels:['Good', 'Bad']
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
        if(document.getElementById('plaid_sync')){
            var ctx = document.getElementById('plaid_sync').getContext('2d');
            window.myPie = new Chart(ctx, config);
        }
    }

    var init_chart15 = function () {
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [chart_sync.feedbacksync.good, chart_sync.feedbacksync.bad],
                    backgroundColor: [
                        window.chartColors.success,
                        window.chartColors.danger,
                    ],
                    label: 'Dataset 1'
                }],
                labels:[ 'Good', 'Bad']
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
        if(document.getElementById('feedback_sync')){
            var ctx = document.getElementById('feedback_sync').getContext('2d');
            window.myPie = new Chart(ctx, config);
        }
    }

    var init_chart16 = function () {
        var config = {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [chart_sync.performancesync.good, chart_sync.performancesync.bad],
                    backgroundColor: [
                    window.chartColors.success,
                    window.chartColors.danger,
                    ],
                    label: 'Dataset 1'
                }],
                labels: [ 'Good', 'Bad']
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        };
        if(document.getElementById('performance_sync')){
            var ctx = document.getElementById('performance_sync').getContext('2d');
            window.myPie = new Chart(ctx, config);

        }
    }


    //Intilize Chartjs function
    init_chart1();
    init_chart2();
    init_chart8();
    init_chart11();
    init_chart12();
    init_chart13();
    init_chart14();
    init_chart15();
    init_chart16();
});