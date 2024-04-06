const { VITE_API_V } = import.meta.env;
export const baseUrlApi = (url: string) => `/proxy/api/${VITE_API_V}/${url}`;
