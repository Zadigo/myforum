<template>
  <section id="comments">
    <client-only>
      <div v-if="store.showCreateCommentForm" class="row">
        <!-- Form -->
        <keep-alive>
          <CommentsForm @editor-content="handleEditorContent" @created="handleCommentCreated" @close="store.showCreateCommentForm=false" />
        </keep-alive>
      </div>

      <div v-else class="row">
        <!-- Poll -->
        <Suspense>
          <AsyncPollSection class="mb-3" />

          <template #fallback>
            <VoltSkeleton class="h-[200px]" />
          </template>
        </Suspense>

        <!-- Comments -->
        <div>
          <CommentsWrapper :comments="threadComments" @reply="handleReply" />
        </div>
      </div>
    </client-only>

    <div class="row">
      <h1 class="font-bold text-2xl my-5">Recommended reading</h1>

      <VoltCard v-for="i in 5" :key="i" class="shadow-sm mb-2">
        <template #content>
          {{ i }}
        </template>
      </VoltCard>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { UserComment, ForumThread, ThreadCommentsApiResponse } from '~/types'

definePageMeta({
  name: 'Thread Comments',
  layout: 'threads'
})

const AsyncPollSection = defineAsyncComponent({
  loader: async () => import('~/components/threads/Poll.vue')
})

// const cachedResponse = ref<ThreadCommentsApiResponse>()
const replyingToComment = ref<UserComment>()

provide('replyingToComment', replyingToComment)

/**
 * Comments for the current thread
 */

const { id } = useRoute().params
const store = useForums()
const { threadComments, currentThread } = storeToRefs(store)
const currentOffset = ref<number>(1)

const { refresh, data: cachedResponse } = await useFetch<ThreadCommentsApiResponse>(`/api/threads/${id}/comments`, {
  method: 'GET',
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
function handleReply(comment: UserComment) {
  replyingToComment.value = comment
  store.showCreateCommentForm = true
}

/**
 * SEO
 */

useHead({
  title: currentThread.value?.title || '...'
})
</script>
