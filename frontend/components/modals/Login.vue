<template>
  <v-dialog v-model="authStore.openLoginModal" width="400" @close="authStore.openLoginModal=false">
    <v-card>
      <v-card-text>
        <v-form @submit.prevent>
          <v-text-field v-model="username" type="username" autocomplete="username" variant="solo-filled" placeholder="Username" flat />
          <v-text-field v-model="password" type="password" autocomplete="current-password" variant="solo-filled" placeholder="Password" flat />
          
          <v-btn variant="tonal" rounded @click="handleLogin">
            Login
          </v-btn>          
        </v-form>

        <v-form v-show="false" @submit.prevent>
          <v-text-field v-model="username" type="text" autocomplete="username" variant="solo-filled" placeholder="Username" flat />
          <v-text-field v-model="password" type="password" autocomplete="new-password" variant="solo-filled" placeholder="Password 1" flat />
          <v-text-field v-model="password" type="password" autocomplete="new-password" variant="solo-filled" placeholder="Password 2" flat />
          
          <div class="flex justify-end">
            <v-btn variant="tonal" rounded @click="handleSignup">
              Signup
            </v-btn>          
          </div>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
// import createDjangoClient from '~/composables/django_client';
import type { LoginAPIResponse } from '~/types';

const { client } = useAxiosClient()
const authStore = useAuthentication()
const { $toast } = useNuxtApp()

const username = ref<string>('')
const password = ref<string>('')

const cookieAccessToken = useCookie<string>('access')
const cookieRefreshToken = useCookie<string>('refresh')

async function handleLogin () {
  try {
    const response = await client.post<LoginAPIResponse>('/token/', {
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

async function handleSignup () {
  // Do something
}
</script>
