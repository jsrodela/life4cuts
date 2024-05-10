function addNumberToInput(value) {
  const inputElement = document.getElementById("people");
  inputElement.value = value;
}

function enablestartbtn(){
  const buttonstatus = document.getElementById("start");
  buttonstatus.disabled = false;
}

function disablestartbtn(){
  const buttonstatus = document.getElementById("start");
  buttonstatus.disabled = true;
}

const numButtons = document.querySelectorAll(".num_btn");
numButtons.forEach(button => {
  const value = button.getAttribute("value");
  button.addEventListener("click", () => {
      addNumberToInput(value);
  });
});