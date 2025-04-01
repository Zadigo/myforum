<template>
  <section id="comments">
    <Transition enter-to-class="animate__animated animate__zoomIn" mode="out-in">
      <!-- Editor -->
      <CommentsForm v-if="store.showCreateCommentForm" @editor-content="handleEditorContent" @created="handleCommentCreated" @close="store.showCreateCommentForm=false" />

      <div v-else class="row">
        <!-- Poll -->
        <!-- <suspense>
          <async-poll-section class="mb-5" />
        </suspense> -->

        <!-- <keep-alive>
          <async-poll-section-vue class="mb-5" />
        </keep-alive> -->

        <div class="col-12">
          <div class="row">
            <div class="col-12 d-flex justify-content-between mb-3">
              <span>Left</span>
              <BasePagination :pagination="currentPagination" :cached-response="cachedResponse" @paginate="handlePagination" />
            </div>

            <!-- Comments -->
            <CommentsIterator :comments="threadComments" @reply="handleReply" />

            <div class="col-12 d-flex justify-content-end mt-3">
              <BasePagination :pagination="currentPagination" :cached-response="cachedResponse" @paginate="handlePagination" />
            </div>
          </div>

          <div class="row">
            <div class="col-12">
              <h1 class="fw-bold display-6 my-5">Recommended reading</h1>

              <div v-for="i in 5" :key="i" class="card mb-2">
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
import type { Comment, Thread, ThreadApiResponse } from '~/types';
import { useSessionStorage } from '@vueuse/core';


const store = useForums()
const { threadComments, currentThread } = storeToRefs(store)
const { handleError } = useErrorHandler()
const { $client } = useNuxtApp()
const { id } = useRoute().params

const cachedResponse = ref<ThreadApiResponse>()
// const showCreateCommentForm = ref(false)
const currentPagination = ref(1)
const replyingToComment = ref<Comment>()

const threads = useSessionStorage<Thread[]>('threads', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

provide('replyingToComment', replyingToComment)

function handleEditorContent(data: { text: string }) {
  // Sets the Quill content to the final
  // request data for the API
  // requestData.content = data.text
  // requestData.content_delta = data.delta
  // requestData.content_html = data.html
  console.log(data)
}

async function getComments(page = 1) {
  try {
    if (currentThread.value) {  
      const response = await $client.get<ThreadApiResponse>(`threads/${currentThread.value.id}/comments`, { params: { page } })
      threadComments.value = response.data.results
      cachedResponse.value = response.data
    }
  } catch (e) {
    handleError(e)
  }
}

async function handlePagination (page: number) {
  await getComments(page)
}

async function handleCommentCreated () {
  await getComments()
  store.showCreateCommentForm = false
}

// TODO: Does not return the last comment that
// was created in the database
function handleReply(comment: Comment) {
  replyingToComment.value = comment
  store.showCreateCommentForm = true
}

onBeforeMount(async () => {
  store.forumThreads = threads.value
  store.setCurrentThread(id)
  await getComments()
})
</script>
