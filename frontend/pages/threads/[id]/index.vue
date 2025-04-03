<template>
  <section id="comments">
    <!-- enter-to-class="animate__animated animate__zoomIn" -->
    <Transition mode="out-in">
      <!-- Editor -->
      <CommentsForm v-if="store.showCreateCommentForm" @editor-content="handleEditorContent" @created="handleCommentCreated" @close="store.showCreateCommentForm=false" />

      <div v-else class="row">
        <!-- Poll -->
        <Suspense>
          <AsyncPollSection class="mb-3" />

          <template #loading>
            Loading...
          </template>
        </Suspense>
        
        <div class="col-12">
          <div class="row">
            <!-- Pagination -->
            <div class="col-12 d-flex justify-content-between mb-3">
              <span>Left</span>
              <BasePagination v-model="currentOffset" :previous-url="`http://example.com?limit=1&offset=0`" :next-url="`http://example.com?limit=1&offset=1`" @paginate="handlePagination" />
            </div>

            <!-- Comments -->
            <CommentsWrapper :comments="threadComments" @reply="handleReply" />
            
            <!-- Pagination -->
            <div class="col-12 d-flex justify-content-end mt-3">
              <BasePagination v-model="currentOffset" :previous-url="`http://example.com?limit=1&offset=0`" :next-url="`http://example.com?limit=1&offset=1`" @paginate="handlePagination" />
            </div>
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
    </Transition>
  </section>
</template>

<script setup lang="ts">
import type { Comment, ForumThread } from '~/types';

const AsyncPollSection = defineAsyncComponent({
  loader: async () => import('~/components/threads/Poll.vue')
})

const { id } = useRoute().params
const store = useForums()
const { threadComments, currentThread } = storeToRefs(store)

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
  transform(data) {
    threadComments.value = data
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
