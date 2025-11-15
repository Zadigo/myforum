<template>
  <section id="comments">
    <client-only>
      <template #default>
        <!-- New Comment -->
        <div v-if="showCreateCommentForm" class="row">
          <!-- Form -->
          <keep-alive>
            <comments-create-form @editor-content="handleEditorContent" @created="handleCommentCreated" @close="toggleShowCreateCommentForm" />
          </keep-alive>
        </div>
  
        <!-- Main -->
        <div v-else class="row">
          <!-- Poll -->
          <suspense>
            <async-poll-section class="mb-3" />
  
            <template #fallback>
              <volt-skeleton class="h-[200px]" />
            </template>
          </suspense>
  
          <!-- Comments -->
          <div>
            <comments-wrapper :comments="threadComments" @reply="handleReply" />
          </div>
        </div>
      </template>

      <template #fallback>
        <volt-skeleton height="200px" width="100%" />
        <volt-skeleton height="100px" width="100%" />
      </template>
    </client-only>

    <div class="row">
      <h1 class="font-bold text-2xl my-5">Recommended reading</h1>

      <volt-card v-for="i in 5" :key="i" class="shadow-sm mb-2">
        <template #content>
          {{ i }}
        </template>
      </volt-card>
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

const { refresh, data } = await useFetch<ThreadCommentsApiResponse>(`/api/threads/${id}/comments`, {
  method: 'GET',
  query: {
    limit: 30,
    offset: currentOffset.value 
  }
})

if (data.value) {
  threadComments.value = data.value.results
}

console.log('Fetched comments:', threadComments)

/**
 * Current Thread Information
 */

const { execute } = await useFetch<ForumThread>(`/api/threads/${id}`, {
  immediate: false,
  transform(data: ForumThread) {
    currentThread.value = data
    return data
  }
})

await execute()

//
function handleEditorContent(data: { text: string, delta: string, html: string }) {
  console.log(data)
}

//
async function handlePagination() {
  refresh()
}

//
async function handleCommentCreated () {
  // await getComments()
  toggleShowCreateCommentForm()
}

/**
 * Replies
 */

const [showCreateCommentForm, toggleShowCreateCommentForm] = useToggle(false)

// TODO: Does not return the last comment that
// was created in the database
function handleReply(comment: UserComment) {
  replyingToComment.value = comment
  toggleShowCreateCommentForm()
}

/**
 * SEO
 */

useHead({
  title: currentThread.value?.title || '...'
})
</script>
