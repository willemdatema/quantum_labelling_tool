// Used for asking before exiting web
let shouldWarnOnLeave = false;
let madeChanges = false;

function enableLeaveWarning() {
    shouldWarnOnLeave = true;
}

window.addEventListener("beforeunload", function (event) {
    if (shouldWarnOnLeave && madeChanges) {
        shouldWarnOnLeave = false;
        const message = "Are you sure you want to leave this page? Unsaved changes may be lost.";
        event.returnValue = message;  // Necessary for displaying the prompt in some browsers
        return message;               // For older browsers
    }
});

function validateAndHighlightFieldsByIds(elementIds, changeMadeFromButton=false) {
    madeChanges = false;

  // Loop through each container ID in the array
  elementIds.forEach(containerId => {
    // Get the container element by its ID
    const container = document.getElementById('collapseCategory' + containerId);

    // Check if the container exists
    if (!container) {
      console.error(`Element with ID "${containerId}" does not exist.`);
      return;
    }

    // Get all input and select elements inside the container
    const elements = container.querySelectorAll('input, select');
    let allFilled = true;

    // Loop through the elements to check if they are filled
    elements.forEach(element => {
      // If the input type is 'checkbox' or 'radio', check if it's checked
      if (element.type === 'checkbox' || element.type === 'radio') {
        if (!element.checked) {
          allFilled = false;
        }
      }
      // For other types of inputs and selects, check if the value is not empty
      else if (element.value === '-' || element.value === null || element.value === '') {
        allFilled = false;
      }
    });

    const button = document.getElementById('button' + containerId);

    // Apply the class based on whether all fields are filled
    if (allFilled) {
      button.classList.remove('bg-warning-subtle');
      button.classList.add('bg-success-subtle');
    } else {
      button.classList.remove('bg-success-subtle');
      button.classList.add('bg-warning-subtle');
    }
  });

  // Update progress bar
    updateProgressBar();

    madeChanges = changeMadeFromButton;
}

function updateProgressBar(){
  // Update progress bar
  let assessmentForm = document.getElementById('assessment');

  let inputs = assessmentForm.querySelectorAll('select');

  let filledCount = 0; // Counter for filled elements
  let total = 0;
  inputs.forEach(element => {
      // Check if the element is filled
      if (element.value && element.value.trim() !== '' && element.value.trim() !== '-') {
          filledCount++;
     }
     total++;
  });

  let progressBar = document.getElementById('progress');
  progressBar.style.width = ((filledCount / total) * 100) +  "%";
  progressBar.innerHTML = ((filledCount / total) * 100).toFixed(0) +  "%";
}

function toggleVisibility(buttonId, elementId) {
    const button = document.getElementById(buttonId);
    const element = document.getElementById(elementId);

    // Toggle the hidden attribute
    if (element.hasAttribute('hidden')) {
        element.removeAttribute('hidden'); // Show the element
        button.textContent = '-'; // Change button text to -
    } else {
        element.setAttribute('hidden', 'true'); // Hide the element
        button.textContent = '+'; // Change button text to +
    }
}

function expandAllAccordions() {
  // Select all elements with class 'collapse' inside accordions
  const accordions = document.querySelectorAll('.accordion-collapse');

  accordions.forEach(accordion => {
    // Add the 'show' class to each accordion element to expand it
    accordion.classList.add('show');
  });
}

function collapseAllAccordions() {
  // Select all elements with class 'collapse' inside accordions
  const accordions = document.querySelectorAll('.accordion-collapse');

  accordions.forEach(accordion => {
    // Remove the 'show' class from each accordion element to collapse it
    accordion.classList.remove('show');
  });
}

// Function to update the remaining characters
function updateCharacterCount(fieldId, countId, maxLength) {
    const field = document.getElementById(fieldId);
    const counter = document.getElementById(countId);
    field.addEventListener('input', function() {
        const remaining = maxLength - field.value.length;
        counter.textContent = remaining + ' characters left';
    });
}

document.addEventListener("DOMContentLoaded", function (event) {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl));
});