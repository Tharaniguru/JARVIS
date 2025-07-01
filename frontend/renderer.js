document.addEventListener("DOMContentLoaded", () => {
  const core = document.getElementById("core");
  const buttonPanel = document.getElementById("buttonPanel");
  const recognizeBtn = document.getElementById("recognizeBtn");
  const stopBtn = document.getElementById("stopBtn");
  const collectBtn = document.getElementById("collectBtn");
  const nameInput = document.getElementById("nameInput");
  const micToggleBtn = document.getElementById("micToggleBtn");
  const micIcon = document.getElementById("micIcon");
  const statusText = document.getElementById("statusText");

  let isPanelOpen = false;
  let isListening = false;

  // Core opens/hides buttons (does NOT start mic)
  core.addEventListener("click", () => {
    isPanelOpen = !isPanelOpen;

    if (isPanelOpen) {
      buttonPanel.classList.add("show");
      Array.from(buttonPanel.children).forEach((el, i) => {
        el.style.animationDelay = `${i * 0.2}s`;
      });
    } else {
      buttonPanel.classList.remove("show");
    }
  });

  // Mic button toggles voice assistant
  micToggleBtn.addEventListener("click", () => {
    isListening = !isListening;

    if (isListening) {
      window.api.startListening();
      micIcon.textContent = "🎙️";
      micIcon.classList.remove("mic-idle");
      micIcon.classList.add("mic-active");
      statusText.textContent = "JARVIS is listening...";
      micToggleBtn.textContent = "❌";
    } else {
      window.api.stopListening();
      micIcon.textContent = "❌";
      micIcon.classList.remove("mic-active");
      micIcon.classList.add("mic-idle");
      statusText.textContent = "JARVIS is idle";
      micToggleBtn.textContent = "🎙️";
    }
  });

  recognizeBtn.addEventListener('click', () => {
    window.api.startRecognition();
  });

  stopBtn.addEventListener('click', () => {
    window.api.stopRecognition();
  });

  collectBtn.addEventListener('click', () => {
    const name = nameInput.value.trim();
    if (name) {
      window.api.startCollection(name);
    } else {
      alert("Please enter a name before collecting face data.");
    }
  });
});
