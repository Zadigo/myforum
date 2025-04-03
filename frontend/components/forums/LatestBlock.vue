<template>
  <!-- Latest posts -->
  <section id="latest-posts">
    <div class="col-12 d-flex justify-content-between">
      <h3>{{ $t('Latest posts') }}</h3>
  
      <NuxtLink to="/whats-new" class="lh-lg">
        {{ $t('All new posts') }}
      </NuxtLink>
    </div>
  
    <div class="col-12">
      <CommentsIterator :comments="comments" :show-actions="false" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Comment } from '~/types';

const { $client } = useNuxtApp()
const { handleError } = useErrorHandler()

const comments = ref<Comment[]>([])

// async function getLatestComments () {
//   try {
//     const response = await $client.get<Comment>('/comments/latest')
//     comments.value = response.data
//   } catch (e) {
//     handleError(e)
//   }
// }

// onBeforeMount(getLatestComments)

useFetch(`/api/comments/latest`, {
  transform(data: Comment[]) {
    comments.value = data
    return data
  }
})
</script>
