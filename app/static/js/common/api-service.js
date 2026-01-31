// static/js/common/api-service.js

/**
 * Custom API Error class for structured error handling.
 * Matches the backend error response format.
 */
export class APIError extends Error {
    constructor(errorData) {
        super(errorData?.message || 'An unknown error occurred');
        this.name = 'APIError';
        this.code = errorData?.code || 'UNKNOWN_ERROR';
        this.status = errorData?.status || 500;
        this.details = errorData?.details || null;
    }
}

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
                // Try to parse error response from backend
                let errorData = null;
                try {
                    const responseBody = await response.json();
                    // Handle new standardized error format
                    if (responseBody.error) {
                        errorData = {
                            code: responseBody.error.code || `HTTP_${response.status}`,
                            message: responseBody.error.message || response.statusText,
                            status: response.status,
                            details: responseBody.error.details || null
                        };
                    } else if (responseBody.message) {
                        // Handle legacy error format
                        errorData = {
                            code: `HTTP_${response.status}`,
                            message: responseBody.message,
                            status: response.status
                        };
                    }
                } catch (parseError) {
                    // If parsing fails, create error from status
                    errorData = {
                        code: `HTTP_${response.status}`,
                        message: response.statusText || 'Network response was not ok',
                        status: response.status
                    };
                }
                throw new APIError(errorData);
            }

            return await response.json();
        } catch (error) {
            // Re-throw APIError as-is, wrap other errors
            if (error instanceof APIError) {
                console.error('API Error:', error.code, error.message);
                throw error;
            }
            console.error('Network Error:', error);
            throw new APIError({
                code: 'NETWORK_ERROR',
                message: error.message || 'Network request failed',
                status: 0
            });
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