<template>
  <section id="forum">
    <!-- Navbar -->
    <base-navbar-vue />

    <!-- Messages -->
    <base-messages-vue />

    <router-view v-slot="{ Component }">
      <transition name="base-transition" mode="out-in">
        <component :key="$route.name" :is="Component" />
      </transition>
    </router-view>
    
    <!-- Footer -->
    <base-footer-vue />
    <modal-search-vue />
    <modal-login-vue />
  </section>
</template>

<script>
import BaseMessagesVue from './layouts/BaseMessages.vue'
import BaseNavbarVue from './components/BaseNavbar.vue'
import BaseFooterVue from './components/BaseFooter.vue'
import ModalSearchVue from './components/ModalSearch.vue'
import ModalLoginVue from './components/ModalLogin.vue'

import { provide, ref } from 'vue'

export default {
  name: 'App',
  setup() {
    var darkMode = ref(false)

    provide('dark_mode', {
      darkMode,
      toggleDarkMode
    })
    
    function toggleDarkMode() {
      darkMode.value = !darkMode.value
    }

  },
  components: {
    BaseMessagesVue,
    BaseNavbarVue,
    BaseFooterVue,
    ModalLoginVue,
    ModalSearchVue
  }
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
