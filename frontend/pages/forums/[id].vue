<template>
  <section class="threads">
    <div class="flex justify-between items-center my-3">
      <div class="flex justify-start align-center gap-2">
        <ClientOnly>
          <VoltDropButton  id="sort-threads" v-model="sortingMethod" :items="sortMethods">
            <Icon name="i-fa-solid:sort" />
          </VoltDropButton>

          {{ sortingMethod }}

          <!-- Filtering -->
          <VoltButton id="filter">
            <Icon name="i-fa-solid:filter" />
          </VoltButton>
        </ClientOnly>
      </div>
    </div>

    <!-- Threads -->
    <Suspense>
      <AsyncThreadsIterator @load-current-forum="handleLoadForumInfo" />

      <template #fallback>
        <VoltSkeleton height="5rem" />
      </template>
    </Suspense>
  </section>
</template>

<script setup lang="ts">
import { sortMethods, type SortMethodNames } from '~/data'
import type { CustomRouteIdParamsGeneric, Forum } from '~/types'

definePageMeta({
  layout: 'forum'
})

const AsyncThreadsIterator = defineAsyncComponent({
  loader: async () => import('~/components/threads/Iterator.vue')
})

const forumStore = useForums()
const { currentForum } = storeToRefs(forumStore)

const { id } = useRoute().params as CustomRouteIdParamsGeneric

/**
 * Fetches the forum information based on the ID from the route
 */
const { data, execute } = useFetch<Forum>(`/api/forums/${id}`, {
  immediate: false,
  method: 'GET'
})

/**
 * Load information of the current forum once the threads are loaded
 */
const handleLoadForumInfo = useDebounceFn(async () => {
  await execute()
  
  console.log('Forum', data.value)

  if (data.value) {
    currentForum.value = data.value
  }
}, 1000)

/**
 * Sorting methods for threads
 */

const sortingMethod = ref<SortMethodNames>('Most recent')

provide('sortingMethod', sortingMethod)
</script>
