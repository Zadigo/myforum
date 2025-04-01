<template>
  <v-app>
    <section id="forum">
      <!-- Navbar -->
      <base-navbar-vue />
  
      <!-- Messages -->
      <base-messages-vue />
  
      <router-view v-slot="{ Component }">
        <transition name="base-transition" mode="out-in">
          <component :is="Component" :key="$route.name" />
        </transition>
      </router-view>
  
      <!-- Footer -->
      <base-footer-vue />
      <modal-search-vue id="search" />
      <modal-login-vue id="login" />
    </section>
  </v-app>
</template>

<script>
import { useDark, useToggle } from '@vueuse/core'
import BaseMessagesVue from '@/layouts/BaseMessages.vue'
import BaseNavbarVue from '@/layouts/BaseNavbar.vue'
import BaseFooterVue from '@/layouts/BaseFooter.vue'
import ModalSearchVue from './components/ModalSearch.vue'
import ModalLoginVue from './components/ModalLogin.vue'

import { provide } from 'vue'

export default {
  name: 'App',
  components: {
    BaseMessagesVue,
    BaseNavbarVue,
    BaseFooterVue,
    ModalLoginVue,
    ModalSearchVue
  },
  setup () {
    const darkMode = useDark()
    const toggleDarkMode = useToggle(darkMode)
    provide('darkMode', darkMode)
    provide('toggleDarkMode', toggleDarkMode)
  },
}
</script>

<style>
@import url('./assets/style.css');

.base-transition-enter-active,
.base-transition-leave-active {
  transition: all .2s ease-in-out;
}

.base-transition-enter-from,
.base-transition-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}

.base-transition-enter-to,
.base-transition-leave-from {
  opacity: 1;
  transform: translateX(0px);
}
</style>
