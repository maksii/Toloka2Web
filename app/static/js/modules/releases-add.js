// static/js/modules/releases-add.js
import { Utils } from '../common/utils.js';
import translations from '../l18n/en.js';
import { DataTableManager } from '../common/datatable.js';

export default class ReleasesAdd {
    init() {
        this.addEventListeners();
    }

    urlButton = document.querySelector('#urlButton');
    filenameIndex = document.querySelector('#filenameIndex');
    filenameIndexGroup = document.querySelector('#filenameIndexGroup');
    cutButton = document.querySelector('#cutButton');
    releaseTitle = document.querySelector('#releaseTitle');
    submitButton = document.querySelector('#submitButton');
    releaseForm = document.querySelector('#releaseForm');  

    addEventListeners() {
        this.urlButton.addEventListener('click', () => { this.filenameIndexGroup.classList.toggle("d-none"); });
        this.filenameIndex.addEventListener('input', () => this.extractNumbers());
        this.cutButton.addEventListener('click', () => this.cutTextTillSeparator());
        this.releaseForm.addEventListener('submit', async (e) => { await this.submitAddNewTitleForm(e) });
    }

    handleTableClick(event) {
        let target = event.target;
        while (target && !target.classList.contains('action-update')) {
            if (target === event.currentTarget) return;
            target = target.parentNode;
        }
        if (target && target.classList.contains('action-update')) {
            this.updateRelease(target);
        }
    }

    extractNumbers() {
        const input = this.filenameIndex.value;
        const numbers = input.split('').map((ch) => (ch >= '0' && ch <= '9') ? ch : ' ').join('').trim().split(/\s+/);
        const resultList = document.querySelector('#numberList');
        resultList.innerHTML = '';
    
        numbers.forEach((number, index) => {
            if (number !== '') {
                const item = document.createElement('div');
                item.className = 'list-group-item';
                item.textContent = `${translations.labels.releaseAddIndex}: ${index+1}, ${translations.labels.releaseAddNumber}: ${number}`;
                item.addEventListener('click', () => {
                    document.querySelector('#index').value = index + 1;
                    resultList.style.display = 'none';
                });
                resultList.appendChild(item);
            }
        });
    
        resultList.style.display = numbers.join('').length === 0 ? 'none' : 'block';
    }

    cutTextTillSeparator()
    {
        let text = this.releaseTitle.value;
        
        // Get text after the first "/" or "|" separator
        const delimiterIndex = text.search(/[\/|]/);
        if (delimiterIndex !== -1) {
            text = text.substring(delimiterIndex + 1).trim();
        }

        // Remove text after year pattern (e.g., "(2022)" or "2022")
        text = text.replace(/\s*[\(\[]?\d{4}[\)\]]?.*$/, '');

        // Remove unsafe characters and clean up the text
        text = text
            // Remove any remaining parentheses and their contents
            .replace(/\(.*?\)/g, '')
            .replace(/\[.*?\]/g, '')
            // Remove unsafe characters for file systems
            .replace(/[\/\\:*?"<>|]/g, '')
            // Remove multiple spaces
            .replace(/\s+/g, ' ')
            // Trim spaces from start and end
            .trim();

        this.releaseTitle.value = text;
    }

    async submitAddNewTitleForm(e) {
        e.preventDefault();
        
        // Disable submit button and show spinner
        this.submitButton.disabled = true;
        this.submitButton.innerHTML = Utils.renderButtonSpinner();
        
        try {
            const formData = new FormData(this.releaseForm);
            const response = await fetch('/api/releases', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();

            // Get references to modal and offcanvas
            const addReleaseModal = bootstrap.Modal.getInstance(document.querySelector('#addReleaseModal'));
            const offcanvasElement = document.getElementById('offcanvasOperationResults');
            
            // First prepare the offcanvas content
            Utils.generateOperationResponseOffCanvas(result);
            const bsOperationOffcanvas = new bootstrap.Offcanvas(offcanvasElement);

            // Create a promise that resolves when the offcanvas is shown
            const offcanvasShown = new Promise(resolve => {
                offcanvasElement.addEventListener('shown.bs.offcanvas', () => {
                    // Only after offcanvas is shown, hide the modal
                    addReleaseModal.hide();
                    // Then refresh the table
                    if (window.releasesTable) {
                        DataTableManager.refreshTable(window.releasesTable);
                    }
                    resolve();
                }, { once: true });
            });

            // Show the offcanvas and wait for it to complete showing
            bsOperationOffcanvas.show();
            await offcanvasShown;

        } catch (error) {
            console.error('Error submitting form:', error);
        } finally {
            // Reset button state
            this.submitButton.innerHTML = translations.buttons.releaseAddSubmit;
            this.submitButton.disabled = false;
        }
    }

}