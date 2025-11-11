<template>
  <volt-card role="article" class="shadow-sm">
    <template #title>
      <NuxtLink to="/rules">
        <h3 class="font-bold">
          {{ title }}
        </h3>
      </NuxtLink>
    </template>

    <template #content>
      <NuxtLink to="/rules">
        {{ text }}
      </NuxtLink>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
defineProps<{ title: string, text: string }>()
</script>
