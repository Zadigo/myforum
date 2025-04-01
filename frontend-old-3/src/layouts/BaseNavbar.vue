<template>
  <nav :class="{ 'navbar-dark text-light bg-dark': darkMode, 'navbar-light text-dark': !darkMode }" class="navbar navbar-expand-lg">
    <div class="container">
      <router-link :to="{ name: 'forums_view' }" class="navbar-brand me-2 fw-bold text-uppercase">
        My Forum
      </router-link>

      <button class="navbar-toggler" type="button" aria-controls="navbarButtonsExample" aria-expanded="false" aria-label="Toggle navigation">
        <i class="fas fa-bars"></i>
      </button>
      
      <button type="reset" @click="toggleDarkMode">Dark</button>

      <div id="navbarButtonsExample" class="collapse navbar-collapse">
        <!-- <form class="input-group w-auto mx-5">
          <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon" />
        </form> -->
        <button type="button" class="btn btn-light shadow-none border rounded w-50 ms-4 text-right" @click="store.openSearchModal=true">
          Search
        </button>

        <div class="d-flex align-items-center ms-auto">
          <a v-if="!authStore.isAuthenticated" href type="button" class="btn btn-link px-3 me-2" @click.prevent="authStore.openLoginModal=true">
            Login
          </a>

          <a v-else href type="button" class="btn btn-link px-3 me-2" @click.prevent="authStore.unsetUser">
            Logout
          </a>

          <router-link v-if="!authStore.isAuthenticated" to="/signup" type="button" class="btn btn-primary me-3">
            Sign up for free
          </router-link>

          <router-link v-if="authStore.isAuthenticated" :to="{ name: 'profile_view', params: { id: authStore.user.id } }" type="button" class="btn btn-primary me-3">
            Profile
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { useForum } from '../store/forum'
import { inject } from 'vue'
import { useAuthentication } from '../store/authentication'

export default {
  name: 'BaseNavbar',
  setup() {
    const store = useForum()
    const authStore = useAuthentication()
    const darkMode = inject('darkMode')
    const toggleDarkMode = inject('toggleDarkMode')

    return {
      store,
      authStore,
      darkMode,
      toggleDarkMode
    }
  }
}
</script>

<style scoped>
.navbar {
  height: 90px;
}
</style>
