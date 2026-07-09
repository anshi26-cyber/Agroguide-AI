function showTab(tabId, btn) {

    // hide all tabs
    document.getElementById("profileTab").classList.add("hidden");
    document.getElementById("editTab").classList.add("hidden");
    document.getElementById("historyTab").classList.add("hidden");

    // show selected tab
    document.getElementById(tabId).classList.remove("hidden");

    // remove active class
    document.querySelectorAll(".tab-btn").forEach(el => {
        el.classList.remove("bg-green-500/30");
    });

    // add active class
    btn.classList.add("bg-green-500/30");
}

// default open first tab
document.addEventListener("DOMContentLoaded", () => {
    const firstTab = document.querySelector(".tab-btn");
    if (firstTab) firstTab.click();
});