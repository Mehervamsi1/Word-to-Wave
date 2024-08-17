window.addEventListener('scroll', function() {
    const titleContainer = document.querySelector('.title-container');
    const navTitle = document.querySelector('.nav-title');
    const title = document.getElementById('title');
    const scrollY = window.scrollY;
    const threshold = 200; // Adjust this value based on how long you want the transition to take

    if (scrollY > 0 && scrollY < threshold) {
        const scale = 1 - (scrollY / threshold);
        const translateY = scrollY / 5; // Adjust this to control the movement speed
        title.style.fontSize = `${5 * scale}rem`;
        title.style.top = `${50 - translateY}%`;
        title.style.left = `${50 - translateY}%`;
        title.style.transform = `translate(-${50 - translateY}%, -${50 - translateY}%)`;
    } else if (scrollY >= threshold) {
        titleContainer.classList.add('scrolled');
        title.style.fontSize = '2rem';
        title.style.top = '10px';
        title.style.left = '10px';
        title.style.transform = 'translate(0, 0)';
        navTitle.style.opacity = '1';
    } else {
        titleContainer.classList.remove('scrolled');
        title.style.fontSize = '5rem';
        title.style.top = '50%';
        title.style.left = '50%';
        title.style.transform = 'translate(-50%, -50%)';
        navTitle.style.opacity = '0';
    }
});

function scrollToMainSection() {
    document.querySelector('.main-section').scrollIntoView({ behavior: 'smooth' });
}