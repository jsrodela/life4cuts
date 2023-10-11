function addNumberToInput(value) {
  const inputElement = document.getElementById("people");
  inputElement.value = value;
}

const numButtons = document.querySelectorAll(".num_btn");
numButtons.forEach(button => {
  const value = button.getAttribute("value");
  button.addEventListener("click", () => {
      addNumberToInput(value);
  });
});