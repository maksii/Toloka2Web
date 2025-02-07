/*!
 * Language mode toggler
 */

(() => {
    'use strict'
  
    const getStoredLanguage = () => localStorage.getItem('language')
    const setStoredLanguage = language => localStorage.setItem('language', language)
  
    const getPreferredLanguage = () => {
        const storedLanguage = getStoredLanguage()
        if (storedLanguage) {
            return storedLanguage
        }
        return 'en' // Default to English
    }
  
    const setLanguage = (language, shouldReload = false) => {
        const currentLanguage = document.documentElement.getAttribute('data-bs-language')
        // Only reload if the language is actually changing and reload is requested
        if (currentLanguage !== language) {
            document.documentElement.setAttribute('data-bs-language', language)
            document.documentElement.setAttribute('lang', language)
            if (shouldReload) {
                // Give time for the MutationObserver to catch the change
                setTimeout(() => {
                    window.location.reload()
                }, 50)
            }
        }
    }
  
    const showActiveLanguage = (language) => {
        document.querySelectorAll('[data-bs-language-value]').forEach(element => {
            const btnToActive = element.getAttribute('data-bs-language-value') === language
            element.classList.toggle('active', btnToActive)
            element.setAttribute('aria-pressed', btnToActive)
        })

        // Update the check mark
        document.querySelectorAll('[data-bs-language-value] .bi.ms-auto').forEach(icon => {
            icon.classList.toggle('d-none', icon.closest('[data-bs-language-value]').getAttribute('data-bs-language-value') !== language)
        })
    }
  
    // Initial setup without reload
    const initialLanguage = getPreferredLanguage()
    setLanguage(initialLanguage)
  
    window.addEventListener('DOMContentLoaded', () => {
        showActiveLanguage(getPreferredLanguage())
  
        document.querySelectorAll('[data-bs-language-value]')
            .forEach(toggle => {
                toggle.addEventListener('click', () => {
                    const language = toggle.getAttribute('data-bs-language-value')
                    setStoredLanguage(language)
                    setLanguage(language, true)
                    showActiveLanguage(language, true)
                })
            })
    })
})(); 