<template>
  <section id="comments">
    <ClientOnly>
      <!-- Editor -->
      <CommentsForm v-if="store.showCreateCommentForm" @editor-content="handleEditorContent" @created="handleCommentCreated" @close="store.showCreateCommentForm=false" />
    </ClientOnly>

    <div v-if="!store.showCreateCommentForm" class="row">
      <!-- Poll -->
      <Suspense>
        <template #default>
          <AsyncPollSection class="mb-3" />
        </template>

        <template #fallback>
          Loading...
        </template>
      </Suspense>
      
      <!-- Comments -->
      <div class="col-12">
        <div class="row">
          <ClientOnly>
            <!-- Pagination -->
            <div class="col-12 d-flex justify-content-between mb-3">
              <span>Left</span>
              <BasePagination v-model="currentOffset" :previous-url="cachedResponse?.previous" :next-url="cachedResponse?.next" @paginate="handlePagination" />
            </div>
          </ClientOnly>

          <!-- Comments -->
          <CommentsWrapper :comments="threadComments" @reply="handleReply" />
          
          <ClientOnly>
            <!-- Pagination -->
            <div class="col-12 d-flex justify-content-end mt-3">
              <BasePagination v-model="currentOffset" :previous-url="cachedResponse?.previous" :next-url="cachedResponse?.next" @paginate="handlePagination" />
            </div>
          </ClientOnly>
        </div>

        <div class="row">
          <div class="col-12">
            <h1 class="fw-bold display-6 my-5">Recommended reading</h1>

            <div v-for="i in 5" :key="i" class="card shadow-sm mb-2">
              <div class="card-body">
                {{ i }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { Comment, ForumThread, ThreadCommentsApiResponse } from '~/types';

const AsyncPollSection = defineAsyncComponent({
  loader: async () => import('~/components/threads/Poll.vue')
})

const { id } = useRoute().params
const store = useForums()
const { threadComments, currentThread } = storeToRefs(store)

const cachedResponse = ref<ThreadCommentsApiResponse>()
const currentOffset = ref<number>(1)
const replyingToComment = ref<Comment>()

provide('replyingToComment', replyingToComment)

function handleEditorContent(data: { text: string, delta: string, html: string }) {
  // Do something
  console.log(data)
}

// async function getComments(page = 1) {
//   try {
//     if (currentThread.value) {  
//       const response = await $client.get<ThreadApiResponse>(`threads/${currentThread.value.id}/comments`, { params: { page } })
//       threadComments.value = response.data.results
//       cachedResponse.value = response.data
//     }
//   } catch (e) {
//     handleError(e)
//   }
// }

const { refresh } = useFetch(`/api/threads/${id}/comments`, {
  query: {
    limit: 30,
    offset: currentOffset.value 
  },
  transform(data: ThreadCommentsApiResponse) {
    cachedResponse.value = data
    threadComments.value = data.results
    return data
  }
})

const { execute } = useFetch(`/api/threads/${id}`, {
  immediate: false,
  transform(data: ForumThread) {
    currentThread.value = data
    return data
  }
})

async function handlePagination() {
  refresh()
}

async function handleCommentCreated () {
  // await getComments()
  store.showCreateCommentForm = false
}

// TODO: Does not return the last comment that
// was created in the database
function handleReply(comment: Comment) {
  replyingToComment.value = comment
  store.showCreateCommentForm = true
}

useHead({
  title: currentThread.value?.title || '...'
})

execute()
</script>
