<template>
  <template v-if="cachedResponse && cachedResponse.errors">
    <div v-for="(error, i) in cachedResponse.errors" :key="i">
      {{ error }}
    </div>
  </template>

  <template v-else>
    <article v-for="(thread, i) in iteratedThreads" :key="thread.node.id" :class="{ 'mt-1': i > 0 }" role="article">
      {{ thread.node }}
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
              <volt-tag><Icon name="fa-solid:comment" />
                {{ thread.node.numberOfComments }}
              </volt-tag>

              <volt-tag><Icon name="fa-solid:calendar" />
                <nuxt-time :datetime="thread.node.createdOn" relative />
              </volt-tag>
              <!-- <span class="badge bg-light text-dark p-2 ms-2">{{ formatData(thread.latest_comment.created_on) }}</span> -->
            </div>
          </template>
        </volt-card>
      </nuxt-link-locale>
    </article>

    <dev-only>
      <dev-container>
        <pre class="bg-light p-3 rounded overflow-scroll h-50 w-full">
          {{ cachedResponse }}
        </pre>
      </dev-container>
    </dev-only>
  </template>
</template>

<script setup lang="ts">
import { SortMethods } from '~/types'
import type { MainThreads, RouteIdParamsGeneric, SortMethodNames } from '~/types'

const { id } = useRoute().params as RouteIdParamsGeneric

const sortingMethod = inject<Ref<SortMethodNames>>('sortingMethod',  ref(SortMethods.MostRecent))
  
const { data: cachedResponse } = await useFetch<MainThreads>(`/api/forums/${id}/threads`, {
  method: 'GET',
  watch: [sortingMethod],
  query: {
    sort: sortingMethod.value
  }
})

const iteratedThreads = computed(() => {
  if (isDefined(cachedResponse)) {
    if (isDefined(cachedResponse.value.data.forumThreads)) {
      return cachedResponse.value.data.forumThreads.edges
    }

    if (isDefined(cachedResponse.value.data.allMainThreads)) {
      return cachedResponse.value.data.allMainThreads.edges
    }
  }
  return []
})
</script>
