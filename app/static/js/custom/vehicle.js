$(document).on('click', '#addBulkVehicles', function(event){
    event.preventDefault();
    let file = $('#file').val()
    
    let unitId = $(this).attr('unitId')
    let url = '/vehicle/bulk'
    if (unitId){
        url += '/'+unitId
    }
    
    if (file){
        form = $('#bulkForm')[0]
        req = $.ajax({
            url:url,
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Vehicles Added Successfully');
                form.reset();
                $('#allocated').load(location.href+" #allocated>*","");
                $('#unallocated').load(location.href+" #unallocated>*","");
            }
        });
    }else{
        alert('Please enter required fields')
    }
});

$(document).on('click', '#addVehicle', function(event){
    event.preventDefault();
    let lifespan = $('#lifespan').val()
    let make = $('#make').val()
    let model = $('#model').val()
    let type = $('#type').val()
    let trim = $('#trim').val()
    let year = $('#year').val()
    let chassis_no = $('#chassis_no').val()
    let engine_no = $('#engine_no').val()
    let supplier = $('#supplier').val()
    let contract_reference = $('#contract_reference').val()
    let date = $('#date').val()
    let remarks = $('#remark').val()
    
    if (lifespan && make && model && trim && type && year && chassis_no && engine_no && supplier && contract_reference && date && remarks){
        form = $('#vehicleForm')[0]
        req = $.ajax({
            url:'/vehicle',
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Vehicle Added Successfully');
                form.reset();
                $('#unallocated').load(location.href+" #unallocated>*","");
            }
        });
    }else{
        alert('Please enter required fields')
    }
});

$(document).on('click', '#updateVehicle', function(event){
    event.preventDefault();

        let vehicleId = $(this).attr('vehicleId');

        form = $('#vehicleForm')[0]
        req = $.ajax({
            url:'/vehicle/'+vehicleId,
            type:'put',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Vehicle Updated Successfully');
                $('#unallocated').load(location.href+" #unallocated>*","");
                $('#allocated').load(location.href+" #allocated>*","");
            }
        });
});

$(document).on('click', '#addAllocation', function(event){
    event.preventDefault();

        let vehicleId = $(this).attr('vehicleId');

        form = $('#allocationForm')[0]
        req = $.ajax({
            url:'/vehicle/allocate/'+vehicleId,
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Vehicle Allocated Successfully');
                form.reset();
                $('#unallocated').load(location.href+" #unallocated>*","");
                $('#allocated').load(location.href+" #allocated>*","");
            }
        });
});

$(document).on('click', '#addLog', function(event){
    event.preventDefault();

        let vehicleId = $(this).attr('vehicleId');

        form = $('#logForm')[0]
        req = $.ajax({
            url:'/vehiclelog/'+vehicleId,
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Vehicle Log Saved Successfully');
                form.reset();
                $('#logbookTable').load(location.href+" #logbookTable>*","");
                $('#information').load(location.href+" #information>*","");
                $('#alertForm').load(location.href+" #alertForm>*","");
            }
        });
});

$(document).on('click', '#addMovement', function(event){
    event.preventDefault();

        let vehicleId = $(this).attr('vehicleId');

        form = $('#movementForm')[0]
        req = $.ajax({
            url:'/movement/'+vehicleId,
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Vehicle Log Saved Successfully');
                form.reset();
                $('#tableMovement').load(location.href+" #tableMovement>*","");
                $('#information').load(location.href+" #information>*","");
                $('#alertForm').load(location.href+" #alertForm>*","");
            }
        });
});

$(document).on('click', '#setAlert', function(event){
    event.preventDefault();

        let vehicleId = $(this).attr('vehicleId');

        form = $('#alertForm')[0]
        req = $.ajax({
            url:'/alert/'+vehicleId,
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Alert updated Successfully');
            }
        });
});