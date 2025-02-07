// static/js/common/api-service.js
export class ApiService {
    static async fetch(url, options = {}) {
        try {
            const response = await fetch(url, {
                credentials: 'include',
                headers: {
                    'Accept': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async get(url) {
        return this.fetch(url);
    }

    static async post(url, data) {
        const options = {
            method: 'POST',
            body: data instanceof FormData ? data : JSON.stringify(data),
            headers: data instanceof FormData ? {} : {
                'Content-Type': 'application/json'
            }
        };
        return this.fetch(url, options);
    }

    static async put(url, data) {
        const options = {
            method: 'PUT',
            body: data instanceof FormData ? data : JSON.stringify(data),
            headers: data instanceof FormData ? {} : {
                'Content-Type': 'application/json'
            }
        };
        return this.fetch(url, options);
    }

    static async delete(url, data) {
        const options = {
            method: 'DELETE',
            body: data instanceof FormData ? data : JSON.stringify(data),
            headers: data instanceof FormData ? {} : {
                'Content-Type': 'application/json'
            }
        };
        return this.fetch(url, options);
    }
} 