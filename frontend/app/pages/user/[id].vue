<template>
  <div>
    Profile
  </div>
</template>

<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import type { User } from '~/types';

const { $nuxtAuthentication } = useNuxtApp()

const authStore = useAuthentication()
const cookieUserProfile = useSessionStorage<User>('user', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

async function handleGetProfile() {
  try {
    const data = await $nuxtAuthentication<User>('/accounts/profile', { method: 'GET' })
    authStore.userProfile = data
    cookieUserProfile.value = data
  } catch {
    // Do something
  }
}

onBeforeMount(handleGetProfile)
</script>
