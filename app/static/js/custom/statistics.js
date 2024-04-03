$(document).on('click', '#searchStats', function(event){
    event.preventDefault();
        form = $('#statsForm')[0]
        req = $.ajax({
            url:'/statistics/data',
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{

                // Set Datatable
                    let unitId = $('#unit_id').val();
                    let make = $('#make').val();
                    let model = $('#model').val();
                    let year = $('#year').val();

                    $('#resultTable').DataTable({
                        "ajax": `/statistics/table?unit_id=${unitId}&make=${make}&model=${model}&year=${year}`
                    });
                
                // Set Chart
                
                // Set new default font family and font color to mimic Bootstrap's default styling
                Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
                Chart.defaults.global.defaultFontColor = '#292b2c';

                // Pie Chart Example
                var ctx = document.getElementById("statisticsChart");
                var statisticsChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: res.labels,
                    datasets: [{
                    data: res.data,
                    backgroundColor: res.colors,
                    }],
                },
                });

            }
        });
});