document.addEventListener('DOMContentLoaded', function(){
    let cards = document.querySelectorAll('.my-card');
    gsap.registerPlugin(ScrollTrigger);

    gsap.from('.hall-of-fame-card', {
        duration: .7, y: '5%',
        opacity: 0,
        ease: 'power4',
        scrollTrigger: {
            trigger: '.hall-of-fame-card',
            start: 'top 80%'
        }
    });

    gsap.from('.recently-added-card', {
        duration: .7, y: '5%',
        opacity: 0,
        ease: 'power4',
        scrollTrigger: {
            trigger: '.recently-added-card',
            start: 'top 80%'
        }
    });

    for(let card of cards){
        card.addEventListener('mouseenter', function(){
            gsap.to(card, { duration: 0.5, ease: "power2.out", scale: 1.02 });
        });
        card.addEventListener('mouseleave', function(){
            gsap.to(card, { duration: 0.5, ease: "power2.out", scale: 1 });
        });
    }
})