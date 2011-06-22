
$(window).load(function () {
    var cropbox = null;
    if ($('img#croppableImage').length > 0) {
        var field = $('img#croppableImage').attr('data-field');
        var scale = $('img#croppableImage').attr('data-scale');
        var ar = $('img#croppableImage').attr('data-aspectratio');
        var jcrop = $.Jcrop('img#croppableImage');
        jcrop.setOptions({aspectRatio: ar,
                          allowSelect: true,
                          allowResize: true,
                          allowMove: true,
                          onSelect: function (coords) {
                              $('input#image-recrop').removeAttr('disabled');
                              cropbox = coords;
                          }
         });
        jcrop.focus();

        $('input#image-recrop').click(function (e) {
            e.preventDefault();
            var context_url = $('base').attr('href');
            $.ajax({
               type: "GET",
               url: context_url+'/@@cropimage/cropImage',
               data: {field: field,
                      scale: scale,
                      x1: cropbox.x,
                      y1: cropbox.y,
                      x2: cropbox.x2,
                      y2: cropbox.y2
                     },
               success: function () {
                   window.location.replace(context_url+'/cropping');
               }
            });
        });
    }
});

