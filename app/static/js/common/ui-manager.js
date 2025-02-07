import { Utils } from './utils.js';
import translations from '../l18n/en.js';

export class UiManager {
    static showToast(title, content, options = {}) {
        const toastContainer = document.querySelector('.toast-container');
        const toastHTML = `
            <div class="toast" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="${options.autohide !== false}">
                <div class="toast-header">
                    <strong class="me-auto">${title}</strong>
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
        return toastElement;
    }

    static showOperationResults(result) {
        const offcanvasElement = document.getElementById('offcanvasOperationResults');
        Utils.generateOperationResponseOffCanvas(result);
        const bsOperationOffcanvas = new bootstrap.Offcanvas(offcanvasElement);
        bsOperationOffcanvas.show();
        return bsOperationOffcanvas;
    }

    static setButtonLoading(button, loadingText = translations.labels.buttonsLoadingText) {
        button.disabled = true;
        button.dataset.originalHtml = button.innerHTML;
        button.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ${loadingText}`;
    }

    static resetButton(button) {
        button.disabled = false;
        button.innerHTML = button.dataset.originalHtml;
        delete button.dataset.originalHtml;
    }

    static showModal(modalId) {
        const modalElement = document.getElementById(modalId);
        const modalInstance = new bootstrap.Modal(modalElement);
        modalInstance.show();
        return modalInstance;
    }

    static hideModal(modalId) {
        const modalElement = document.getElementById(modalId);
        const modalInstance = bootstrap.Modal.getInstance(modalElement);
        if (modalInstance) {
            modalInstance.hide();
        }
    }

    static createFormData(formElement) {
        const formData = new FormData(formElement);
        const data = {};
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        return data;
    }

    static showConfirmDialog(message, onConfirm, onCancel) {
        const confirmModal = `
            <div class="modal fade" id="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="confirmModalLabel">Confirm Action</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">${message}</div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-primary" id="confirmBtn">Confirm</button>
                        </div>
                    </div>
                </div>
            </div>`;

        document.body.insertAdjacentHTML('beforeend', confirmModal);
        const modalElement = document.getElementById('confirmModal');
        const modal = new bootstrap.Modal(modalElement);

        modalElement.querySelector('#confirmBtn').addEventListener('click', () => {
            modal.hide();
            onConfirm();
        });

        modalElement.addEventListener('hidden.bs.modal', () => {
            if (onCancel) onCancel();
            modalElement.remove();
        });

        modal.show();
    }
} 