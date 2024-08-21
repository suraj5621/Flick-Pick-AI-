function showTooltip() {
  let tooltip = document.getElementById("tooltipe");
  // Apply styles when clicked
  tooltip.style.visibility = "visible";
  tooltip.style.opacity = 2;
  tooltip.style.transform = "translateX(-50%) translateY(-10px)";
}

function hideTooltip() {
  var tooltip = document.getElementById("tooltipe");
  tooltip.style.opacity = 0;
  tooltip.style.visibility = "hidden";
  tooltip.style.transform = "translateX(-50%) translateY(0)";
}

var imgBx = document.getElementById("img-bx");
var mainBx = document.getElementById("mnbxe");

// for mouseover
imgBx.addEventListener("mouseover", function () {
  // Shaking Animation for both elements
  imgBx.style.animation = "shake 697ms ease-in-out forwards";
  mainBx.style.animation = "shake 697ms ease-in-out forwards";
});

// for mouseout
imgBx.addEventListener("mouseout", function () {
  // Remove animation
  imgBx.style.animation = "";
  mainBx.style.animation = "";
});
