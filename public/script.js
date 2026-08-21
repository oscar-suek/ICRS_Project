// --- Intro modal ---------------------------------------------------------
const overlay = document.getElementById("intro-modal-overlay");
const closeBtn = document.getElementById("close-intro-modal");
const aboutBtn = document.getElementById("about-btn");

if (overlay && closeBtn) {
  // Always shown on page load.
  overlay.classList.remove("hidden");

  closeBtn.addEventListener("click", () => {
    overlay.classList.add("hidden");
  });

  // Also close on clicking the dark backdrop (but not the modal box itself)
  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      overlay.classList.add("hidden");
    }
  });

  if (aboutBtn) {
    aboutBtn.addEventListener("click", () => {
      overlay.classList.remove("hidden");
    });
  }
}

// --- Prediction form -------------------------------------------------------
const form = document.getElementById("predict-form");
const resultBox = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Backstop check — min/max on the inputs already block the browser's
  // native submit, but this catches pasted or scripted values too.
  const invalid = [];
  for (const input of form.querySelectorAll("input[type='number']")) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.min);
    const max = parseFloat(input.max);
    if (Number.isNaN(value) || value < min || value > max) {
      invalid.push(`${input.name} (must be ${min}–${max})`);
    }
  }
  if (invalid.length) {
    resultBox.classList.remove("hidden");
    resultBox.innerHTML = `<p class="error">Out of range: ${invalid.join(", ")}</p>`;
    return;
  }

  const data = Object.fromEntries(new FormData(form).entries());

  resultBox.classList.remove("hidden");
  resultBox.innerHTML = "<p>Predicting...</p>";

  try {
    const res = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const json = await res.json();

    if (!res.ok) {
      resultBox.innerHTML = `<p class="error">${json.error}</p>`;
      return;
    }

    const list = json.top_3_recommendations
      .map((r) => `<li>${r.career} — ${r.confidence}%</li>`)
      .join("");

    const warning = json.low_confidence
      ? `<p class="warn">${json.message}</p>`
      : "";

    resultBox.innerHTML = `
      ${warning}
      <h2>Recommended: ${json.predicted_career}</h2>
      <p>Confidence: ${json.confidence}%</p>
      <h3>Top 3</h3>
      <ul>${list}</ul>
    `;
  } catch (err) {
    resultBox.innerHTML = `<p class="error">Request failed: ${err}</p>`;
  }
});
