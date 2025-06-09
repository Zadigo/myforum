<template>
  <!-- Latest posts -->
  <section id="latest-posts">
    <div class="flex justify-between">
      <h3>{{ $t('Latest posts') }}</h3>
      
      <VoltSecondaryButton>
        <NuxtLinkLocale to="/whats-new" class="lh-lg">
          {{ $t('All new posts') }}
        </NuxtLinkLocale>
      </VoltSecondaryButton>
    </div>
  
    <div>
      <CommentsIterator :comments="comments" :show-actions="false" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Comment } from '~/types';

const comments = ref<Comment[]>([])

useFetch(`/api/comments/latest`, {
  transform(data: Comment[]) {
    comments.value = data
    return data
  }
})
</script>
