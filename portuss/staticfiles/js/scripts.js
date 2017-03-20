/**
 * Created by Admin on 04.10.2016.
 */
$(document).ready(function(){
    $( function() {
        var $tags=$(".city-search").attr('data-auto-complete');
        var availableTags = [
            $tags
        ];
        console.log($tags);
        $( "#city-search" ).autocomplete({
            source: availableTags
        });
    } );
    var $fnb=$(".form-next-step-button");
    $(".pre-active").removeClass("pre-active").addClass("active-tab").slideToggle(1);
    $fnb.click(function(e){
        e.preventDefault();
        var $cur_tab=$(".active-tab"),
            $cur_ac_tab=$(".active-form-tab");
        $cur_tab.removeClass("active-tab").slideToggle(1).next().slideToggle(1).addClass("active-tab");
        $cur_ac_tab.removeClass("active-form-tab").addClass('non-active-tab').next().addClass("active-form-tab").removeClass('non-active-tab');
    });
    $( function() {
        $( "#form-datepicker" ).datepicker();
    });
    $( function() {
        $( "#page-search-date" ).datepicker({
            showOn: "button",
            buttonImage: "./images/calendar.png",
            buttonImageOnly: true,
            buttonText: "Select date"
        });
    } );
    var $pre_price=$('.pre-price-block');
    $( function() {
        var dateFormat = "mm/dd/yy",
            from = $( "#book-date-from" )
                .datepicker()
                .on( "change", function() {
                    to.datepicker( "option", "minDate", getDate( this ) );
                }),
            to = $( "#book-date-to" ).datepicker()
                .on( "change", function() {
                    $pre_price.show(400);
                    from.datepicker( "option", "maxDate", getDate( this ) );
                });
        function getDate( element ) {
            var date;
            try {
                date = $.datepicker.parseDate( dateFormat, element.value );
            } catch( error ) {
                date = null;
            }
            return date;
        }
    } );
    // $('.datepicker').keydown(function(e) {
    //     e.preventDefault();
    //     return false;
    // });
    $( function() {
        var dateFormat = "mm/dd/yy",
            from = $( "#page-search-date-from" )
                .datepicker()
                .on( "change", function() {
                    to.datepicker( "option", "minDate", getDate( this ) );
                }),
            to = $( "#page-search-date-to" ).datepicker()
                .on( "change", function() {
                    from.datepicker( "option", "maxDate", getDate( this ) );
                });
        function getDate( element ) {
            var date;
            try {
                date = $.datepicker.parseDate( dateFormat, element.value );
            } catch( error ) {
                date = null;
            }
            return date;
        }
    } );
    // sliders-section
    var $ds_mf=$('#ds-mf-slider'),
        $ds_mf_amount=$('#ds-mf-display'),
        $ds_mf_attr=$('#ds-mf-slider-attributes'),
        $rent_slider_attr=$(".rent-slider-attributes"),
        $rent_slider_display=$("#form-rent-term"),
        $rent_slider=$("#rent-slider"),
        $ds_ml=$('#ds-ml-slider'),
        $ds_ml_amount=$('#ds-ml-display'),
        $ds_ml_attr=$('#ds-ml-slider-attributes'),
        $ds_pr=$('#ds-pr-slider'),
        $ds_pr_amount=$('#ds-pr-display'),
        $ds_pr_attr=$('#ds-pr-slider-attributes');
    $( function() {
        $rent_slider.slider({
            min: +$rent_slider_attr.attr('data-min'),
            max: +$rent_slider_attr.attr('data-max'),
            step: +$rent_slider_attr.attr('data-step'),
            value: +$rent_slider_attr.attr('data-initial-place'),
            slide: function( event, ui ) {
                $rent_slider_display.val( ui.value);
            }
        });
        $rent_slider_display.val($rent_slider.slider("value"));

        $ds_mf.slider({
            range: true,
            min: +$ds_mf_attr.attr('data-range-min'),
            max: +$ds_mf_attr.attr('data-range-max'),
            step: +$ds_mf_attr.attr('data-range-step'),
            values: [ +$ds_mf_attr.attr('data-range-min-initial'), +$ds_mf_attr.attr('data-range-max-initial') ],
            slide: function( event, ui ) {
                $ds_mf_amount.val( ui.values[ 0 ] + "-" + ui.values[ 1 ] + " " + $ds_mf_attr.attr('data-range-postfix') );
            }
        });
        $ds_mf_amount.val($ds_mf.slider( "values", 0 ) +
            "-" + $ds_mf.slider( "values", 1 ) + " " + $ds_mf_attr.attr('data-range-postfix') );

        $ds_ml.slider({
            range: true,
            min: +$ds_ml_attr.attr('data-range-min'),
            max: +$ds_ml_attr.attr('data-range-max'),
            step: +$ds_ml_attr.attr('data-range-step'),
            values: [ +$ds_ml_attr.attr('data-range-min-initial'), +$ds_ml_attr.attr('data-range-max-initial') ],
            slide: function( event, ui ) {
                $ds_ml_amount.val( ui.values[ 0 ] + "-" + ui.values[ 1 ] + " " + $ds_ml_attr.attr('data-range-postfix') );
            }
        });
        $ds_ml_amount.val($ds_ml.slider( "values", 0 ) +
            "-" + $ds_ml.slider( "values", 1 ) + " " + $ds_ml_attr.attr('data-range-postfix') );

        $ds_pr.slider({
            range: true,
            min: +$ds_pr_attr.attr('data-range-min'),
            max: +$ds_pr_attr.attr('data-range-max'),
            step: +$ds_pr_attr.attr('data-range-step'),
            values: [ +$ds_pr_attr.attr('data-range-min-initial'), +$ds_pr_attr.attr('data-range-max-initial') ],
            slide: function( event, ui ) {
                $ds_pr_amount.val( ui.values[ 0 ] + "-" + ui.values[ 1 ] + " " + $ds_pr_attr.attr('data-range-postfix') );
            }
        });
        $ds_pr_amount.val($ds_pr.slider( "values", 0 ) +
            "-" + $ds_pr.slider( "values", 1 ) + " " + $ds_pr_attr.attr('data-range-postfix') );
    } );
    var $ds_trigger=$('.detailed-search'),
        $ds=$('.detailed-search-block'),
        $di_trigger=$('.cc-detailed-info'),
        $di=$('.cc-detailed-info-block');
    $ds_trigger.on('click', function(e){
        e.preventDefault();
        $ds.slideToggle(400);
    });
    $di_trigger.on('click', function(e){
        e.preventDefault();
        $di.slideToggle(400);
    });

    var $mob_menu_trigger=$('.mobile-menu-burger'),
        $mob_menu=$('.mob-menu'),
        $mob_1=$('.mob-block-1'),
        $mob_2=$('.mob-block-2'),
        $mob_3=$('.mob-block-3'),
        $mob_search_trigger=$('.mob-block-3 .icon'),
        $mob_search_form=$('.mob-block-3 .header-search'),
        event = jQuery.Event( "submit" );

    $mob_search_trigger.click(function () {
        if($mob_3.hasClass('ready')){
            $mob_search_form.trigger( event );
        } else {
            $mob_3.addClass('ready');
        }
    });
    $mob_menu_trigger.click(function () {
        $mob_menu.toggleClass('it-begins');
        if($mob_menu.hasClass('it-begins')){
            $mob_menu.addClass('triggered');
            setTimeout(function () {
                $mob_1.addClass('ready');
            }, 400);
            setTimeout(function () {
                $mob_2.addClass('ready');
            }, 800);
        } else {
            if($mob_3.hasClass('ready')){
                $mob_3.removeClass('ready');
                setTimeout(function () {
                    $mob_2.removeClass('ready');
                }, 400);
                setTimeout(function () {
                    $mob_1.removeClass('ready');
                }, 800);
                setTimeout(function () {
                    $mob_menu.removeClass('triggered');
                }, 1200);
            } else{
                $mob_2.removeClass('ready');
                setTimeout(function () {
                    $mob_1.removeClass('ready');
                }, 400);
                setTimeout(function () {
                    $mob_menu.removeClass('triggered');
                }, 800);
            }
        }
    });

    function handleFileSelect(evt) {
        var files = evt.target.files; // FileList object

        // Loop through the FileList and render image files as thumbnails.
        for (var i = 0, f; f = files[i]; i++) {

            // Only process image files.
            if (!f.type.match('image.*')) {
                continue;
            }

            var reader = new FileReader();

            // Closure to capture the file information.
            reader.onload = (function (theFile) {
                return function (e) {
                    // Render thumbnail.
                    var span = document.createElement('span');
                    span.innerHTML = ['<img class="thumb" src="', e.target.result,
                        '" title="', escape(theFile.name), '"/>'].join('');
                    document.getElementById('previewImg').insertBefore(span, null);
                };
            })(f);

            // Read in the image file as a data URL.
            reader.readAsDataURL(f);
        }
    }
    (function($,undefined) {
        $(".gallery-thumbs .swiper-slide").bind("click", function(event) {
            $('.gallery-top').addClass('opened-gallery-top');
        });
        $(".gallery-close").bind("click", function(event) {
            $('.gallery-top').removeClass('opened-gallery-top');
        });
    })($);

    document.getElementById('car-gallery-load').addEventListener('change', handleFileSelect, false);


});