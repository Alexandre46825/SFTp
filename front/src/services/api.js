import axios from 'axios'

const api = axios.create({
  baseURL: "http://172.20.10.8:8000",
  //baseURL: "http://localhost:8000",
  withCredentials: false
})

api.interceptors.request.use((config) => {

  const token = localStorage.getItem('token')

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export default api