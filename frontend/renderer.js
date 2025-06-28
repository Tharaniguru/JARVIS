document.addEventListener("DOMContentLoaded", () => {
  const core = document.getElementById("core");
  const buttonPanel = document.getElementById("buttonPanel");

  core.addEventListener("click", () => {
    if (!buttonPanel.classList.contains("show")) {
      buttonPanel.classList.add("show");

      // Animate each button with staggered delay
      const children = buttonPanel.children;
      for (let i = 0; i < children.length; i++) {
        const el = children[i];
        el.style.animationDelay = `${i * 0.2}s`;
      }
    } else {
      buttonPanel.classList.remove("show");
    }
  });

  // Button functionality
  document.getElementById('recognizeBtn').addEventListener('click', () => {
    window.api.startRecognition();
  });

  document.getElementById('stopBtn').addEventListener('click', () => {
    window.api.stopRecognition();
  });

  document.getElementById('collectBtn').addEventListener('click', () => {
    const name = document.getElementById('nameInput').value.trim();
    if (name) {
      window.api.startCollection(name);
    } else {
      alert("Please enter a name before collecting face data.");
    }
  });
});
