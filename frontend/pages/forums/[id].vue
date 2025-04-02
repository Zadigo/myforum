<template>
  <section class="threads">
    <div class="row">
      <div class="col-12 d-flex justify-content-between align-items-center my-3">
        <div class="d-flex justify-content-start align-items-center gap-2" style="width: 200px;">
          <!-- Sorting -->
          <v-btn id="sort" color="primary" variant="tonal">
            <font-awesome icon="sort" />
          </v-btn>

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
          <v-btn id="filter" color="primary" variant="tonal">
            <font-awesome icon="filter" />
          </v-btn>

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

        <!-- Pagination -->
        <!-- <BasePagination :pagination="currentPage" /> -->
        Pagination
      </div>

      <!-- Threads -->
      <Suspense>
        <AsyncThreadsIterator @load-current-forum="handleLoadForumInfo" />

        <template #fallback>
          Loading...
        </template>
      </Suspense>
    </div>
  </section>
</template>

<script setup lang="ts">
import { sortMethods } from '~/data'

const AsyncThreadsIterator = defineAsyncComponent({
  loader: async () => import('~/components/threads/Iterator.vue')
})

const { id } = useRoute().params
const forumStore = useForums()
const { currentForum } = storeToRefs(forumStore)
const { sortThreads, categories } = useThreadsComposable()


const { data, execute } = useFetch(`/api/forums/${id}/infos`, {
  immediate: false
})

async function handleLoadForumInfo() {
  execute()
  currentForum.value = data.value
}
</script>
