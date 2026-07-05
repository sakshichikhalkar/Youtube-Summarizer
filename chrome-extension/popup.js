const button = document.getElementById("summarizeBtn");
const resultBox = document.getElementById("result");
const summaryTypeSelect = document.getElementById("summaryType");

button.addEventListener("click", function() {
  resultBox.textContent = "Loading...";

  const selectedType = summaryTypeSelect.value;

  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    const currentUrl = tabs[0].url;

    if (!currentUrl.includes("youtube.com") && !currentUrl.includes("youtu.be")) {
      resultBox.textContent = "Please open a YouTube video first.";
      return;
    }

    fetch(`http://youtube-summarizer-api-production-28a9.up.railway.app/summarize?url=${encodeURIComponent(currentUrl)}&summary_type=${selectedType}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          resultBox.textContent = "Error: " + data.error;
        } else {
          resultBox.textContent = data.summary;
        }
      })
      .catch(error => {
        resultBox.textContent = "Could not connect to server. Is it running?";
      });
  });
});