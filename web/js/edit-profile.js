let modal = document.getElementById("profile-modal");
let modal_button = document.getElementById("edit-profile");

// Open modal on click
modal_button.onclick = function() {
  modal.style.display = "block";
}

// Close modal when clicked everywhere else
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}