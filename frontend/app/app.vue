<template>
  <nuxt-layout>
    <client-only>
      <volt-toast />
    </client-only>
    
    <nuxt-loading-indicator />
    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
await useSession()

const tokens = ['bg-primary-50', 'dark:bg-primary-950']

onMounted(() => { document.body.classList.add(...tokens) })
onUnmounted(() => { document.body.classList.remove(...tokens) })

/**
 * Modals
 */

useState('loginModal', () => false)
useState('searchModal', () => false)
</script>

<style>
.page-enter-active,
.page-leave-active {
  transition: all 0.5s;
}

.page-enter-from,
.page-leave-to {
  opacity: 0;
  filter: blur(2rem);
}

.page-enter-to,
.page-leave-from {
  opacity: 1;
  filter: blur(0);
}
</style>
