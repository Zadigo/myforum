<template>
  <v-app>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </v-app>
</template>

<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import type { User } from './types';

const authStore = useAuthentication()

const cookieAccessToken = useCookie<string>('access')
const cookieRefreshToken = useCookie<string>('refresh')

const cachedUserProfile = useSessionStorage<User>('user', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

authStore.accessToken = cookieAccessToken.value
authStore.refreshToken = cookieRefreshToken.value
authStore.userProfile = cachedUserProfile.value
</script>
