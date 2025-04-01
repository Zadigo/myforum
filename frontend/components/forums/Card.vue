<template>
  <NuxtLink to="/rules" aria-label="Site rules / FAQ" class="text-dark">
    <article class="card shadow-sm" role="article">
      <div class="card-body">
        <h3 class="card-title">
          {{ title }}
        </h3>
        
        <p class="card-text">
          {{ text }}
        </p>
      </div>
    </article>
  </NuxtLink>
</template>

<script setup lang="ts">
defineProps({
  title: {
    type: String,
    required: true
  },
  text: {
    type: String,
    required: true
  }
})
</script>
