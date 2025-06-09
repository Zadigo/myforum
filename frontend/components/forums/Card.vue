<template>
  <VoltCard role="article">
    <template #title>
      <NuxtLink to="/rules">
        <h3 class="card-title">
          {{ title }}
        </h3>
      </NuxtLink>
    </template>

    <template #content>
      <NuxtLink to="/rules">
        {{ text }}
      </NuxtLink>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
defineProps<{ title: string, text: string }>()
</script>
