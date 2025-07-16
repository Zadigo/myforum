<template>
  <section id="comments">
    <!-- Editor -->
    <div v-if="store.showCreateCommentForm" class="row">
      <KeepAlive>
        <CommentsForm @editor-content="handleEditorContent" @created="handleCommentCreated" @close="store.showCreateCommentForm=false" />
      </KeepAlive>
    </div>

    <div v-else class="row">
      <!-- Poll -->
      <Suspense>
        <AsyncPollSection class="mb-3" />

        <template #fallback>
          <VoltSkeleton class="h-[100px]" />
        </template>
      </Suspense>

      <!-- Comments -->
      <div>
        <CommentsWrapper :comments="threadComments" @reply="handleReply" />
      </div>
    </div>

    <div class="row">
      <h1 class="font-bold display-6 my-5">Recommended reading</h1>

      <div v-for="i in 5" :key="i" class="card shadow-sm mb-2">
        <div class="card-body">
          {{ i }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Comment, ForumThread, ThreadCommentsApiResponse } from '~/types'

definePageMeta({
  layout: 'threads'
})

const AsyncPollSection = defineAsyncComponent({
  loader: async () => import('~/components/threads/Poll.vue')
})

// const cachedResponse = ref<ThreadCommentsApiResponse>()
const replyingToComment = ref<Comment>()

provide('replyingToComment', replyingToComment)

/**
 * Comments for the current thread
 */

const { id } = useRoute().params
const store = useForums()
const { threadComments, currentThread } = storeToRefs(store)
const currentOffset = ref<number>(1)

const { refresh, data: cachedResponse } = await useFetch<ThreadCommentsApiResponse>(`/api/threads/${id}/comments`, {
  query: {
    limit: 30,
    offset: currentOffset.value 
  }
})

if (cachedResponse.value) {
  threadComments.value = cachedResponse.value.results
}

/**
 * Information for the current thread
 */

const { execute } = await useFetch<ForumThread>(`/api/threads/${id}`, {
  immediate: false,
  transform(data: ForumThread) {
    currentThread.value = data
    return data
  }
})

execute()

/**
 *
 * @param data 
 */
function handleEditorContent(data: { text: string, delta: string, html: string }) {
  console.log(data)
}

/**
 *
 */
async function handlePagination() {
  refresh()
}

/**
 *
 */
async function handleCommentCreated () {
  // await getComments()
  store.showCreateCommentForm = false
}

/**
 *
 */
// TODO: Does not return the last comment that
// was created in the database
function handleReply(comment: Comment) {
  replyingToComment.value = comment
  store.showCreateCommentForm = true
}

useHead({
  title: currentThread.value?.title || '...'
})
</script>
