<template>
  <volt-dialog v-model:visible="loginModal" :dismissable-mask="false" modal>
    <form class="space-y-3" @submit.prevent>
      <volt-input-text v-model="usernameField" type="username" class="w-full" autocomplete="username" placeholder="Username" />
      <volt-input-text v-model="password" type="password" class="w-full" autocomplete="current-password" placeholder="Password" />
      
      <volt-button class="ms-auto" @click="() => login()">
        Login
      </volt-button>
    </form>

    <form v-show="false" @submit.prevent>
      <volt-input-text v-model="usernameField" type="text" autocomplete="username" placeholder="Username" />
      <volt-input-text v-model="password" type="password" autocomplete="new-password" placeholder="Password 1" />
      <volt-input-text v-model="password" type="password" autocomplete="new-password" placeholder="Password 2" />
      
      <div class="flex justify-end">
        <volt-button @click="handleSignup">
          Signup
        </volt-button>          
      </div>
    </form>
  </volt-dialog>
</template>

<script setup lang="ts">
const loginModal = useState<boolean>('loginModal')

const { usernameField, password, login } = useLogin('username')

// Signup
async function handleSignup () {}
</script>
