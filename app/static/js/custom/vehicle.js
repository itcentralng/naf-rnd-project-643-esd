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
                form.reset();
                $('#unallocated').load(location.href+" #unallocated>*","");
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