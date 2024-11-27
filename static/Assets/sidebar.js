document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleBtn');
    const contentFrame = document.getElementById('contentFrame');
    const navbarLinks = document.querySelectorAll('.navbar a');

    // Set the "Dashboard" option as active by default on load
    const dashboardLink = document.querySelector('.navbar a[data-page="admin_dashboard"]');
    if (dashboardLink) {
        dashboardLink.classList.add('active');
        contentFrame.src = dashboardLink.getAttribute('href');  // Use href which has the full URL
    }

    // Toggle sidebar visibility
    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('collapsed');
    });

    // Handle navigation link clicks
    navbarLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            // Remove 'active' class from all links and add it to the clicked link
            navbarLinks.forEach(link => link.classList.remove('active'));
            this.classList.add('active');

            // Change the iframe source based on the clicked link
            const page = this.getAttribute('href');  // Now using href to navigate to the correct URL
            contentFrame.src = page;
        });
    });

    // Check the current page and highlight the corresponding link after iframe loads
    contentFrame.addEventListener('load', function() {
        // Get the current file name from iframe's location
        const currentSrc = contentFrame.contentWindow.location.pathname.split('/').pop();

        // Loop through all navbar links and update the active class
        navbarLinks.forEach(link => {
            const page = link.getAttribute('href').split('/').pop();  // Extract the last part of the href path
            if (page === currentSrc) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    });
});
