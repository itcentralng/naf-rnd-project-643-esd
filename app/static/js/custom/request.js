$(document).on('click', '.acceptAllocation', function(event){
    event.preventDefault();
    let allocationId = $(this).attr('allocationId');
        req = $.ajax({
            url:'/vehicle/accept/'+allocationId,
            type:'patch'
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Allocation accepted successfully!');
                $('#vehicleAllocation').load(location.href+" #vehicleAllocation>*","");
                $('#vehicleReallocation').load(location.href+" #vehicleReallocation>*","");
            }
        });
});
$(document).on('click', '.rejectAllocation', function(event){
    event.preventDefault();
    let allocationId = $(this).attr('allocationId');
        req = $.ajax({
            url:'/vehicle/reject/'+allocationId,
            type:'patch'
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Allocation accepted successfully!');
                $('#vehicleAllocation').load(location.href+" #vehicleAllocation>*","");
                $('#vehicleReallocation').load(location.href+" #vehicleReallocation>*","");
            }
        });
});
