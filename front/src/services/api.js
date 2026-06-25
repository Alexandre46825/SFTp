import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/',
})

api.interceptors.request.use()

export default api