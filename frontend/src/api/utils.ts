const { VITE_API_V } = import.meta.env;
export const baseUrlApi = (url: string) => `/proxy/api/${VITE_API_V}${url}`;
export const baseUrl = (url: string) => `/proxy${VITE_API_V}${url}`;
export const baseUrlNoVersion = (url: string) => `/proxy${url}`;
export const baseUrlApiNoVersion = (url: string) => `/proxy/api${url}`;
export const staticUrl = (url: string) => `/proxy/static${url}`;
