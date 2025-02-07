// static/js/modules/releases-add.js
import { ApiService } from '../common/api-service.js';
import { UiManager } from '../common/ui-manager.js';
import { Utils, translations } from '../common/utils.js';

export default class ReleasesAdd {
    constructor() {
        this.urlButton = document.querySelector('#urlButton');
        this.filenameIndex = document.querySelector('#filenameIndex');
        this.filenameIndexGroup = document.querySelector('#filenameIndexGroup');
        this.cutButton = document.querySelector('#cutButton');
        this.releaseTitle = document.querySelector('#releaseTitle');
        this.submitButton = document.querySelector('#submitButton');
        this.releaseForm = document.querySelector('#releaseForm');
    }

    init() {
        this.addEventListeners();
    }

    addEventListeners() {
        this.urlButton.addEventListener('click', () => this.toggleFilenameIndex());
        this.filenameIndex.addEventListener('input', () => this.extractNumbers());
        this.cutButton.addEventListener('click', () => this.cutTextTillSeparator());
        this.releaseForm.addEventListener('submit', async (e) => this.handleFormSubmit(e));
    }

    toggleFilenameIndex() {
        this.filenameIndexGroup.classList.toggle("d-none");
    }

    extractNumbers() {
        const input = this.filenameIndex.value;
        const numbers = input.split('')
            .map(ch => (ch >= '0' && ch <= '9') ? ch : ' ')
            .join('')
            .trim()
            .split(/\s+/);

        const resultList = document.querySelector('#numberList');
        resultList.innerHTML = '';

        if (numbers.join('').length === 0) {
            resultList.style.display = 'none';
            return;
        }

        numbers.forEach((number, index) => {
            if (number !== '') {
                const item = document.createElement('div');
                item.className = 'list-group-item';
                item.textContent = `${translations.labels.releaseAddIndex}: ${index + 1}, ${translations.labels.releaseAddNumber}: ${number}`;
                item.addEventListener('click', () => {
                    document.querySelector('#index').value = index + 1;
                    resultList.style.display = 'none';
                });
                resultList.appendChild(item);
            }
        });

        resultList.style.display = 'block';
    }

    cutTextTillSeparator() {
        let text = this.releaseTitle.value;
        
        // Get text after the first "/" or "|" separator
        const delimiterIndex = text.search(/[\/|]/);
        if (delimiterIndex !== -1) {
            text = text.substring(delimiterIndex + 1).trim();
        }

        // Remove text after year pattern and clean up
        text = text
            .replace(/\s*[\(\[]?\d{4}[\)\]]?.*$/, '')
            .replace(/\(.*?\)/g, '')
            .replace(/\[.*?\]/g, '')
            .replace(/[\/\\:*?"<>|]/g, '')
            .replace(/\s+/g, ' ')
            .trim();

        this.releaseTitle.value = text;
    }

    async handleFormSubmit(e) {
        e.preventDefault();
        
        try {
            UiManager.setButtonLoading(this.submitButton);
            
            const formData = new FormData(this.releaseForm);
            const result = await ApiService.post('/api/releases', formData);

            // Show operation results
            UiManager.showOperationResults(result);
            
            // Close modal and refresh table
            UiManager.hideModal('addReleaseModal');
            if (window.releasesTable) {
                window.releasesTable.ajax.reload();
            }

        } catch (error) {
            console.error('Error submitting form:', error);
        } finally {
            UiManager.resetButton(this.submitButton, translations.buttons.releaseAddSubmit);
        }
    }
}