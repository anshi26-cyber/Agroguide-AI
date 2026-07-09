window.toggleTheme = function () {
    const html = document.documentElement;
    const btn = document.getElementById("theme-btn");

    html.classList.toggle("dark");

    if (html.classList.contains("dark")) {
        localStorage.setItem("theme", "dark");
        btn.innerHTML = "☀️";
    } else {
        localStorage.setItem("theme", "light");
        btn.innerHTML = "🌙";
    }
};

// Load theme on page load
window.onload = function () {
    const btn = document.getElementById("theme-btn");

    if (localStorage.getItem("theme") === "dark") {
        document.documentElement.classList.add("dark");
        if (btn) btn.innerHTML = "☀️";
    }
};
