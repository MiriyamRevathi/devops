/**
 * DevOpsFlow Client-side Interaction JavaScript Module
 */
document.addEventListener("DOMContentLoaded", function() {
    console.log("DevOpsFlow Control Center Initialized.");

    // Highlight current active menu link
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll(".sidebar-menu .menu-item");
    
    menuLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href && currentPath === href) {
            link.classList.add("active");
        }
    });

    // Auto-scroll terminal log viewers to bottom
    const logViewers = document.querySelectorAll(".terminal-log-viewer");
    logViewers.forEach(viewer => {
        viewer.scrollTop = viewer.scrollHeight;
    });
});
