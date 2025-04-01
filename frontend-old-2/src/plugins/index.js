import { client } from './axios.js'
import { createVueSession, useVueSession } from './vue-storages/index.js'

import './fontawesome.js'
import './webfontloader.js'

import _ from 'lodash'
import cookies from 'universal-cookie'

import duration from 'dayjs/plugin/duration'
import utc from 'dayjs/plugin/utc'
import relativeTime from 'dayjs/plugin/relativeTime'
import dayjs from 'dayjs'
// import i18n from './i18n.js'

dayjs.extend(duration)
dayjs.extend(utc)
dayjs.extend(relativeTime)


const sessionPlugin = createVueSession({
  afterMount () {}
})

if (import.meta.env.DEV) {
  window.dayjs = dayjs
  window.lodash = _
  window.UniversalCookie = cookies
}

export {
  dayjs
}

export default function installPlugins () {
  return {
    install: (app) => {
      app.use(sessionPlugin)
      // app.use(i18n)

      const { session } = useVueSession()

      app.config.globalProperties.$http = client
      app.config.globalProperties.$date = dayjs()
      app.config.globalProperties.$session = session
    }
  }
}
