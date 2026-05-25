var mapOptions = {
  center: [51.4484, 5.4909],
  zoom: 16,
};

var map = new L.map("map", mapOptions);
var layer = new L.TileLayer(
  "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
);
map.addLayer(layer);

var customIcon = L.icon({
  iconUrl: "/images/pin.svg",
  iconSize: [40, 40],
  iconAnchor: [20, 40],
  popupAnchor: [0, -40],
});

var pins = [
  {
    coords: [51.4484, 5.4909],
    title: "Common ash -- Campus Centre",
    description: "First image you find when you look up the word tree...",
    image: "/images/oak.jpg", // Replace "ash" asset variable with straight path
    imageAlt: "The ash tree in the middle of the campus",
    icon: customIcon,
  },
];

var aside = document.getElementById("map-aside");
var closeBtn = document.getElementById("aside-close");
var asideTitle = document.getElementById("aside-title");
var asideDescription = document.getElementById("aside-description");

pins.forEach(function (pin) {
  L.marker(pin.coords, { icon: pin.icon })
    .addTo(map)
    .on("click", function () {
      const existingImg = aside.querySelector("img");
      if (existingImg) existingImg.remove();

      const img = document.createElement("img");
      img.src = pin.image;
      img.alt = pin.imageAlt;
      img.id = "aside-image";
      aside.prepend(img);

      asideTitle.textContent = pin.title;
      asideDescription.textContent = pin.description;
      aside.classList.add("visible");
      document.getElementById("map-hint").style.display = "none";
    });
});

closeBtn.addEventListener("click", function () {
  aside.classList.remove("visible");
});
