<template>
  <article v-for="(thread, i) in cachedResponse?.data.allMainThreads.edges" :key="thread.node.id" :class="{ 'mt-1': i > 0 }" role="article">
    <nuxt-link-locale :to="`/threads/${thread.node.id}`" class="text-dark">
      <volt-card class="card shadow-sm">
        <template #content>
          <div class="flex justify-start items-center gap-2 mb-4">
            <volt-avatar image="/avatar1.png" shape="circle" />
            <h3 class="font-title font-bold">{{ thread.node.title }}</h3>
            <icon v-if="thread.node.ownedByUser" name="i-lucide:bolt-lightning" class="text-warning" />
          </div>

          <div v-if="thread.node.description" class="font-light my-2">
            {{ thread.node.description }}
          </div>

          <div class="space-x-3">
            <volt-tag><Icon name="fa-solid:comment" />{{ thread.node.numberOfComments }}</volt-tag>
            <volt-tag><Icon name="fa-solid:calendar" />{{ formatData(thread.node.createdOn) }}</volt-tag>
            <!-- <span class="badge bg-light text-dark p-2 ms-2">{{ formatData(thread.latest_comment.created_on) }}</span> -->
          </div>
        </template>
      </volt-card>
    </nuxt-link-locale>
  </article>
</template>

<script setup lang="ts">
import type { SortMethodNames } from '~/data'
import type { MainThreads, RouteIdParamsGeneric } from '~/types'

const { id } = useRoute().params as RouteIdParamsGeneric

const sortingMethod = inject<Ref<SortMethodNames>>('sortingMethod')
  
const { data: cachedResponse } = await useFetch<MainThreads>(`/api/forums/${id}/threads`, {
  method: 'GET',
  watch: [sortingMethod],
  query: {
    sort: sortingMethod.value
  }
})
  
const { $dayjs } = useNuxtApp()

// Transforms a date to its  readable version
function formatData(value: string) {
  return $dayjs(value).fromNow()
}
</script>
