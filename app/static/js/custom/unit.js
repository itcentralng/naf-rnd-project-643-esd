$(document).on('click', '#addUnit', function(event){
    event.preventDefault();
    let name = $('#name').val();
    let location_ = $('#location').val();
    let command = $('#command').val();
    if (name && location_ && command){
        form = $('#unitForm')[0]
        req = $.ajax({
            url:'/unit',
            type:'post',
            contentType: false,
            processData: false,
            data: new FormData(form)
        });
        req.done(function(res){
            if (res.error){
                alert(res.error);
            }else{
                alert('Unit Added Successfully');
                form.reset();
                $('#dataTable').load(location.href+" #dataTable>*","");
            }
        });
    }else{
        alert('Please enter required fields')
    }
});