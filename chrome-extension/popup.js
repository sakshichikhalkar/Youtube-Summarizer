const button = document.getElementById("summarizeBtn");
const resultBox = document.getElementById("result");

button.addEventListener("click", function() {
  resultBox.textContent = "Loading...";

  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentUrl = tabs[0].url;
    fetch(`http://localhost:8000/summarize?url=${encodeURIComponent(currentUrl)}`)
      .then(response => response.json())
      .then(data => {
        resultBox.textContent = data.summary;
      });
  });
});