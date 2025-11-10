<template>
  <div>
    Profile
  </div>
</template>

<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import type { User } from '~/types';

const { $client } = useNuxtApp()

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
    const response = await $client.get<User>('/accounts/profile')
    authStore.userProfile = response.data
    cookieUserProfile.value = response.data
  } catch {
    // Do something
  }
}

onBeforeMount(handleGetProfile)
</script>
