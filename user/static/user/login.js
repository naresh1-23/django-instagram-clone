document.querySelector(".button").disabled = falses;
function checking() {
  if (
    document.querySelector(".email").value == "" ||
    document.querySelector(".password").value == ""
  ) {
    document.querySelector(".button").disabled = true;
  } else {
    document.querySelector(".button").disabled = false;
    document.querySelector(".button").style.backgroundColor =
      "rgb(0, 162, 255)";
    document.querySelector(".button").style.cursor = "pointer";
  }
}
