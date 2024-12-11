document.addEventListener("scroll", () => {
    const elements = document.querySelectorAll(".scroll-hidden");
    elements.forEach((element) => {
        const rect = element.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
            element.classList.add("scroll-visible");
        }
    });
});

// Trigger the scroll animation immediately on page load
window.addEventListener("load", () => {
    document.dispatchEvent(new Event("scroll"));
});