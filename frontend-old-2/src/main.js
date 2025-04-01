import App from './App.vue'

import { createPinia } from 'pinia'
// import { useScript } from 'unhead'
import { createApp, toRaw } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { createVuetify } from 'vuetify'
import { createHead } from 'unhead'
import { useVueSession } from './plugins/vue-storages'
import { QuillEditor } from '@vueup/vue-quill'

import router from './router'

import './style.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'mdb-ui-kit/css/mdb.min.css'
import 'vuetify/styles'
import 'mdb-ui-kit/css/mdb.min.css'
import '@mdi/font/css/materialdesignicons.css'
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import installPlugins from './plugins'

import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import colors from 'vuetify/util/colors'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

const head = createHead({
  plugins: [
    // CapoPlugin()
  ]
})

const pinia = createPinia()
pinia.use(({ store }) => {
  const { session } = useVueSession()

  store.$router = toRaw(router)
  store.$session = toRaw(session)
})

const plugins = installPlugins()

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    themes: {
      light: {
        dark: false,
        colors: {
          primary: colors.red.darken1
        }
      }
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi
    }
  }
})

const app = createApp(App)
app.use(router)
app.use(pinia)
app.use(plugins)
app.use(vuetify)
app.use(head)
app.component('QuillEditor', QuillEditor)
app.component('FontAwesomeIcon', FontAwesomeIcon)
app.mount('#app')
