// Auto-dismiss alert messages after 3 seconds
setTimeout(function () {
  document.querySelectorAll(".alert").forEach(function (alert) {
    alert.style.transition = "opacity 0.5s ease";
    alert.style.opacity = "0";
    setTimeout(function () {
      alert.remove();
    }, 500);
  });
}, 3000);
