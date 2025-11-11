<template>
  <volt-dialog v-model:visible="authStore.openLoginModal" modal @close="authStore.openLoginModal=false">
    <form @submit.prevent>
      <volt-input-text v-model="usernameField" type="username" autocomplete="username" placeholder="Username" flat />
      <volt-input-text v-model="password" type="password" autocomplete="current-password" placeholder="Password" flat />
      
      <volt-button @click="() => login()">
        Login
      </volt-button>
    </form>

    <form v-show="false" @submit.prevent>
      <volt-input-text v-model="usernameField" type="text" autocomplete="username" placeholder="Username" flat />
      <volt-input-text v-model="password" type="password" autocomplete="new-password" placeholder="Password 1" flat />
      <volt-input-text v-model="password" type="password" autocomplete="new-password" placeholder="Password 2" flat />
      
      <div class="flex justify-end">
        <volt-button @click="handleSignup">
          Signup
        </volt-button>          
      </div>
    </form>
  </volt-dialog>
</template>

<script setup lang="ts">
// const loginModal = useState('loginModal')

const authStore = useAuthentication()
const { usernameField, password, login } = useLogin('username')

// Signup
async function handleSignup () {}
</script>
