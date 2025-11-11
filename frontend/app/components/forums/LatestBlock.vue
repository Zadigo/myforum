<template>
  <section id="latest-posts">
    <div class="flex justify-between">
      <h3 class="font-bold font-title text-2xl">
        {{ $t('Latest posts') }}
      </h3>
      
      <VoltSecondaryButton>
        <NuxtLinkLocale to="/whats-new">
          {{ $t('All new posts') }}
        </NuxtLinkLocale>
      </VoltSecondaryButton>
    </div>
  
    <div>
      <CommentsIterator :comments="comments || []" :show-actions="false" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

const { data: comments } = await useFetch<UserComment[]>('/api/comments/latest', {
  method: 'GET'
})
</script>
