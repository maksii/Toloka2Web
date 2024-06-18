const repo = 'maksii/Toloka2Web'; // Change this to your repository

function checkReleaseStatus() {
    const lastCheckedRelease = localStorage.getItem('lastCheckedRelease');
    fetch(`https://api.github.com/repos/${repo}/releases/latest`)
        .then(response => response.json())
        .then(data => {
            const latestRelease = data.tag_name;
            if (lastCheckedRelease !== latestRelease) {
                const formattedContent = formatContent(data.body);
                showReleaseToast(data.name, formattedContent, latestRelease);
            }
        })
        .catch(error => console.error('Error fetching release data:', error));
}

function showReleaseToast(title, content, latestRelease) {
    const toastContainer = document.querySelector('.toast-container');
    const toastHTML = `
        <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="false">
            <div class="toast-header">
                <strong class="me-auto">New Release: ${title}</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${content}
            </div>
        </div>
    `;
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = new bootstrap.Toast(toastContainer.lastElementChild);
    toastElement.show();

    // Add event listener for when the toast is hidden
    toastContainer.lastElementChild.addEventListener('hidden.bs.toast', function () {
        localStorage.setItem('lastCheckedRelease', latestRelease);
    });
}

function formatContent(markdown) {
    // Convert markdown to HTML
    let html = marked.parse(markdown);

    // Modify image sizes
    html = html.replace(/<img /g, '<img style="max-width:100%;height:auto;" ');

    // Sanitize HTML
    return DOMPurify.sanitize(html);
}
checkReleaseStatus();