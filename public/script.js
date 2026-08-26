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

// --- Career information ----------------------------------------------------
const careerDetails = {
  "Accountant": {
    description:
      "Accountants manage financial records, prepare financial statements, analyze financial information, and help individuals and organizations make informed financial decisions.",
    why:
      "This career is well suited to people who enjoy working with numbers, analyzing information, maintaining accuracy, and solving structured problems.",
    skills: [
      "Numerical reasoning",
      "Financial analysis",
      "Attention to detail",
      "Organization",
      "Problem solving",
      "Communication"
    ],
    workAreas: [
      "Accounting firms",
      "Banks and financial institutions",
      "Government organizations",
      "Private companies",
      "Consulting firms"
    ],
    careerPath:
      "Accounting Assistant → Accountant → Senior Accountant → Financial Controller → Finance Manager",
    nextSteps: [
      "Develop strong accounting and mathematics skills.",
      "Learn accounting software and spreadsheet tools.",
      "Study financial reporting and taxation.",
      "Gain practical experience through internships or projects.",
      "Consider professional accounting certifications."
    ]
  },

  "Architect": {
    description:
      "Architects design buildings and spaces while balancing creativity, functionality, safety, and environmental considerations.",
    why:
      "This career is suitable for people who combine creativity with technical thinking and enjoy designing practical solutions to complex problems.",
    skills: [
      "Creative thinking",
      "Technical drawing",
      "Spatial reasoning",
      "Problem solving",
      "Project management",
      "Communication"
    ],
    workAreas: [
      "Architecture firms",
      "Construction companies",
      "Real estate organizations",
      "Government agencies",
      "Independent practice"
    ],
    careerPath:
      "Architecture Student → Graduate Architect → Architect → Senior Architect → Principal Architect",
    nextSteps: [
      "Develop drawing and design skills.",
      "Learn computer-aided design software.",
      "Study architecture and construction principles.",
      "Build a portfolio of design projects.",
      "Gain experience through internships."
    ]
  },

  "Business Manager": {
    description:
      "Business managers oversee operations, coordinate teams, manage resources, and help organizations achieve their strategic and financial objectives.",
    why:
      "This career suits people who enjoy leadership, organization, decision-making, communication, and solving business problems.",
    skills: [
      "Leadership",
      "Decision making",
      "Communication",
      "Strategic thinking",
      "Financial awareness",
      "Team management"
    ],
    workAreas: [
      "Private companies",
      "Banks",
      "Retail organizations",
      "Consulting firms",
      "Startups"
    ],
    careerPath:
      "Business Assistant → Business Manager → Senior Manager → Operations Manager → Executive",
    nextSteps: [
      "Develop leadership and communication skills.",
      "Learn business fundamentals.",
      "Study project and financial management.",
      "Gain experience managing teams or projects.",
      "Develop strong decision-making skills."
    ]
  },

  "Cybersecurity Analyst": {
    description:
      "Cybersecurity analysts protect computer systems, networks, and data from cyber threats by identifying vulnerabilities, monitoring systems, and responding to security incidents.",
    why:
      "This career is particularly suitable for people who enjoy technology, analytical thinking, investigation, and solving complex problems.",
    skills: [
      "Cybersecurity fundamentals",
      "Problem solving",
      "Network security",
      "Threat analysis",
      "Critical thinking",
      "Attention to detail"
    ],
    workAreas: [
      "Technology companies",
      "Banks",
      "Government agencies",
      "Telecommunications companies",
      "Cybersecurity firms"
    ],
    careerPath:
      "IT Support → Security Analyst → Cybersecurity Engineer → Security Architect → Security Manager",
    nextSteps: [
      "Learn networking and operating systems.",
      "Study cybersecurity fundamentals.",
      "Practice using security tools and labs.",
      "Learn about common cyber threats and vulnerabilities.",
      "Consider cybersecurity certifications."
    ]
  },

  "Data Scientist": {
    description:
      "Data scientists use statistics, programming, machine learning, and data analysis to discover patterns and produce insights that support decision-making.",
    why:
      "This career suits people who enjoy mathematics, programming, analytical thinking, experimentation, and discovering patterns in information.",
    skills: [
      "Statistics",
      "Programming",
      "Machine learning",
      "Data analysis",
      "Critical thinking",
      "Problem solving"
    ],
    workAreas: [
      "Technology companies",
      "Banks",
      "Research organizations",
      "Healthcare",
      "Consulting firms"
    ],
    careerPath:
      "Data Analyst → Data Scientist → Senior Data Scientist → Machine Learning Engineer → Data Science Lead",
    nextSteps: [
      "Learn Python or R.",
      "Study statistics and mathematics.",
      "Learn SQL and data analysis.",
      "Build machine-learning projects.",
      "Create a portfolio of data projects."
    ]
  },

  "Entrepreneur": {
    description:
      "Entrepreneurs identify opportunities, develop business ideas, build products or services, and take responsibility for growing and managing a business.",
    why:
      "This career is suitable for people who enjoy innovation, leadership, independence, decision-making, and creating solutions to real-world problems.",
    skills: [
      "Leadership",
      "Creativity",
      "Communication",
      "Risk assessment",
      "Problem solving",
      "Business planning"
    ],
    workAreas: [
      "Startups",
      "Small businesses",
      "Technology ventures",
      "Consulting",
      "Independent businesses"
    ],
    careerPath:
      "Idea → Startup Founder → Business Owner → Growing Enterprise → Business Leader",
    nextSteps: [
      "Learn basic business and financial management.",
      "Identify real-world problems that need solutions.",
      "Develop and test business ideas.",
      "Learn marketing and customer research.",
      "Build practical entrepreneurial experience."
    ]
  },

  "Graphic Designer": {
    description:
      "Graphic designers create visual content for brands, products, publications, websites, social media, and other forms of communication.",
    why:
      "This career suits people with strong creativity, visual thinking, attention to detail, and an interest in communicating ideas through design.",
    skills: [
      "Visual creativity",
      "Typography",
      "Digital design",
      "Communication",
      "Branding",
      "Attention to detail"
    ],
    workAreas: [
      "Design agencies",
      "Advertising companies",
      "Media organizations",
      "Technology companies",
      "Freelance work"
    ],
    careerPath:
      "Junior Designer → Graphic Designer → Senior Designer → Art Director → Creative Director",
    nextSteps: [
      "Learn professional design software.",
      "Study typography, layout, and color theory.",
      "Create a portfolio of original work.",
      "Practice designing for different audiences.",
      "Gain experience through freelance or internship projects."
    ]
  },

  "Journalist / Media": {
    description:
      "Journalists and media professionals research, investigate, write, edit, and communicate information to the public through print, television, radio, and digital platforms.",
    why:
      "This career is suited to people who enjoy communication, research, storytelling, critical thinking, and staying informed about current events.",
    skills: [
      "Writing",
      "Communication",
      "Research",
      "Critical thinking",
      "Interviewing",
      "Storytelling"
    ],
    workAreas: [
      "News organizations",
      "Television and radio",
      "Digital media",
      "Publishing",
      "Public relations"
    ],
    careerPath:
      "Reporter → Journalist → Senior Journalist → Editor → Media Director",
    nextSteps: [
      "Develop strong writing skills.",
      "Practice researching and verifying information.",
      "Create articles, videos, or other media projects.",
      "Learn digital journalism tools.",
      "Build a professional portfolio."
    ]
  },

  "Lawyer": {
    description:
      "Lawyers provide legal advice, interpret laws, represent clients, prepare legal documents, and help resolve disputes.",
    why:
      "This career suits people who enjoy reasoning, communication, research, argumentation, and analyzing complex situations.",
    skills: [
      "Critical thinking",
      "Research",
      "Communication",
      "Logical reasoning",
      "Negotiation",
      "Attention to detail"
    ],
    workAreas: [
      "Law firms",
      "Courts",
      "Government",
      "Corporate organizations",
      "Non-governmental organizations"
    ],
    careerPath:
      "Law Student → Graduate/Associate → Lawyer → Senior Counsel → Partner/Legal Director",
    nextSteps: [
      "Develop strong reading and writing skills.",
      "Study legal principles and reasoning.",
      "Practice structured argumentation.",
      "Develop research skills.",
      "Gain practical legal experience."
    ]
  },

  "Mechanical Engineer": {
    description:
      "Mechanical engineers design, develop, test, and improve machines, mechanical systems, equipment, and industrial processes.",
    why:
      "This career suits people who enjoy mathematics, physics, technical problem-solving, design, and understanding how machines work.",
    skills: [
      "Mathematics",
      "Engineering design",
      "Problem solving",
      "Physics",
      "Technical drawing",
      "Computer-aided design"
    ],
    workAreas: [
      "Manufacturing",
      "Automotive companies",
      "Energy companies",
      "Engineering firms",
      "Industrial organizations"
    ],
    careerPath:
      "Engineering Graduate → Mechanical Engineer → Senior Engineer → Engineering Manager → Engineering Director",
    nextSteps: [
      "Strengthen mathematics and physics.",
      "Learn computer-aided design tools.",
      "Work on practical engineering projects.",
      "Develop technical problem-solving skills.",
      "Gain industrial experience."
    ]
  },

  "Medical Doctor": {
    description:
      "Medical doctors diagnose illnesses, treat patients, provide preventive care, and help people maintain and improve their health.",
    why:
      "This career is suited to people who combine scientific thinking with empathy, communication, responsibility, and a desire to help others.",
    skills: [
      "Scientific reasoning",
      "Communication",
      "Empathy",
      "Decision making",
      "Problem solving",
      "Attention to detail"
    ],
    workAreas: [
      "Hospitals",
      "Clinics",
      "Medical centers",
      "Research institutions",
      "Public health organizations"
    ],
    careerPath:
      "Medical Student → Doctor → Resident → Specialist → Consultant",
    nextSteps: [
      "Develop strong biology and chemistry foundations.",
      "Learn about human anatomy and physiology.",
      "Develop communication and interpersonal skills.",
      "Prepare for medical education and professional training.",
      "Seek relevant healthcare experience."
    ]
  },

  "Pharmacist": {
    description:
      "Pharmacists specialize in medicines, helping ensure that medications are used safely and effectively while advising patients and healthcare professionals.",
    why:
      "This career suits people who enjoy science, healthcare, accuracy, communication, and helping others.",
    skills: [
      "Chemistry",
      "Biology",
      "Attention to detail",
      "Communication",
      "Scientific reasoning",
      "Patient care"
    ],
    workAreas: [
      "Hospitals",
      "Community pharmacies",
      "Pharmaceutical companies",
      "Research organizations",
      "Healthcare institutions"
    ],
    careerPath:
      "Pharmacy Student → Pharmacist → Senior Pharmacist → Specialist Pharmacist → Pharmacy Manager",
    nextSteps: [
      "Build a strong foundation in chemistry and biology.",
      "Study pharmacology and pharmaceutical sciences.",
      "Develop accurate record-keeping skills.",
      "Gain practical pharmacy experience.",
      "Keep up with developments in medicines and healthcare."
    ]
  },

  "Public Administrator": {
    description:
      "Public administrators help manage government programs, public services, policies, and resources to meet the needs of communities and citizens.",
    why:
      "This career suits people interested in leadership, organization, public service, policy, communication, and solving community problems.",
    skills: [
      "Leadership",
      "Organization",
      "Policy analysis",
      "Communication",
      "Decision making",
      "Project management"
    ],
    workAreas: [
      "Government ministries",
      "Local government",
      "Public agencies",
      "International organizations",
      "Non-governmental organizations"
    ],
    careerPath:
      "Administrative Officer → Public Administrator → Senior Administrator → Director → Public Service Executive",
    nextSteps: [
      "Learn about government and public policy.",
      "Develop strong organizational skills.",
      "Study project and resource management.",
      "Develop communication and leadership abilities.",
      "Gain experience through public-service projects."
    ]
  },

  "Software Engineer": {
    description:
      "Software engineers design, develop, test, deploy, and maintain software systems that solve problems and provide useful services to individuals and organizations.",
    why:
      "This career is particularly suitable for people who enjoy technology, logical thinking, problem-solving, creativity, and building practical solutions.",
    skills: [
      "Programming",
      "Problem solving",
      "Logical reasoning",
      "Software design",
      "Database management",
      "Teamwork"
    ],
    workAreas: [
      "Technology companies",
      "Banks",
      "Telecommunications",
      "Government",
      "Startups",
      "Freelance and remote work"
    ],
    careerPath:
      "Junior Developer → Software Engineer → Senior Software Engineer → Software Architect → Engineering Manager",
    nextSteps: [
      "Learn a programming language such as Python or JavaScript.",
      "Build practical software projects.",
      "Learn Git and version control.",
      "Study databases and software development practices.",
      "Create a professional project portfolio."
    ]
  },

  "Teacher / Educator": {
    description:
      "Teachers and educators help students develop knowledge, skills, confidence, and understanding through structured learning and guidance.",
    why:
      "This career suits people who enjoy communication, helping others learn, patience, organization, and sharing knowledge.",
    skills: [
      "Communication",
      "Patience",
      "Leadership",
      "Organization",
      "Presentation",
      "Empathy"
    ],
    workAreas: [
      "Primary schools",
      "Secondary schools",
      "Universities",
      "Training organizations",
      "Online education"
    ],
    careerPath:
      "Teacher → Senior Teacher → Head of Department → School Administrator → Education Leader",
    nextSteps: [
      "Develop strong communication and presentation skills.",
      "Study effective teaching methods.",
      "Gain experience explaining concepts to others.",
      "Develop lesson-planning and organizational skills.",
      "Explore educational technology and modern teaching methods."
    ]
  }
};

