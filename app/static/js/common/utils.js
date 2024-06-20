// static/js/common/utils.js
export class Utils {
    static async fetchData(url, options = {}) {
        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error('Network response was not ok');
            return await response.json();
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }

    static generateOperationResponseOffCanvas(response) {
        if (!response) return; // Exit if no response data
    
        // Determine alert and badge classes based on the response code
        const alertClass = response.response_code === 'SUCCESS' ? 'alert-success' :
                           response.response_code === 'FAILURE' ? 'alert-danger' : 'alert-warning';
        const badgeClass = response.response_code === 'SUCCESS' ? 'bg-success' :
                           response.response_code === 'FAILURE' ? 'bg-danger' : 'bg-warning';
    
        // Helper function to generate list items for accordion
        function generateListItems(items) {
            return items.map(item => `<li class="list-group-item">${item}</li>`).join('');
        }
    
        // Generate accordion HTML
        function generateAccordion(id, headingText, items) {
            return `
                <div class="accordion mt-3" id="${id}">
                    <div class="accordion-item">
                        <h2 class="accordion-header" id="${id}Heading">
                            <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#${id}Collapse" aria-expanded="false" aria-controls="${id}Collapse">
                                ${headingText}
                            </button>
                        </h2>
                        <div id="${id}Collapse" class="accordion-collapse collapse" aria-labelledby="${id}Heading">
                            <div class="accordion-body">
                                <ul class="list-group">
                                    ${generateListItems(items)}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    
        // Generate the entire card with accordions
        const cardHTML = `
            <div class="card alert ${alertClass}">
                <div class="card-body">
                    <h5 class="card-title">Operation Type: ${response.operation_type.replace('_', ' ').toLowerCase().replace(/\b\w/g, l => l.toUpperCase())}</h5>
                    <p class="card-text">Response Code: <span class="badge ${badgeClass}">${response.response_code}</span></p>
                    <p class="card-text">Start Time: ${response.start_time}</p>
                    <p class="card-text">End Time: ${response.end_time}</p>
                    ${response.titles_references ? generateAccordion('TitlesAccordion', 'Titles References', response.titles_references) : ''}
                    ${response.torrent_references ? generateAccordion('torrentAccordion', 'Torrent References', response.torrent_references) : ''}
                    ${response.operation_logs ? generateAccordion('logsAccordion', 'Operation Logs', response.operation_logs) : ''}
                    <hr>
                    <p class="mb-0">Create an issue on github if something wrong.</p>
                </div>
            </div>
        `;
    
        // Insert the generated HTML into a predefined container in your HTML
        document.getElementById('offcanvasBody').innerHTML = cardHTML;
    }

    static downloadFile(url) {
        const link = document.createElement('a');
        link.href = url;
        link.download = true;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }

    static renderButtonSpinner()
    {
        return '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...';
    }

    static renderActionButton(action, buttonClass, buttonState, buttonIcon, buttonText)
    {
        return `<button class="btn ${buttonClass} ${action}" ${buttonState}><span class="bi ${buttonIcon}" aria-hidden="true"></span><span class="visually-hidden" role="status">${buttonText}</span></button>`;
    }

    static hasParentWithClass(element, tillParent, classname) {
        while (element && element !== tillParent) {
            if (element.classList && element.classList.contains(classname)) {
                return true;
            }
            element = element.parentNode;
        }
        return false;
    }

    static addRelease()
    {
        const addReleaseModal = new bootstrap.Modal(document.querySelector('#addReleaseModal'), {
            keyboard: false
          });
        addReleaseModal.show();
    }

}