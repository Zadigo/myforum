import axios from 'axios'
import { useAuthentication } from '../store/authentication'
// import { useMessages } from '../store/messages'

axios.defaults.headers.common['Content-Type'] = 'application/json'
axios.defaults.headers.common['Accept-Language'] = 'fr,en;q=0.9'

const client = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/v1/',
    responseType: 'json',
    withCredentials: true,
    timeout: 5000
})

function createClient () {
    return {
        install: (app) => {
            app.config.globalProperties.$http = client
        }
    }
}

client.interceptors.request.use(
    request => {
        var store = useAuthentication()
        if (store.isAuthenticated) {
            request.headers.Authorization = `Token ${store.token}`
        }
        return request
    },

    error => {
        return Promise.reject(error)
    }
)

client.interceptors.response.use(
    response => {
        if (response.status === 401) {
            const store = useAuthentication()
            store.unsetUser()
        }
        return response
    },

    error => {
        return Promise.reject(error)
    }
)

export {
    client,
    createClient
}
