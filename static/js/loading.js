$(document).ready(function(){
    setInterval(function(){
        $.ajax({
            type:'GET',
            url: "/sales/loading-json/",
            success: function(data, status, xhr) { 
                //console.log(data);
               // console.log(typeof(data));
               // var keys = Object.keys(data);
                for (const [key, value] of Object.entries(data)) {
                    console.log(`${key}: ${value}`);
                    $('#50kg-count-'+key).html(value['50kg']);
                    $("#50kg-tweight-"+key).html(parseInt(value['50kg']) * 50);
                    $('#25kg-count-'+key).html(value['25kg']);
                    $("#25kg-tweight-"+key).html(parseInt(value['25kg']) * 25);
                    $('#20kg-count-'+key).html(value['20kg']);
                    $("#20kg-tweight-"+key).html(parseInt(value['20kg']) * 20);
                    $('#6kg-count-'+key).html(value['6kg']);
                    $("#6kg-tweight-"+key).html(parseInt(value['6kg']) * 6);
                    $("#counter-total-"+key).html(
                        (parseInt(value['50kg']) * 50) + (parseInt(value['25kg']) * 25)
                        + (parseInt(value['20kg']) * 20) + (parseInt(value['6kg']) * 6)
                        );
                  }
                
            } , 
        })
    },2000);
}); 