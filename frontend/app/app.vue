<template>
  <nuxt-layout>
    <nuxt-loading-indicator />
    <nuxt-page />
  </nuxt-layout>
</template>

<script setup lang="ts">
await useSession()

const tokens = ['bg-primary-50', 'dark:bg-primary-900']

onMounted(() => { document.body.classList.add(...tokens) })
onUnmounted(() => { document.body.classList.remove(...tokens) })
</script>
