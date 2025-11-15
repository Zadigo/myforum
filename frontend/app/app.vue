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
      <client-only>
        <volt-card class="fixed left-5 top-5 z-40">
          <template #content>
            <p>User ID: {{ userId }}</p>
            <p>Authenticated: {{ isAuthenticated }}</p>
            <p>Has Token: {{ hasToken }}</p>
          </template>
        </volt-card>
      </client-only>
    </dev-only>

    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
const { hasToken, verify } = useNuxtAuthentication()
const { userId, isAuthenticated } = useUser()


await verify('token', 'Token is not valid')

await useSession()

const tokens = ['bg-primary-50', 'dark:bg-primary-950']

onMounted(() => { document.body.classList.add(...tokens) })
onUnmounted(() => { document.body.classList.remove(...tokens) })

/**
 * Modals
 */

useState<boolean>('loginModal', () => false)
useState<boolean>('searchModal', () => false)
useState<boolean>('createCommentModal', () => false)
useState<boolean>('loadedQuillEditor', () => false)
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
