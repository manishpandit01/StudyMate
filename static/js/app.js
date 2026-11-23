document.addEventListener("DOMContentLoaded", function () {
  
  document.querySelectorAll("[data-password-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var input = document.getElementById(button.getAttribute("data-password-toggle"));
      if (!input) return;
      input.type = input.type === "password" ? "text" : "password";
      button.innerHTML = input.type === "password" ? '<i class="bi bi-eye"></i>' : '<i class="bi bi-eye-slash"></i>';
    });
  });

  document.querySelectorAll("[data-bookmark-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      var saved = button.getAttribute("aria-pressed") === "true";
      button.setAttribute("aria-pressed", String(!saved));
      button.innerHTML = saved
        ? '<i class="bi bi-bookmark"></i> Save to Study Guide'
        : '<i class="bi bi-bookmark-fill"></i> Saved to Study Guide';
    });
  });

  var questionBox = document.querySelector("[data-question-input]");
  var characterCount = document.querySelector("[data-character-count]");
  if (questionBox && characterCount) {
    var updateCount = function () { characterCount.textContent = questionBox.value.length + " / 1000"; };
    questionBox.addEventListener("input", updateCount);
    updateCount();
  }

  var fileInput = document.querySelector("[data-file-input]");
  var dropZone = document.querySelector("[data-drop-zone]");
  var fileName = document.querySelector("[data-file-name]");
  if (fileInput && dropZone) {
    var showFile = function (file) {
      if (!file) return;
      if (file.type !== "application/pdf") {
        if (fileName) fileName.textContent = "Please choose a PDF file.";
        fileInput.value = "";
        return;
      }
      if (fileName) fileName.textContent = file.name;
    };
    fileInput.addEventListener("change", function () { showFile(fileInput.files[0]); });
    dropZone.addEventListener("dragover", function (event) {
      event.preventDefault();
      dropZone.classList.add("dragover");
    });
    dropZone.addEventListener("dragleave", function () { dropZone.classList.remove("dragover"); });
    dropZone.addEventListener("drop", function (event) {
      event.preventDefault();
      dropZone.classList.remove("dragover");
      var file = event.dataTransfer.files[0];
      if (file && fileInput.files) {
        fileInput.files = event.dataTransfer.files;
      }
      showFile(file);
    });
  }

  document.querySelectorAll("[data-filter]").forEach(function (input) {
    input.addEventListener("input", function () {
      var selector = input.getAttribute("data-filter");
      var query = input.value.toLowerCase().trim();
      document.querySelectorAll(selector).forEach(function (item) {
        item.classList.toggle("d-none", !item.textContent.toLowerCase().includes(query));
      });
    });
  });

  document.querySelectorAll("[data-setting-toggle]").forEach(function (toggle) {
    toggle.addEventListener("change", function () {
      var label = toggle.closest(".form-check").querySelector("[data-toggle-state]");
      if (label) label.textContent = toggle.checked ? "On" : "Off";
    });
  });
});
