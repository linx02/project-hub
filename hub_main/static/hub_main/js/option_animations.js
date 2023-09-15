document.addEventListener('DOMContentLoaded', function(){

    const postOptions = document.querySelectorAll('.post-option');
    for(let option of postOptions){
        option.addEventListener('mouseenter', function(){
            gsap.to(option, { duration: 0.5, ease: "power2.out", y: -3 });
        });
        option.addEventListener('mouseleave', function(){
            gsap.to(option, { duration: 0.5, ease: "power2.out", y: 0 });
        });

        option.addEventListener('click', function(){
            
        });
    }

});