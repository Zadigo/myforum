import { createApp, markRaw } from 'vue'
import { createPinia } from 'pinia'
import { createVueSession } from './plugins/vue-storages'
import { createClient } from './plugins/axios'
import { createVuetify } from 'vuetify'
import { QuillEditor } from '@vueup/vue-quill'

import App from './App.vue'
import router from './routes'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import DayJsAdapter from '@date-io/dayjs'
import '@/plugins/fontawesome'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

const store = createPinia()
const session = createVueSession()
const client = createClient()

const vuetify = createVuetify({
  components,
  directives,
  date: {
    adapter: DayJsAdapter
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  }
})

store.use(({ store }) => {
  store.vueSession = markRaw(session)
})


const app = createApp(App)
app.use(router)
app.use(store)
app.use(session)
app.use(client)
app.use(vuetify)
app.component('QuillEditor', QuillEditor)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
