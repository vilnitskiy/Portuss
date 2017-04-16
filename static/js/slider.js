/**
 * Created by Admin on 02.01.2017.
 */
$(document).ready(function(){
    var main_swiper = new Swiper('.main-slider', {
        slidesPerView: 1,
        nextButton: '.main-slider-next-button',
        prevButton: '.main-slider-prev-button',
        speed: 1500,
        loop: "true"
    });
    var popular_cars = new Swiper('.popular-cars-slider', {
        slidesPerView: 4,
        spaceBetween: 30,
        nextButton: '.popular-cars-next',
        prevButton: '.popular-cars-prev',
        speed: 1500,
        loop: "true",
        breakpoints: {
            // when window width is <= 320px
            320: {
                slidesPerView: 1,
                spaceBetween: 10
            },
            700: {
                slidesPerView: 2,
                spaceBetween: 15
            },
            1024: {
                slidesPerView: 3,
                spaceBetween: 20
            }
        }
    });
    var popular_city = new Swiper('.popular-city-slider', {
        slidesPerView: 4,
        slidesPerColumn: 1,
        spaceBetween: 30,
        nextButton: '.popular-city-next',
        prevButton: '.popular-city-prev',
        speed: 1500,
        loop: "true",
        breakpoints: {
            320: {
                slidesPerView: 1,
                slidesPerColumn: 1,
                spaceBetween: 10
            },
            700: {
                slidesPerView: 2,
                slidesPerColumn: 1,
                spaceBetween: 15
            },
            1024: {
                slidesPerView: 3,
                slidesPerColumn: 1,
                spaceBetween: 20
            }
        }
    });
    var cc_gallery = new Swiper('.cc-gallery', {
        slidesPerView: 4,
        nextButton: '.cc-gallery-next',
        prevButton: '.cc-gallery-prev',
        spaceBetween: 20,
        speed: 1500,
        loop: "true"
    });
    var galleryTop = new Swiper('.gallery-top', {
        slidesPerView: 'auto',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        // centeredSlides: true,
        loop: true,
    });
    var galleryThumbs = new Swiper('.gallery-thumbs', {
        centeredSlides: true,
        slidesPerView: 'auto',
        nextButton: '.right-pagination-gallery-button',
        prevButton: '.left-pagination-gallery-button',
        slideToClickedSlide: true,
        // loopedSlides: 5,
        // slidesPerView: 4,
        loop: true,
        breakpoints: {
            // // when window width is <= 320px
            // 320: {
            //     slidesPerView: 1,
            // },
            // // when window width is <= 480px
            // 480: {
            //     slidesPerView: 2,
            // },
            // // when window width is <= 640px
            // 640: {
            //     slidesPerView: 3,
            // }
        }
    });
    galleryTop.params.control = galleryThumbs;
    galleryThumbs.params.control = galleryTop;
});