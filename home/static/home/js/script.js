document.addEventListener('DOMContentLoaded', function () {
    let exploreCarousel = document.querySelector('#exploreCarousel');
    let carousel = new bootstrap.Carousel(exploreCarousel, {
        interval: 3000, // Changes slides every 3 seconds
        wrap: true // Ensures infinite loop
    });
});
