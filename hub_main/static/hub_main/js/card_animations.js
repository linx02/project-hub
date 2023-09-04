document.addEventListener('DOMContentLoaded', function(){
    
    let cards = document.querySelectorAll('.my-card');
    
    for(let card of cards){
        card.addEventListener('mouseenter', function(){
            gsap.to(card, { duration: 0.5, ease: "power2.out", scale: 1.02 });
        });
        card.addEventListener('mouseleave', function(){
            gsap.to(card, { duration: 0.5, ease: "power2.out", scale: 1 });
        });
    }

})