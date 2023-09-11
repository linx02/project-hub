document.addEventListener('DOMContentLoaded', function(){

    gsap.registerPlugin(ScrollTrigger);

    gsap.from('.hall-of-fame-card', {
        duration: 1.5, y: '5%',
        opacity: 0,
        ease: 'power4',
        scrollTrigger: {
            trigger: '.hall-of-fame-card',
            start: 'top 80%'
        }
    });

    gsap.from('.recently-added-card', {
        duration: 1.5, y: '5%',
        opacity: 0,
        ease: 'power4',
        scrollTrigger: {
            trigger: '.recently-added-card',
            start: 'top 80%'
        }
    });
    
});