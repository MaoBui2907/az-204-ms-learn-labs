function loadBlobsData(container) {
    console.log(container)
    $.ajax({
        type: "GET",
        url: "/get_blobs",
        data: {
            "container": container
        },
        success: function (response) {
            $(this).check()
        }
    });
}

$('#uploadForm').submit(function (e) { 
    e.preventDefault();
    var data = $(this);
    var file = $('#media')
    
    $.ajax({
        type: "POST",
        url: "/upload",
        data: data.serialize()
    })
});