<template>
  <nav :class="{ 'navbar-dark text-light bg-dark': darkMode, 'navbar-light text-dark': !darkMode }" class="navbar navbar-expand-lg">
    <div class="container">
      <NuxtLink to="/" class="navbar-brand me-2 fw-bold text-uppercase">
        My Forum
      </NuxtLink>

      <button class="navbar-toggler" type="button" aria-controls="navbarButtonsExample" aria-expanded="false" aria-label="Toggle navigation">
        <font-awesome icon="bars" />
      </button>
      
      <button type="button" @click="toggle()">
        Dark
      </button>

      <div id="navbarButtonsExample" class="collapse navbar-collapse">
        <!-- <form class="input-group w-auto mx-5">
          <input type="search" class="form-control rounded" placeholder="Search" aria-label="Search" aria-describedby="search-addon" />
        </form> -->
        <!-- <button type="button" class="btn btn-light shadow-none border rounded w-50 ms-4 text-right" @click="store.openSearchModal=true">
          Search
        </button> -->

        <v-btn variant="tonal" @click="forumStore.openSearchModal=true">
          Search
        </v-btn>

        <div class="d-flex align-items-center ms-auto">
          <a v-if="!authStore.isAuthenticated" href="#" type="button" class="btn btn-link px-3 me-2" @click.prevent="authStore.openLoginModal=true">
            Login
          </a>

          <a v-else href="#" type="button" class="btn btn-link px-3 me-2" @click.prevent="authStore.logout()">
            Logout
          </a>

          <a v-if="!authStore.isAuthenticated" href="#" type="button" class="btn btn-primary me-3" @click.prevent="authStore.openLoginModal=true">
            Sign up for free
          </a>

          <NuxtLink v-if="authStore.isAuthenticated" to="/user/1" type="button" class="btn btn-primary me-3">
            Profile
          </NuxtLink>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useDark, useToggle } from '@vueuse/core';

const darkMode = useDark()
const toggle = useToggle(darkMode)

const authStore = useAuthentication()
const forumStore = useForums()
</script>
