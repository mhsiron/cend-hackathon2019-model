$('#datefield').on('change',function(){

    $.ajax({
        url: "/date",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'datefield': document.getElementById('datefield').value

        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('bargraph', data );
        }
    });
})