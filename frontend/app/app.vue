<template>
  <nuxt-layout>
    <nuxt-loading-indicator />
    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core'
import type { User } from './types'

const authStore = useAuthentication()

const cookieAccessToken = useCookie<string>('access')
const cookieRefreshToken = useCookie<string>('refresh')

const cachedUserProfile = useSessionStorage<User>('user', null, {
  serializer: {
    read(raw) {
      return JSON.parse(raw)
    },
    write(value) {
      return JSON.stringify(value)
    }
  }
})

authStore.accessToken = cookieAccessToken.value
authStore.refreshToken = cookieRefreshToken.value
authStore.userProfile = cachedUserProfile.value

const tokens = ['bg-primary-100', 'dark:bg-primary-900']

onMounted(() => { document.body.classList.add(...tokens) })
onUnmounted(() => { document.body.classList.remove(...tokens) })
</script>
