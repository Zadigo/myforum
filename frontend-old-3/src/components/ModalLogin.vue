<template>
  <v-dialog v-model="authStore.openLoginModal" width="500" @close="authStore.openLoginModal=false">
    <v-card>
      <v-card-text>
        <div class="row">
          <div class="col-12">
            <v-text-field v-model="requestData.username" type="text" placeholder="Email or username" autocomplete="username" variant="outlined"></v-text-field>
            <v-text-field v-model="requestData.password" type="password" placeholder="Password" autocomplete="current-password" class="my-1" variant="outlined"></v-text-field>
            
            <div class="d-flex justify-content-center">
              <v-btn color="primary" rounded @click="login">
                Login
              </v-btn>
            </div>
          </div>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
// import BaseModalVue from '../layouts/BaseModal.vue'
import { useAuthentication } from '../store/authentication'

export default {
  name: 'ModalLogin',
  components: {
    // BaseModalVue
  },
  setup() {
    const authStore = useAuthentication()
    
    return {
      authStore
    }
  },
  data () {
    return {
      requestData: {
        username: null,
        email: null,
        password: null
      }
    }
  },
  methods: {
    async login() {
      // Login the user
      try {
        const response = await this.$http.post('/accounts/login', this.requestData)
        this.authStore.setUser(response.data)
      } catch(error) {
        console.error(error)
      }
    }
  }
}
</script>
