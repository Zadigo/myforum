import { useServerAxiosClient } from '~/composables/client'

export default defineNuxtPlugin(_nuxtApp => {
  const { client } = useServerAxiosClient()
  return {
    provide: {
      client
    }
  }
})
