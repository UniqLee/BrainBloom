document.addEventListener("DOMContentLoaded", function () {
    // Fade-in effect for the promotional container
    const promoContainer = document.querySelector(".promo-container");
    promoContainer.style.opacity = "0";
    promoContainer.style.transform = "translateY(20px)";
    
    setTimeout(() => {
        promoContainer.style.transition = "opacity 1s ease, transform 1s ease";
        promoContainer.style.opacity = "1";
        promoContainer.style.transform = "translateY(0)";
    }, 200);

    // Button hover effect
    const buttons = document.querySelectorAll(".btn");
    buttons.forEach(button => {
        button.addEventListener("mouseover", () => {
            button.style.transform = "scale(1.05)";
            button.style.transition = "transform 0.3s ease";
        });

        button.addEventListener("mouseout", () => {
            button.style.transform = "scale(1)";
        });
    });
});