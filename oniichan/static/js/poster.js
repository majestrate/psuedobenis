/** poster.js */


function poster_widget_inject(elem)
{
    var inner = $("<div/>", {
        id: "poster_inner"
    });

    var txtid = "postsmg";
    var poster_info_id = "poster_msg";

    var change_text = function(msgtxt, fadeout) {
        $("#"+poster_info_id).text(msgtxt);
        console.log("change poster text to '"+msgtxt+"'");
        if(fadeout) $("#"+poster_info_id).delay(fadeout).fadeOut(100);
    };

    $("<div/>", {
        id :poster_info_id
    }).appendTo(inner);

    inner.appendTo(elem);
    $("<textarea/>", {
        id: txtid,
    }).appendTo(inner);
    $("<input/>", {
        type: "button",
        value: "post",
        click: function() {
            var txt = $("#"+txtid).val();
            $.post("/api/post.json", /* api endpoint */
                   {message:txt}, /* post data */
                   function(data, text, xhr) { /* success func */
                       var j = text;
                       
                       if(j.error) {
                           change_text("posting error: "+j.error, 1000);
                       } else {
                           change_text("posted :D", 1000);
                       }
                   }, "json");
        }
    }).appendTo(inner);
}


onready(function() {
    poster_widget_inject($("#poster"));
});