// --- Prediction form -------------------------------------------------------
const form = document.getElementById("predict-form");
const resultBox = document.getElementById("result");
const retakeBtn = document.getElementById("retake-btn");

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
    resultBox.innerHTML =
      `<p class="error">Out of range: ${invalid.join(", ")}</p>`;
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

    const career = careerDetails[json.predicted_career];

    if (!career) {
      resultBox.innerHTML = `
        ${warning}
        <h2>Recommended: ${json.predicted_career}</h2>
        <p>Confidence: ${json.confidence}%</p>
        <h3>Top 3</h3>
        <ul>${list}</ul>
      `;
    } else {
      resultBox.innerHTML = `
        ${warning}
    
        <div class="career-header">
          <p class="result-label">YOUR CAREER RECOMMENDATION</p>
          <h2>${json.predicted_career}</h2>
          <div class="confidence">
            <strong>${json.confidence}%</strong>
            <span>Confidence</span>
          </div>
        </div>
    
        <div class="career-section">
          <h3>About This Career</h3>
          <p>${career.description}</p>
        </div>
    
        <div class="career-section">
          <h3>Why This Career?</h3>
          <p>${career.why}</p>
        </div>
    
        <div class="career-section">
          <h3>Key Skills</h3>
          <ul class="career-list">
            ${career.skills.map(skill => `<li>${skill}</li>`).join("")}
          </ul>
        </div>
    
        <div class="career-section">
          <h3>Typical Work Areas</h3>
          <ul class="career-list">
            ${career.workAreas.map(area => `<li>${area}</li>`).join("")}
          </ul>
        </div>
    
        <div class="career-section">
          <h3>Possible Career Path</h3>
          <p class="career-path">${career.careerPath}</p>
        </div>
    
        <div class="career-section">
          <h3>Recommended Next Steps</h3>
          <ol class="career-list">
            ${career.nextSteps.map(step => `<li>${step}</li>`).join("")}
          </ol>
        </div>
    
        <div class="career-section alternatives">
          <h3>Other Careers You May Like</h3>
          <ul class="career-list">
            ${list}
          </ul>
        </div>
      `;
    }

    // Show the Retake button after a successful prediction
    retakeBtn.classList.remove("hidden");

  } catch (err) {
    resultBox.innerHTML =
      `<p class="error">Request failed: ${err}</p>`;
  }
});


// --- Retake Assessment ----------------------------------------------------
if (retakeBtn) {
  retakeBtn.addEventListener("click", () => {

    // Clear all answers
    form.reset();

    // Clear the previous recommendation
    resultBox.innerHTML = "";
    resultBox.classList.add("hidden");

    // Hide the Retake button until another prediction is made
    retakeBtn.classList.add("hidden");

    // Return the user to the top of the assessment
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });

    // Put the cursor in the first question
    const firstInput = form.querySelector("input");

    if (firstInput) {
      setTimeout(() => firstInput.focus(), 400);
    }
  });
}

// --- Logout ---------------------------------------------------------------
const logoutBtn = document.getElementById("logout-btn");
if (logoutBtn) {
  logoutBtn.addEventListener("click", async () => {
    try {
      await fetch("/api/logout", { method: "POST" });
    } finally {
      window.location.href = "/";
    }
  });
}
