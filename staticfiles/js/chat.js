document.addEventListener('DOMContentLoaded', () => {

  function prettyDate(timestamp) {
    var now = new Date();
    var nowDay = new Date(now.getFullYear(), now.getMonth(), now.getDate()); // get current date without time
    var date = new Date(timestamp * 1000);
    var dateDay = new Date(date.getFullYear(), date.getMonth(), date.getDate()); // get message date without time
    var diff = Math.floor((nowDay - dateDay) / (1000 * 60 * 60 * 24)); // difference in days

    var day = date.getDate();
    var month = date.getMonth() + 1; // JavaScript months are 0-11
    var year = date.getFullYear();
    var hour = ("0" + date.getHours()).slice(-2); // add leading zero if needed
    var minute = ("0" + date.getMinutes()).slice(-2); // add leading zero if needed
    var period = hour >= 12 ? 'PM' : 'AM';

    hour = hour % 12;
    hour = hour ? hour : 12; // the hour '0' should be '12'
    hour = ("0" + hour).slice(-2);  // add leading zero if needed

    if (diff === 0) {
      return "Today at " + hour + ":" + minute + " " + period;
    } else if (diff === 1) {
      return "Yesterday at " + hour + ":" + minute + " " + period;
    } else {
      return day + "/" + month + "/" + year + " at " + hour + ":" + minute + " " + period;
    }
  }


  // Convert Unix timestamp to readable format in user's local timezone
  document.querySelectorAll(".timestamp").forEach(function (el) {
    var timestamp = el.getAttribute("data-timestamp");
    el.innerText = prettyDate(timestamp);
  });

})
  
  
  const dropdownMenu = document.querySelector(".dropdown-menu");
  const dropdownButton = document.querySelector(".dropdown-button");
  
  if (dropdownButton) {
    dropdownButton.addEventListener("click", () => {
      dropdownMenu.classList.toggle("show");
    });
  }
  
  // Upload Image
  const photoInput = document.querySelector("#avatar");
  const photoPreview = document.querySelector("#preview-avatar");
  if (photoInput)
  photoInput.onchange = () => {
  const [file] = photoInput.files;
  if (file) {
    photoPreview.src = URL.createObjectURL(file);
}
};
