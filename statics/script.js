document.addEventListener('DOMContentLoaded', (event) => {
    const startTime = new Date().getTime();
    const timeLimit = 30 * 60 * 1000; // 30 minutes in milliseconds

    setInterval(() => {
        const currentTime = new Date().getTime();
        if (currentTime - startTime > timeLimit) {
            document.querySelector('form').innerHTML = '<p>Time limit exceeded. Access to update data denied.</p>';
        }
    }, 1000);
});
