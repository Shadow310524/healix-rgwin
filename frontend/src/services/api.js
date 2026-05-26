import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const api = axios.create({
  baseURL: API_URL,
});

// Interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const authService = {
  login: async (email, password) => {
    const params = new URLSearchParams();
    params.append('username', email);
    params.append('password', password);
    
    const response = await api.post('/auth/login', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return response.data;
  },
  getCurrentUser: async () => {
    const response = await api.post('/auth/test-token');
    return response.data;
  }
};

export const productService = {
  getProducts: async () => {
    const response = await api.get('/products/');
    return response.data;
  },
  createProduct: async (productData) => {
    const response = await api.post('/products/', productData);
    return response.data;
  }
};

export const categoryService = {
  getCategories: async () => {
    const response = await api.get('/categories/');
    return response.data;
  },
  createCategory: async (categoryData) => {
    const response = await api.post('/categories/', categoryData);
    return response.data;
  }
};

export const enquiryService = {
  getEnquiries: async () => {
    const response = await api.get('/enquiries/');
    return response.data;
  },
  createEnquiry: async (enquiryData) => {
    const response = await api.post('/enquiries/', enquiryData);
    return response.data;
  }
};
export const uploadService = {
  uploadImage: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  }
};
export const chatService = {
  sendMessage: async (messages) => {
    const response = await api.post('/chat/', { messages });
    return response.data;
  }
};

export default api;
