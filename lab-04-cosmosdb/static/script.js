function loadBlobsData(container) {
    console.log(container)
    $.ajax({
        type: "GET",
        url: "/get_blob",
        data: {
            "container": container
        },
        success: function (response) {
            $(this).check()
        }
    });
}