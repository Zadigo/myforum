<template>
  <section id="latest-posts">
    <div class="flex justify-between">
      <h3 class="font-bold text-2xl">
        {{ $t('Latest posts') }}
      </h3>
      
      <VoltSecondaryButton>
        <NuxtLinkLocale to="/whats-new" class="lh-lg">
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
import type { Comment } from '~/types'

const { data: comments } = useFetch<Comment[]>('/api/comments/latest')
</script>
