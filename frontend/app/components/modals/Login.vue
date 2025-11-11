<template>
  <VoltDialog v-model:visible="authStore.openLoginModal" modal @close="authStore.openLoginModal=false">
    <form @submit.prevent>
      <VoltInputText v-model="username" type="username" autocomplete="username" placeholder="Username" flat />
      <VoltInputText v-model="password" type="password" autocomplete="current-password" placeholder="Password" flat />
      
      <VoltButton @click="handleLogin">
        Login
      </VoltButton>
    </form>

    <form v-show="false" @submit.prevent>
      <VoltInputText v-model="username" type="text" autocomplete="username" placeholder="Username" flat />
      <VoltInputText v-model="password" type="password" autocomplete="new-password" placeholder="Password 1" flat />
      <VoltInputText v-model="password" type="password" autocomplete="new-password" placeholder="Password 2" flat />
      
      <div class="flex justify-end">
        <VoltButton @click="handleSignup">
          Signup
        </VoltButton>          
      </div>
    </form>
  </VoltDialog>
</template>

<script setup lang="ts">
import type { LoginAPIResponse } from '~/types'

const { client } = useLogin()
const authStore = useAuthentication()
const { $toast } = useNuxtApp()

const username = ref<string>('')
const password = ref<string>('')

const cookieAccessToken = useCookie<string>('access')
const cookieRefreshToken = useCookie<string>('refresh')

/**
 *
 */
async function handleLogin () {
  try {
    const response = await client.post<LoginAPIResponse>('/auth/v1/token/', {
      username: username.value,
      password: password.value
    })

    authStore.accessToken = response.data.access
    cookieAccessToken.value = response.data.access
    cookieRefreshToken.value = response.data.refresh

    authStore.openLoginModal = false
    username.value = ''
    password.value = ''
    
    $toast('Connected')
  } catch {
    // Handle error
  }
}

/**
 *
 */
async function handleSignup () {
  // Do something
}
</script>
