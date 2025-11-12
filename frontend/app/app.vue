<template>
  <nuxt-layout>
    <client-only>
      <!-- Toast -->
      <template #default>
        <volt-toast />
      </template>
    </client-only>
    
    <!-- Indicator -->
    <nuxt-loading-indicator />

    <dev-only>
      <volt-card class="fixed left-5 top-5 z-40">
        <template #content>
          <p>User ID: {{ userId }}</p>
          <p>Authenticated: {{ isAuthenticated }}</p>
          <p>Has Token: {{ hasToken }}</p>
        </template>
      </volt-card>
    </dev-only>

    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
const { hasToken } = useNuxtAuthentication()
const { userId, isAuthenticated } = useUser()
console.info('nuxt authentication state:', { userId: userId.value, isAuthenticated: isAuthenticated.value })

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
