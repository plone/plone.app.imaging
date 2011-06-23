jQuery(document).ready(function () {
    jQuery('.selImageToCropBtn').prepOverlay({
         subtype: 'ajax',
         config: {
             onLoad: function () {
                 var cropbox = null;
                 if (jQuery('img#croppableImage').length > 0) {
                     var field = jQuery('img#croppableImage').attr('data-field');
                     var scale = jQuery('img#croppableImage').attr('data-scale');
                     var ar = jQuery('img#croppableImage').attr('data-aspectratio');
                     var jcrop = jQuery.Jcrop('img#croppableImage');
                     jcrop.setOptions({aspectRatio: ar,
                                       allowSelect: true,
                                       allowResize: true,
                                       allowMove: true,
                                       onSelect: function (coords) {
                                           jQuery('input#image-recrop').removeAttr('disabled');
                                           cropbox = coords;
                                       }
                      });
                     jcrop.focus();

                     jQuery('input#image-recrop').click(function (e) {
                         e.preventDefault();
                         var context_url = jQuery('base').attr('href');
                         jQuery.ajax({
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


             }
         },
     });
});
