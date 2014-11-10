/*jslint browser: true, onevar: true, undef: true, nomen: true, eqeqeq: true, plusplus: true, bitwise: true, newcap: true, immed: true, regexp: false, white:true */
/*global jQuery, ajax_noresponse_message, window */

jQuery(document).ready(function () {
    jQuery('.selImageToCropBtn').prepOverlay({
        subtype: 'ajax',
        filter: 'form#cropImage',
        config: {
            onLoad: function () {
                if (jQuery('img#croppableImage').length > 0) {
                    var field = jQuery('img#croppableImage').attr('data-field'),
                        scale = jQuery('img#croppableImage').attr('data-scale'),
                        ar = jQuery('img#croppableImage').attr('data-aspectratio'),
                        jcrop = jQuery.Jcrop('img#croppableImage'),
                        cropbox = null;
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
                            if (context_url.substr(-1) !== '/') {
                                context_url = context_url + '/';
                            }
                            jQuery.ajax({
                                type: 'GET',
                                url: context_url + '/@@cropimage/cropImage',
                                data: {field: field,
                                       scale: scale,
                                       x1: cropbox.x,
                                       y1: cropbox.y,
                                       x2: cropbox.x2,
                                       y2: cropbox.y2
                                      },
                                success: function () {
                                    window.location.replace(context_url + 'cropping');
                                }
                            });
                        });
                }
            }
        }
    });
});
