document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.getElementById('toggleBtn');
    const contentFrame = document.getElementById('contentFrame');
    const navbarLinks = document.querySelectorAll('.navbar a');
    const logoutLink = document.querySelector('.navbar a[data-page="logout"]'); // Select logout link

    // Set the "Dashboard" option as active by default
    const dashboardLink = document.querySelector('.navbar a[data-page="admin_dashboard"]');
    if (dashboardLink) {
        dashboardLink.classList.add('active');
        contentFrame.src = dashboardLink.getAttribute('href');
    }

    // Toggle sidebar visibility and adjust the iframe
    toggleBtn.addEventListener('click', function () {
        sidebar.classList.toggle('collapsed');
        adjustIframePosition();
    });

    // Adjust iframe margin based on sidebar state
    function adjustIframePosition() {
        const isCollapsed = sidebar.classList.contains('collapsed');
        const mainContent = document.querySelector('.main-content');
        mainContent.style.marginLeft = isCollapsed ? '70px' : '250px';
    }

    // Handle navigation link clicks
    navbarLinks.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();

            // Remove 'active' class from all links and add it to the clicked link
            navbarLinks.forEach(navLink => navLink.classList.remove('active'));
            this.classList.add('active');

            // Update iframe source
            const page = this.getAttribute('href');
            contentFrame.src = page;
        });
    });

    // Highlight the corresponding link after iframe loads
    contentFrame.addEventListener('load', function () {
        const currentSrc = contentFrame.contentWindow.location.pathname.split('/').pop();

        // Update active class based on the iframe's content
        navbarLinks.forEach(link => {
            const page = link.getAttribute('href').split('/').pop();
            if (page === currentSrc) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    });

    // Logout functionality for the logout link
    if (logoutLink) {
        logoutLink.addEventListener('click', function (event) {
            event.preventDefault();

            // Redirect the entire browser window to the login page
            const logoutUrl = this.getAttribute('href');
            window.top.location.href = logoutUrl;
        });
    }

    // Ensure proper iframe positioning on load
    adjustIframePosition();
});
