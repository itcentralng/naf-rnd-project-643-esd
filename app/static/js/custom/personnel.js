$(document).on('click', '#addPersonnel', function(event){
    event.preventDefault();
    form = $('#persForm')[0]
    req = $.ajax({
        url:'/personnel',
        type:'post',
        contentType: false,
        processData: false,
        data: new FormData(form)
    });
    req.done(function(res){
        if (res.error){
            alert(res.error);
        }else{
            alert('Personnel Registered Successfully');
            form.reset();
        }
    });
});