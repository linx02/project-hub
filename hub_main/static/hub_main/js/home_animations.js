document.addEventListener('DOMContentLoaded', function(){

    gsap.registerPlugin(ScrollTrigger);

    gsap.from('.hall-of-fame-card', {
        duration: 1.5, y: '5%',
        opacity: 0,
        ease: 'power4',
        stagger: 0.15,
        scrollTrigger: {
            trigger: '.hall-of-fame-card',
            start: 'top 80%'
        }
    });

    gsap.from('.recently-added-card', {
        duration: 1.5, y: '5%',
        opacity: 0,
        ease: 'power4',
        stagger: 0.15,
        scrollTrigger: {
            trigger: '.recently-added-card',
            start: 'top 80%'
        }
    });

    const headerWord = document.getElementById('header-word');
    
    const words = ['Share', 'Discuss', 'Test'];
    
    let currentWordIndex = 0;
    
    function animateWordTransition() {

        gsap.to(headerWord, {
            duration: 0.5,
            translateY: '-50%',
            opacity: 0,
            ease: 'power4.in',
            onComplete: function() {

                currentWordIndex = (currentWordIndex + 1) % words.length;
                headerWord.textContent = words[currentWordIndex];
                
                gsap.fromTo(headerWord, {
                    translateY: '50%',
                    opacity: 0,
                    ease: 'power4.out',
                }, {
                    duration: 0.5,
                    translateY: '0%',
                    opacity: 1,
                    ease: 'power4'
                });
            },
        });
    }
    
    setInterval(animateWordTransition, 5000);
    
    gsap.fromTo(headerWord, {
        opacity: 0,
    }, {
        duration: 0.5,
        opacity: 1,
    });
    
});