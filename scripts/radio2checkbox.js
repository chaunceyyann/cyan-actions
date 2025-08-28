javascript:(function() {
  const toggled = document.body.dataset.radiosToggled === "true";
  
  if (!toggled) {
    // Convert radios → checkboxes
    document.querySelectorAll('input[type="radio"]').forEach(radio => {
      const oldId = radio.id;
      const checkbox = document.createElement('input');
      checkbox.type = 'checkbox';
      checkbox.name = radio.name ? radio.name + '[]' : '';
      checkbox.value = radio.value;
      if (oldId) checkbox.id = oldId;
      checkbox.checked = radio.checked;
      if (radio.className) checkbox.className = radio.className;
      checkbox.disabled = radio.disabled;

      // Store metadata so we can revert later
      checkbox.dataset.originalType = "radio";
      checkbox.dataset.originalName = radio.name;

      radio.parentNode.replaceChild(checkbox, radio);

      if (oldId) {
        const label = document.querySelector(`label[for="${oldId}"]`);
        if (label) label.setAttribute('for', checkbox.id);
      }
    });
    document.body.dataset.radiosToggled = "true";
    console.log("✅ Radios converted to checkboxes.");
  } else {
    // Convert checkboxes (that were radios) back → radios
    document.querySelectorAll('input[type="checkbox"][data-original-type="radio"]').forEach(checkbox => {
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = checkbox.dataset.originalName || '';
      radio.value = checkbox.value;
      if (checkbox.id) radio.id = checkbox.id;
      radio.checked = checkbox.checked;
      if (checkbox.className) radio.className = checkbox.className;
      radio.disabled = checkbox.disabled;

      checkbox.parentNode.replaceChild(radio, checkbox);

      if (radio.id) {
        const label = document.querySelector(`label[for="${radio.id}"]`);
        if (label) label.setAttribute('for', radio.id);
      }
    });
    document.body.dataset.radiosToggled = "false";
    console.log("↩️ Checkboxes reverted to radios.");
  }
})();
