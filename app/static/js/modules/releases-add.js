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
        this.releasePreview = document.querySelector('#releasePreview');
        this.addReleaseModal = document.querySelector('#addReleaseModal');
    }

    init() {
        this.addEventListeners();
        this.setupModalDefaults();
    }

    addEventListeners() {
        this.urlButton.addEventListener('click', () => this.toggleFilenameIndex());
        this.filenameIndex.addEventListener('input', () => this.extractNumbers());
        this.cutButton.addEventListener('click', () => this.cutTextTillSeparator());
        this.releaseForm.addEventListener('submit', async (e) => this.handleFormSubmit(e));
        
        // Add validation on input
        const previewInputs = () => { this.updateReleasePreview(); };
        this.releaseTitle.addEventListener('input', () => { this.validateTitle(); previewInputs(); });
        const seasonEl = document.querySelector('#season');
        const indexEl = document.querySelector('#index');
        if (seasonEl) { seasonEl.addEventListener('input', () => { this.validateNumber('season'); previewInputs(); }); seasonEl.addEventListener('change', previewInputs); }
        if (indexEl) { indexEl.addEventListener('input', () => { this.validateNumber('index'); previewInputs(); }); indexEl.addEventListener('change', previewInputs); }
        document.querySelector('#correction').addEventListener('input', () => this.validateNumber('correction'));
        document.querySelector('#tolokaUrl').addEventListener('input', () => this.validateUrl());
        const releaseGroup = document.querySelector('#releaseGroup');
        const meta = document.querySelector('#meta');
        const ongoing = document.querySelector('#ongoing');
        if (releaseGroup) { releaseGroup.addEventListener('input', previewInputs); releaseGroup.addEventListener('change', previewInputs); }
        if (meta) { meta.addEventListener('input', previewInputs); meta.addEventListener('change', previewInputs); }
        if (ongoing) ongoing.addEventListener('change', previewInputs);
    }

    setupModalDefaults() {
        if (!this.addReleaseModal) return;
        this.addReleaseModal.addEventListener('shown.bs.modal', () => this.loadReleaseDefaults());
    }

    async loadReleaseDefaults() {
        try {
            const result = await ApiService.get('/api/releases/defaults');
            const metaInput = document.querySelector('#meta');
            if (metaInput && result?.default_meta !== undefined && metaInput.value === '') {
                metaInput.value = result.default_meta || '';
            }
            this.updateReleasePreview();
        } catch (err) {
            console.warn('Could not load release defaults:', err);
            this.updateReleasePreview();
        }
    }

    updateReleasePreview() {
        if (!this.releasePreview) return;
        const title = (document.querySelector('#releaseTitle')?.value || '').trim();
        const season = (document.querySelector('#season')?.value || '').trim();
        const metaVal = (document.querySelector('#meta')?.value || '').trim();
        const groupVal = (document.querySelector('#releaseGroup')?.value || '').trim();
        const isOngoing = document.querySelector('#ongoing')?.checked ?? true;
        const indexVal = (document.querySelector('#index')?.value || '1').trim();
        const parts = [];
        if (title) parts.push(title);
        if (season !== '' || title) {
            const s = season !== '' ? season : '1';
            const idx = indexVal ? parseInt(indexVal, 10) : 1;
            if (isOngoing && !isNaN(idx)) {
                parts.push(`S${s.padStart(2, '0')}E01-E${String(idx).padStart(2, '0')}`);
            } else {
                parts.push(`S${s.padStart(2, '0')}`);
            }
        }
        if (metaVal) parts.push(metaVal);
        if (groupVal) parts.push(`[${groupVal}]`);
        this.releasePreview.textContent = parts.length ? parts.join(' ') : '—';
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
        
        // Trigger form validation and preview update after modifying the title
        this.validateTitle();
        this.updateReleasePreview();
    }

    validateTitle() {
        const title = this.releaseTitle.value;
        const invalidChars = /[\/\\:*?"<>|]/;
        const isValid = !invalidChars.test(title);
        
        this.releaseTitle.setCustomValidity(isValid ? '' : translations.validation?.invalidTitle || 'Title contains invalid characters');
        this.releaseTitle.reportValidity();
        return isValid;
    }

    validateNumber(fieldId) {
        const input = document.querySelector(`#${fieldId}`);
        const value = input.value;
        const isValid = /^\d+$/.test(value);
        
        input.setCustomValidity(isValid ? '' : translations.validation?.invalidNumber || 'Please enter a valid number');
        input.reportValidity();
        return isValid;
    }

    validateUrl() {
        const url = document.querySelector('#tolokaUrl').value;
        const isValid = url && url.trim() !== '' && url.startsWith('https://toloka.to/');
        
        document.querySelector('#tolokaUrl').setCustomValidity(
            isValid ? '' : translations.validation?.invalidUrl || 'Please enter a valid Toloka URL'
        );
        document.querySelector('#tolokaUrl').reportValidity();
        return isValid;
    }

    validateForm() {
        return this.validateTitle() && 
               this.validateNumber('season') && 
               this.validateNumber('index') && 
               this.validateNumber('correction') && 
               this.validateUrl();
    }

    async handleFormSubmit(e) {
        // Prevent default form submission immediately
        e.preventDefault();
        e.stopPropagation();
        
        // Force form validation UI to show
        this.releaseForm.classList.add('was-validated');
        
        // Check HTML5 form validity first
        if (!this.releaseForm.checkValidity()) {
            return;
        }
        
        // Then check our custom validation
        if (!this.validateForm()) {
            return;
        }
        
        try {
            UiManager.setButtonLoading(this.submitButton);
            
            const formData = new FormData(this.releaseForm);
            
            // Handle ongoing checkbox - ensure it's sent as a proper boolean value
            const ongoingCheckbox = document.querySelector('#ongoing');
            formData.set('ongoing', ongoingCheckbox.checked ? 'true' : 'false');
            
            const result = await ApiService.post('/api/releases', formData);

            // Check if the operation was successful
            if (result && !result.error) {
                // Show success message
                UiManager.showOperationResults(result);
                
                // Close modal and dispatch event to refresh table
                UiManager.hideModal('addReleaseModal');
                window.dispatchEvent(new CustomEvent('releaseAdded'));
            } else {
                // Show error message but keep modal open
                UiManager.showOperationResults(result || { error: 'Failed to add release' });
            }
        } catch (error) {
            console.error('Error submitting form:', error);
            // Show error message but keep modal open
            UiManager.showOperationResults({ error: error.message || 'Failed to add release' });
        } finally {
            UiManager.resetButton(this.submitButton, translations.buttons.releaseAddSubmit);
        }
    }
}