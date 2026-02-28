document.addEventListener("DOMContentLoaded", function () {
  // Element references
  const predictBtn = document.getElementById("predictBtn");
  const clearBtn = document.getElementById("clearBtn");
  const resultCard = document.getElementById("resultCard");
  const resultText = document.getElementById("resultText");
  const symptomSearch = document.getElementById("symptomSearch");
  const clearSearch = document.getElementById("clearSearch");
  const selectedCount = document.getElementById("selectedCount");
  const selectedTags = document.getElementById("selectedTags");
  const symptomsAnalyzed = document.getElementById("symptomsAnalyzed");
  const loadingOverlay = document.getElementById("loadingOverlay");
  const newAnalysis = document.getElementById("newAnalysis");
  const symptomItems = document.querySelectorAll(".symptom-item");
  const checkboxes = document.querySelectorAll("input[name='symptom']");

  // Update selected count and tags
  function updateSelectedState() {
    const selected = getSelectedSymptoms();
    selectedCount.textContent = selected.length;

    // Update tags
    if (selected.length > 0) {
      selectedTags.classList.remove("hidden");
      selectedTags.innerHTML = selected.map(symptom => `
        <span class="symptom-tag" data-value="${symptom}">
          ${formatSymptomName(symptom)}
          <button class="remove-tag" data-symptom="${symptom}">
            <i class="fas fa-times"></i>
          </button>
        </span>
      `).join("");

      // Add click handlers to remove buttons
      selectedTags.querySelectorAll(".remove-tag").forEach(btn => {
        btn.addEventListener("click", (e) => {
          e.stopPropagation();
          const symptomValue = btn.dataset.symptom;
          const checkbox = document.querySelector(`input[value="${symptomValue}"]`);
          if (checkbox) {
            checkbox.checked = false;
            updateSelectedState();
          }
        });
      });
    } else {
      selectedTags.classList.add("hidden");
    }
  }

  // Format symptom name for display
  function formatSymptomName(symptom) {
    return symptom.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
  }

  // Get selected symptoms
  function getSelectedSymptoms() {
    const checked = Array.from(document.querySelectorAll("input[name='symptom']:checked"));
    return checked.map(ch => ch.value);
  }

  // Search functionality
  symptomSearch.addEventListener("input", function () {
    const query = this.value.toLowerCase().trim();
    
    clearSearch.classList.toggle("hidden", query === "");

    symptomItems.forEach(item => {
      const symptomName = item.dataset.symptom;
      if (symptomName.includes(query) || query === "") {
        item.classList.remove("hidden-symptom");
      } else {
        item.classList.add("hidden-symptom");
      }
    });
  });

  clearSearch.addEventListener("click", function () {
    symptomSearch.value = "";
    clearSearch.classList.add("hidden");
    symptomItems.forEach(item => item.classList.remove("hidden-symptom"));
    symptomSearch.focus();
  });

  // Add change listeners to all checkboxes
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener("change", updateSelectedState);
  });

  // Predict button
  predictBtn.addEventListener("click", async function () {
    const symptoms = getSelectedSymptoms();
    
    if (symptoms.length === 0) {
      showNotification("Please select at least one symptom", "warning");
      return;
    }

    // Show loading
    loadingOverlay.classList.remove("hidden");
    resultCard.classList.add("hidden");

    try {
      // Add a slight delay for better UX
      await new Promise(resolve => setTimeout(resolve, 1500));

      const resp = await fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: symptoms })
      });

      const data = await resp.json();
      
      // Hide loading
      loadingOverlay.classList.add("hidden");

      if (data.success) {
        resultText.textContent = data.predicted_disease;
        symptomsAnalyzed.textContent = symptoms.length;
        resultCard.classList.remove("hidden");
        
        // Scroll to result
        resultCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      } else {
        showNotification("Prediction failed. Please try again.", "error");
      }
    } catch (err) {
      loadingOverlay.classList.add("hidden");
      showNotification("Server error. Please try again.", "error");
    }
  });

  // Clear button
  clearBtn.addEventListener("click", function () {
    checkboxes.forEach(ch => ch.checked = false);
    resultCard.classList.add("hidden");
    updateSelectedState();
    symptomSearch.value = "";
    clearSearch.classList.add("hidden");
    symptomItems.forEach(item => item.classList.remove("hidden-symptom"));
  });

  // New analysis button
  newAnalysis.addEventListener("click", function () {
    resultCard.classList.add("hidden");
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  // Simple notification function
  function showNotification(message, type = "info") {
    // Remove existing notification
    const existing = document.querySelector(".notification");
    if (existing) existing.remove();

    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
      <i class="fas ${type === 'warning' ? 'fa-exclamation-circle' : 'fa-times-circle'}"></i>
      <span>${message}</span>
    `;
    
    // Add styles
    Object.assign(notification.style, {
      position: 'fixed',
      top: '20px',
      right: '20px',
      padding: '16px 24px',
      background: type === 'warning' ? 'rgba(245, 158, 11, 0.9)' : 'rgba(239, 68, 68, 0.9)',
      color: 'white',
      borderRadius: '12px',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      fontSize: '14px',
      fontWeight: '500',
      zIndex: '9999',
      animation: 'slideInRight 0.3s ease',
      boxShadow: '0 10px 40px rgba(0,0,0,0.3)'
    });

    document.body.appendChild(notification);

    // Add animation keyframes if not exists
    if (!document.querySelector('#notification-styles')) {
      const style = document.createElement('style');
      style.id = 'notification-styles';
      style.textContent = `
        @keyframes slideInRight {
          from { transform: translateX(100%); opacity: 0; }
          to { transform: translateX(0); opacity: 1; }
        }
      `;
      document.head.appendChild(style);
    }

    // Remove after 3 seconds
    setTimeout(() => {
      notification.style.animation = 'slideInRight 0.3s ease reverse';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }

  // Add keyboard shortcuts
  document.addEventListener("keydown", function (e) {
    // Ctrl/Cmd + Enter to predict
    if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
      e.preventDefault();
      predictBtn.click();
    }
    // Escape to clear search
    if (e.key === "Escape" && symptomSearch === document.activeElement) {
      symptomSearch.value = "";
      clearSearch.classList.add("hidden");
      symptomItems.forEach(item => item.classList.remove("hidden-symptom"));
      symptomSearch.blur();
    }
  });

  // Initialize
  updateSelectedState();
});
