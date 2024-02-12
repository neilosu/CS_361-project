
document.getElementById('showTodayVocab').addEventListener('click', function() {
    // Example fetch request; replace URL with your actual endpoint
    fetch('http://localhost:8080/today')
    .then(response => response.json())
    .then(data => {
        localStorage.setItem('vocabData', JSON.stringify(data)); // Storing fetched data in localStorage
        window.location.href = 'vocabPage.html'; // Navigating to the vocab page
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('searchVocab').addEventListener('click', function() {
    window.location.href = 'searchPage.html'; // Make sure 'searchPage.html' is the correct path
});

document.getElementById('settings').addEventListener('click', function() {
    window.location.href = 'settingsPage.html'; // Make sure 'searchPage.html' is the correct path
});
