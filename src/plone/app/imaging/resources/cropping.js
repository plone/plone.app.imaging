scaleBoxes = {};

function cropAreaChanged(field, scale, coords) {
    console.log(field);
    console.log(scale);
    console.log(coords);
    scaleBoxes[[field, scale]] = coords;
}


$(window).load(function () {
    $('img.croppableImage').each(function () {
        var self = this;
        var ar = $(this).attr('data-aspectratio');
        var field = $(this).attr('data-field');
        var scale = $(this).attr('data-scale');
        var selector = '#' + this.id;
        var jcrop = $.Jcrop(selector);
        jcrop.setOptions({aspectRatio: ar,
                          allowSelect: true,
                          allowResize: true,
                          allowMove: true,
                          onSelect: function (coords) {
                                        cropAreaChanged(field, scale, coords);
                                    }
                          });
        jcrop.focus();
    });

    $('button.cropImageButton').click(function (event) {
        event.preventDefault();
        var field = $(this).attr('data-field');
        var scale = $(this).attr('data-scale');
        var context_url = $('base').attr('href');
        if (!([field, scale] in scaleBoxes)) {
            return;
        }
        var box = scaleBoxes[[field, scale]];
        $.ajax({
            type: "GET",
            url: context_url+'/@@cropping/cropImage',
            data: {field: field,
                   scale: scale,
                   x1: box.x,
                   y1: box.y,
                   x2: box.x2,
                   y2: box.y2
                  }
        });
    });
});

