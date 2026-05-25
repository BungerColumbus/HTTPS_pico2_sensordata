const header = document.getElementById("header-global");

window.addEventListener("scroll", function () {
  header.dataset.sticky = window.scrollY > 0;
});
