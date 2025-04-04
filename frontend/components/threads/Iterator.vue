<template>
  <div class="col-12">
    <article v-for="(thread, i) in forumThreads" :key="thread.id" :class="{ 'mt-1': i > 0 }" role="article" @click="forumStore.setCurrentThread(thread.id)">
      <NuxtLink :to="`/threads/${thread.id}`" :aria-label="thread.title" class="text-dark">
        <div class="card shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-start align-items-center gap-2 mb-4">
              <img src="https://via.placeholder.com/200x200" class="rounded-circle" width="50" height="50">
              <h3 class="card-title m-0 h4">{{ thread.title }}</h3>
              <font-awesome v-if="thread.owned_by_user" icon="bolt-lightning" class="text-warning" />
            </div>

            <div v-if="thread.description" class="card-text fw-light my-2">
              {{ thread.description }}
            </div>

            <div class="card-info">
              <span class="badge bg-light text-dark p-2"><span class="mdi mdi-comment ms-2" /> {{ thread.number_of_comments }}</span>
              <span class="badge bg-light text-dark p-2 ms-2"><span class="mdi mdi-calendar ms-2" /> {{ formatData(thread.created_on) }}</span>
              <!-- <span class="badge bg-light text-dark p-2 ms-2">{{ formatData(thread.latest_comment.created_on) }}</span> -->
            </div>
          </div>
        </div>
      </NuxtLink>
    </article>
  </div>
</template>

<script setup lang="ts">
import type  { ForumThreadsApiResponse } from '~/types'

const { $dayjs } = useNuxtApp()
const { id } = useRoute().params
const forumStore = useForums()
const { forumThreads } = storeToRefs(forumStore)

const emit = defineEmits({
  'load-current-forum' () {
    return true
  }
})

const cachedResponse = ref<ForumThreadsApiResponse>()

useFetch(`/api/forums/${id}/threads`, {
  onResponse() {
    emit('load-current-forum')
  },
  transform(data: ForumThreadsApiResponse) {
    cachedResponse.value = data
    forumThreads.value = data.results
    return data
  }
})

function formatData(value: string) {
  return $dayjs(value).fromNow()
}
</script>
