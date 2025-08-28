(function () {
  const form = document.querySelector("form");
  if (!form) {
    alert("No form found!");
    return;
  }

  const boxes = [
    ...document.querySelectorAll(
      'input[type="checkbox"][data-original-type="radio"]:checked'
    ),
  ];
  if (boxes.length === 0) {
    alert("No selections!");
    return;
  }

  let index = 0;
  function submitNext() {
    if (index >= boxes.length) {
      alert("🚀 Submitted all choices into background tabs!");
      return;
    }

    const box = boxes[index];
    index++;

    // Clone the form
    const tempForm = form.cloneNode(true);

    // Keep only this checkbox’s selection
    [...tempForm.querySelectorAll(
      'input[type="checkbox"][data-original-type="radio"]'
    )].forEach((el) => {
      if (el.value !== box.value) {
        el.remove();
      } else {
        const r = document.createElement("input");
        r.type = "radio";
        r.name = el.dataset.originalName;
        r.value = el.value;
        r.checked = true;
        el.parentNode.replaceChild(r, el);
      }
    });

    // Open background tab and auto-submit
    const newWin = window.open("about:blank", "_blank", "noopener,noreferrer");
    const newDoc = newWin.document;
    newDoc.open();
    newDoc.write(
      "<html><body>" +
        tempForm.outerHTML +
        "<script>document.forms[0].submit();<\/script></body></html>"
    );
    newDoc.close();

    // Wait 300ms before next submit
    setTimeout(submitNext, 300);
  }

  submitNext();
})();
