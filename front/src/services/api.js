import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/docs'
})

api.interceptors.request.use()

export default api