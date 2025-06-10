<template>
  <div>
    <article v-for="(thread, i) in forumThreads" :key="thread.id" :class="{ 'mt-1': i > 0 }" role="article" @click="forumStore.setCurrentThread(thread.id)">
      <NuxtLink :to="`/threads/${thread.id}`" :aria-label="thread.title" class="text-dark">
        <VoltCard class="card shadow-sm">
          <template #content>
            <div class="flex justify-start items-center gap-2 mb-4">
              <VoltAvatar image="https://via.placeholder.com/200x200" shape="cirlce" />
              <h3 class="card-title m-0 h4">{{ thread.title }}</h3>
              <font-awesome v-if="thread.owned_by_user" icon="bolt-lightning" class="text-warning" />
            </div>

            <div v-if="thread.description" class="font-light my-2">
              {{ thread.description }}
            </div>

            <div class="space-x-3">
              <VoltTag><Icon icon="fa-solid:comment" />{{ thread.number_of_comments }}</VoltTag>
              <VoltTag><Icon icon="fa-solid:calendar" />{{ formatData(thread.created_on) }}</VoltTag>
              <!-- <span class="badge bg-light text-dark p-2 ms-2">{{ formatData(thread.latest_comment.created_on) }}</span> -->
            </div>
          </template>
        </VoltCard>
      </NuxtLink>
    </article>
  </div>
</template>

<script setup lang="ts">
import type  { ThreadApiResponse } from '~/types'

const { $dayjs } = useNuxtApp()
const { id } = useRoute().params
const forumStore = useForums()
const { forumThreads } = storeToRefs(forumStore)

const emit = defineEmits<{ 'load-current-forum': [] }>()

const { status, data: cachedResponse } = useFetch<ThreadApiResponse>(`/api/forums/${id}/threads`)

if (cachedResponse.value) {
  forumThreads.value = cachedResponse.value.results
}

watch(status, (value) => {
  if (value === 'success') {
    emit('load-current-forum')
  }
})

/**
 * Transforms a date to its human
 * readable version
 */
function formatData(value: string) {
  return $dayjs(value).fromNow()
}
</script>
