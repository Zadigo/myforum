<template>
  <section class="threads">
    <div class="col-12 d-flex justify-content-between align-items-center my-3">
      <div class="flex justify-start align-center gap-2">
        <!-- Sorting -->
        <VoltButton id="sort" color="primary" variant="tonal">
          <font-awesome icon="sort" />
        </VoltButton>

        <v-menu activator="#sort">
          <v-list>
            <v-list-item v-for="(method, index) in sortMethods" :key="method.name" :value="index" @click="sortThreads(index)">
              <v-list-item-title>
                {{ method.name }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>

        <!-- Filtering -->
        <VoltButton id="filter">
          <font-awesome icon="filter" />
        </VoltButton>

        <v-menu activator="#filter">
          <v-list>
            <v-list-item v-for="(category, index) in categories" :key="category" :value="index">
              <v-list-item-title>
                {{ category }}
              </v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>

    <!-- Threads -->
    <Suspense>
      <AsyncThreadsIterator @load-current-forum="handleLoadForumInfo" />

      <template #fallback>
        Loading...
      </template>
    </Suspense>
  </section>
</template>

<script setup lang="ts">
import { sortMethods } from '~/data'

definePageMeta({
  layout: 'forum'
})

const AsyncThreadsIterator = defineAsyncComponent({
  loader: async () => import('~/components/threads/Iterator.vue')
})

const { id } = useRoute().params
const forumStore = useForums()
const { currentForum } = storeToRefs(forumStore)
const { sortThreads, categories } = useThreadsComposable()


const { data, execute } = useFetch(`/api/forums/${id}`, {
  immediate: false
})

if (data.value) {
  currentForum.value = data.value
}

/**
 *
 */
async function handleLoadForumInfo() {
  execute()
}
</script>
