/** poster.js */


function poster_widget_inject(elem)
{
    var inner = $("<div/>", {
        id: "poster_inner"
    });

    var txtid = "postsmg";
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

                   }, "json");
        }
    }).appendTo(inner);
}


onready(function() {
    poster_widget_inject($("#poster"));
});
