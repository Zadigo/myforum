<template>
  <base-modal-vue :show="authStore.openLoginModal" @modal-close="authStore.openLoginModal=false">
    <template #default>
      <div class="row">
        <div class="col-12">
          <input v-model="credentials.username" type="text" placeholder="Email or username" autocomplete="username" class="form-control p-2">
          <input v-model="credentials.password" type="password" placeholder="Password" autocomplete="current-password" class="form-control p-2 my-1">
          <button class="btn btn-lg btn-primary" @click="login">
            Login
          </button>
        </div>
      </div>      
    </template>
  </base-modal-vue>
</template>

<script>
import BaseModalVue from '../layouts/BaseModal.vue'
import { useAuthentication } from '../store/authentication'

export default {
  name: 'ModalLogin',
  setup() {
    var authStore = useAuthentication()
    
    return {
      authStore
    }
  },
  components: {
    BaseModalVue
  },
  data: () => ({
    credentials: {
      username: null,
      email: null,
      password: null
    }
  }),
  methods: {
    async login() {
      try {
        var response = await this.$http.post('/accounts/login', this.credentials)
        this.authStore.setUser(response.data)
      } catch(error) {
        console.error(error)
      }
    }
  }
}
</script>
