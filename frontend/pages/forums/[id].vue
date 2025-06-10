<template>
  <section class="threads">
    <div class="col-12 d-flex justify-content-between align-items-center my-3">
      <div class="flex justify-start align-center gap-2">
        <!-- Sorting -->
        <!-- <VoltButton id="sort" color="primary" variant="tonal">
          <font-awesome icon="sort" />
        </VoltButton>

        <v-menu activator="#sort">
          <v-list>
            <v-list-item v-for="(method, index) in sortMethods" :key="method.label" :value="index" @click="sortThreads(index)">
              <v-list-item-title>
                {{ method.label }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu> -->

        <ClientOnly>
          <VoltDropButton  id="sort-threads" :items="sortMethods" />
        </ClientOnly>
        
        <!-- Filtering -->
        <VoltButton id="filter">
          <font-awesome icon="filter" />
        </VoltButton>

        <!-- <v-menu activator="#filter">
          <v-list>
            <v-list-item v-for="(category, index) in categories" :key="category" :value="index">
              <v-list-item-title>
                {{ category }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu> -->
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
import { sortMethods } from '~/data'
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
const { sortThreads, categories } = useThreadsComposable()


const { data, execute } = useFetch<Forum>(`/api/forums/${id}`, {
  immediate: false,
  method: 'GET'
})


/**
 *
 */
const handleLoadForumInfo = useDebounceFn(async () => {
  await execute()
  
  console.log('Forum', data.value)
  if (data.value) {
    currentForum.value = data.value
  }
}, 3000)
</script>
