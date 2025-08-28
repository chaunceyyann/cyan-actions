javascript:(function() {
  // Select all radio buttons
  const radios = document.querySelectorAll('input[type="radio"]');
  radios.forEach(radio => {
    // Create a new checkbox element
    const checkbox = document.createElement('input');
    // Copy relevant attributes
    checkbox.type = 'checkbox';
    checkbox.name = radio.name + (radio.name ? '[]' : ''); // Append [] for multi-select
    checkbox.value = radio.value;
    checkbox.id = radio.id;
    checkbox.checked = radio.checked;
    if (radio.className) checkbox.className = radio.className;
    if (radio.disabled) checkbox.disabled = true;

    // Replace the radio with the checkbox
    radio.parentNode.replaceChild(checkbox, radio);

    // Update associated labels (if any)
    const label = document.querySelector(`label[for="${radio.id}"]`);
    if (label) label.setAttribute('for', checkbox.id);
  });
  alert('Radio buttons converted to checkboxes!');
})();
