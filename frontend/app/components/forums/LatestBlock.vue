<template>
  <section id="latest-posts">
    <div class="flex justify-between items-center mb-5">
      <h3 class="font-bold font-title text-2xl dark:text-primary-100">
        {{ $t('Latest posts') }}
      </h3>
      
      <volt-secondary-button>
        <nuxt-link-locale to="/whats-new">
          {{ $t('All new posts') }}
        </nuxt-link-locale>
      </volt-secondary-button>
    </div>
    
    <!-- Latest Comments -->
    <comments-iterator :comments="comments || []" :show-actions="false" />
  </section>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

const comments = await $fetch<UserComment[]>('/api/comments/latest', { method: 'GET' })
</script>
