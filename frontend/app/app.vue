<template>
  <NuxtLayout>
    <NuxtLoadingIndicator />
    <NuxtPage />
  </NuxtLayout>
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

onMounted(() => { document.body.classList.add('bg-slate-100/50') })
onUnmounted(() => { document.body.classList.remove('bg-slate-100/50') })
</script>
