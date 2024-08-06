document.getElementById('scrollButton').addEventListener('click', function() {
    document.querySelector('main').scrollIntoView({ behavior: 'smooth' });
});

document.getElementById('record-icon').addEventListener('click', function() {
    this.classList.toggle('active');
});
