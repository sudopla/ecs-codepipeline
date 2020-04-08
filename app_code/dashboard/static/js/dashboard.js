type = ['','info','success','warning','danger'];

ajax_requests = [];

dashboard = {


    //AWS Page
    initAWS: function(){

        $.each(ajax_requests, function(idx, jqXHR) {
            jqXHR.abort();
        });


        //Storage Usage
        $.ajax({
                url: '/aws/storage',
                dataType: 'json',
                beforeSend: function (xhr){
                    ajax_requests.push(xhr)
                },
                success: function (json) {
                    var labels_current_storage = ['EBS Volumes - ', 'Snapshots - ', 'S3 - '];
                    var colors_storage = ['#72788d', '#84dcc6', '#ffa69e'];
                    var current_storage_values = json.values;

                    dashboard.createPieChart(current_storage_values, 'AWSStorageChart', colors_storage, labels_current_storage, 'GB');
                }
            });

        //Bar Graph - Monthly Storage Usage
        $.ajax({
                url: '/aws/storage_monthly_usage',
                dataType: 'json',
                beforeSend: function (xhr){
                    ajax_requests.push(xhr)
                },
                success: function (json) {
                    var colors_storage = ['#72788d', '#84dcc6', '#ffa69e'];
                    var x_legend = json.months;
                    var ebs_space = json.ebs_values;
                    var snaphots_space = json.snapshots_values;
                    var s3_space = json.s3_values;
                    var list_bars_labels = ['EBS Volumes', 'Snapshots', 'S3'];
                    var list_values = [ebs_space, snaphots_space, s3_space];

                    dashboard.createBarChart('StorageUsageAWS', 'GB-Month', x_legend, list_bars_labels, list_values, colors_storage);
                }
            });

        //Bar Graph - Monthly costs by service
         $.ajax({
                url: '/aws/monthly_costs',
                dataType: 'json',
                beforeSend: function (xhr){
                    ajax_requests.push(xhr)
                },
                success: function (json) {
                    list_bars_labels = ['EC2-Instances', 'RDS', 'Direct Connect', 'Support', 'VPC', 'EKS', 'EC2-Others', 'Others'];
                    var x_legend = json.months;
                    var ec2_costs = json.ec2_values;
                    var direct_connect_costs = json.direct_connect_values;
                    var support_costs = json.support_values;
                    var vpc_costs = json.vpc_values;
                    var ec2_other_costs = json.ec2_other_values;
                    var other_costs = json.others_values;
                    //
                    var rds_costs = json.rds_values;
                    var eks_costs = json.eks_values
                    list_values = [ec2_costs, rds_costs, direct_connect_costs, support_costs, vpc_costs, eks_costs, ec2_other_costs, other_costs];
                    var list_bars_colors = ['#6A45CE', '#19647e', '#2DB1A1', '#FF6E61', '#FED918', '#80A1C1', '#A51E54', '#3ECC54'];
                    var months_totals = json.months_totals

                    dashboard.createBarChart('MonthlyCostsAWS', '$', x_legend, list_bars_labels, list_values, list_bars_colors, months_totals);
                }
            });


    },


    //FUNCTIONS

    createPieChart: function (values, element, colors, labels, metric_unit) {

        var labels_temp = [];

        //Add metric unit to labels
        labels.forEach(function (label_value, i) {
            labels_temp[i] = label_value +values[i]+metric_unit
        });

        var data = {
            // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: labels_temp,
                datasets: [{
                     data: values,
                     backgroundColor: colors
                }]
        };

        var options = { legend: {
                display: true,
                position: 'right',
                labels :{
                    fontColor: '#333333',
                    fontSize: 12
                }
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, chartData) {
                        return chartData.labels[tooltipItem.index];
                    }
                }
            },
            responsive: true
        };

        var ctx = document.getElementById(element).getContext('2d');

        var myPieChart = new Chart(ctx,{
            type: 'pie',
            data: data,
            options: options
        });

        return myPieChart;

    },

    createBarChart: function (element, metric_unit, labels, list_bars_labels, list_values, list_bars_colors, totals_list = 0) {

        datasets_list = []

        list_bars_labels.forEach(function (label_bar_value, i) {
            datasets_list[i] = {
                label: label_bar_value,
                data: list_values[i],
                backgroundColor: list_bars_colors[i],
                borderWidth: 0
            }
        });

        var data = {
            // These labels appear in the legend and in the tooltips when hovering different arcs
            labels: labels,
            datasets: datasets_list
        };

        var options = { legend: {
                display: true,
                position: 'right',
                labels :{
                    fontColor: '#333333',
                    fontSize: 12
                }
            },
            tooltips: {
                footerFontStyle: 'normal',
                callbacks: {
                    label: function(tooltipItem, chartData) {
                        if (metric_unit == '$') {
                            return chartData.datasets[tooltipItem.datasetIndex].label + ' ' + metric_unit + tooltipItem.yLabel;
                        } else {
                            return chartData.datasets[tooltipItem.datasetIndex].label + ' ' + tooltipItem.yLabel + metric_unit;
                        }
                    },
                    footer: function(tooltipItem, chartData) {
                         if (metric_unit == '$' && totals_list != 0) {
                            //NEED TO FIND THE X LEGEND AND THEN USE THAT NUMBER IN A LIST OF THE TOTAL VALUES FOR EACH MONTH
                            return 'Total Cost: $' + totals_list[tooltipItem[0].index];
                         }
                    }
                }
            },
            scales: {
                yAxes: [{
                    ticks: {
                        // Include a dollar sign in the ticks
                        callback: function(value, index, values) {
                            if (metric_unit == '$') {
                                return metric_unit + value;
                            } else {
                                return value + metric_unit;
                            }
                        },
                        beginAtZero: true
                    }
                }]
            },
            responsive: true
        };

        var ctx = document.getElementById(element).getContext('2d');

        var myBarChart = new Chart(ctx,{
            type: 'bar',
            data: data,
            options: options
        });

        return myBarChart;
    }

};
