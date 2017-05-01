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
    var $fnb=$(".form-next-step-button"),
        $fpb=$(".form-prev-step-button");
    $(".pre-active").removeClass("pre-active").addClass("active-tab").slideToggle(1);

    $.ajaxSetup({ 
         beforeSend: function(xhr, settings) {
             function getCookie(name) {
                 var cookieValue = null;
                 if (document.cookie && document.cookie != '') {
                     var cookies = document.cookie.split(';');
                     for (var i = 0; i < cookies.length; i++) {
                         var cookie = jQuery.trim(cookies[i]);
                         // Does this cookie string begin with the name we want?
                         if (cookie.substring(0, name.length + 1) == (name + '=')) {
                             cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                             break;
                         }
                     }
                 }
                 return cookieValue;
             }
             if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                 // Only send the token to relative URLs i.e. locally.
                 xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
             }
         } 
    });

    $.ajax({
        url: rent_url,
        type: "GET",
        dataType: 'html',
        success: function (data) {
            $('#form_rent_wizard').prepend(data);
        },
        error: function(data){
            console.log(data);
        }
    });

    function display_errors(errors){
        $('.error').remove();
        for (var k in errors) {
            if (errors[k] != 'errors_marker_value') {
                $("#form_rent_wizard").append(errors[k]);
            }
       }
    }

    var next_step = 1;
    $fnb.click(function(e){
        var serializedData = $('#form_rent_wizard').serialize() + '&next_step=' + next_step;
        $.ajax({
            url: rent_url,
            data: serializedData,
            type: "POST",
            success: function (data) {
                for (var k in data) {
                    if (data[k] == 'errors_marker_value') {
                        display_errors(data);
                    }
                }
                if (data == 'OK') {
                    console.log('redirect');
                    window.location.replace(main_url);
                }
                else if (data['errors_marker_key'] == undefined){
                    $('#form_rent_wizard').find('*').not($fnb).remove();
                    $('#form_rent_wizard').prepend(data);
                    // increase next_step till the forms in multistep form end
                    if (next_step != 5) {
                        next_step++;
                    }
                    console.log(next_step);
                    e.preventDefault();
                    var $cur_dp_tab=$(".dp-tab-active"),
                        $cur_ac_tab=$(".active-form-tab");
                    $cur_ac_tab.removeClass("active-form-tab").addClass('non-active-tab').next().addClass("active-form-tab").removeClass('non-active-tab');
                    $cur_dp_tab.removeClass("dp-tab-active").addClass('dp-tab-inactive').next().addClass("dp-tab-active").removeClass('non-active-tab');
                }
            },
            error: function(data){
                var errors = data.responseJSON;
                console.log(errors);
            }
        });
    });

    $fpb.click(function(e){
        e.preventDefault();
        var $cur_tab=$(".active-tab"),
            $cur_dp_tab=$(".dp-tab-active"),
            $cur_ac_tab=$(".active-form-tab");
        $cur_tab.removeClass("active-tab").slideToggle(1).prev().slideToggle(1).addClass("active-tab");
        $cur_ac_tab.removeClass("active-form-tab").addClass('non-active-tab').prev().addClass("active-form-tab").removeClass('non-active-tab');
        $cur_dp_tab.removeClass("dp-tab-active").addClass('dp-tab-inactive').prev().addClass("dp-tab-active").removeClass('non-active-tab');
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
    $('.view-profile').click(function(event){
        event.preventDefault();
        $('.profile-submenu').slideToggle();
    });
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
    $( function() {
        var dateFormat = "mm/dd/yy",
            from = $( "#rent-terms-from" )
                .datepicker()
                .on( "change", function() {
                    to.datepicker( "option", "minDate", getDate( this ) );
                }),
            to = $( "#rent-terms-to" ).datepicker()
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
    var $com_tab=$('.comment-tab');
    $('.clients-tab').click(function (event) {
        event.preventDefault();
        $com_tab.removeClass('active');
        $(this).addClass('active');
        $('.clients-reviews').css('display','block');
        $('.owners-reviews').css('display','none');
    });
    $('.owners-tab').click(function (event) {
        event.preventDefault();
        $com_tab.removeClass('active');
        $(this).addClass('active');
        $('.clients-reviews').css('display','none');
        $('.owners-reviews').css('display','block');
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
    var $hiw_tab=$('.hiw-tab'),
        $cur_hiw_tab=$('.active-hiw-tab').attr('data-tab-index'),
        $hiw_content=$('.hiw-tab-content');
    $hiw_tab.click(function () {
        if($cur_hiw_tab!=$(this).attr('data-tab-index')){
            $hiw_tab.removeClass('active-hiw-tab');
            $(this).addClass('active-hiw-tab');
            $cur_hiw_tab=$(this).attr('data-tab-index');
            $hiw_content.fadeOut(300);
            setTimeout(function () {
                $('.hiw-tab-content[data-tab-index="'+$cur_hiw_tab+'"]').fadeIn(300);
            }, 300);
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
    $('.massages-sector').niceScroll();
    document.getElementById('car-gallery-load').addEventListener('change', handleFileSelect, false);

});
