<template>
  <article v-for="(thread, i) in forumThreads" :key="thread.id" :class="{ 'mt-1': i > 0 }" role="article" @click="forumStore.setCurrentThread(thread.id)">
    <NuxtLink :to="`/threads/${thread.id}`" :aria-label="thread.title" class="text-dark">
      <VoltCard class="card shadow-sm">
        <template #content>
          <div class="flex justify-start items-center gap-2 mb-4">
            <VoltAvatar image="/avatar1.png" shape="circle" />
            <h3 class="font-title font-bold">{{ thread.title }}</h3>
            <font-awesome v-if="thread.owned_by_user" icon="bolt-lightning" class="text-warning" />
          </div>

          <div v-if="thread.description" class="font-light my-2">
            {{ thread.description }}
          </div>

          <div class="space-x-3">
            <VoltTag><Icon name="fa-solid:comment" />{{ thread.number_of_comments }}</VoltTag>
            <VoltTag><Icon name="fa-solid:calendar" />{{ formatData(thread.created_on) }}</VoltTag>
            <!-- <span class="badge bg-light text-dark p-2 ms-2">{{ formatData(thread.latest_comment.created_on) }}</span> -->
          </div>
        </template>
      </VoltCard>
    </NuxtLink>
  </article>
</template>

<script setup lang="ts">
import type { SortMethodNames } from '~/data'
import type { ThreadApiResponse } from '~/types'

const { $dayjs } = useNuxtApp()
const { id } = useRoute().params
const forumStore = useForums()
const { forumThreads } = storeToRefs(forumStore)

const emit = defineEmits<{ 'load-current-forum': [] }>()

const sortingMethods = inject<Ref<SortMethodNames>>('sortingMethods', ref('Most recent'))

const { data: cachedResponse } = await useFetch<ThreadApiResponse>(`/api/forums/${id}/threads`, {
  method: 'GET',
  watch: [sortingMethods],
  query: {
    sort: sortingMethods.value
  }
})

if (cachedResponse.value) {
  console.log('cachedResponse', cachedResponse.value)
  forumThreads.value = cachedResponse.value.results
}

/**
 * Transforms a date to its human
 * readable version
 */
function formatData(value: string) {
  return $dayjs(value).fromNow()
}

onMounted(() => emit('load-current-forum'))
</script>
