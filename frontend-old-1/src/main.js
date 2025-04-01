import { createApp, markRaw } from 'vue'
import App from './App.vue'
// import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import { createPinia, storeToRefs } from 'pinia'
import { createVueSession } from './plugins/vue-storages/session-storage'
import { createClient } from './plugins/axios'
import router from './routes'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import '@mdi/font/css/materialdesignicons.min.css'

const store = createPinia()
const app = createApp(App)
const session = createVueSession()

loadFonts()

store.use(({ store }) => {
    store.vueSession  = markRaw(session)
})

app.use(router)
app.use(store)
app.use(session)
app.use(createClient())
// .use(vuetify)
app.mount('#app')
