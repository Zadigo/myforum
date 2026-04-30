<template>
  <section id="search" class="my-5">
    <div class="mb-3">
      <volt-tabs v-model:value="currentPill">
        <volt-tab-list>
          <volt-tab v-for="link in links" :key="link.name" :value="link.name" as="div" class="nav-item">
            {{ link.name }}
          </volt-tab>
        </volt-tab-list>
      </volt-tabs>
    </div>
    
    <div>
      <!-- Comments -->
      <comments-iterator v-if="searchResult" :comments="searchResult.comments" />
    </div>
  </section>
</template>

<script setup lang="ts">
import type { RouteIdParamsGeneric, SearchApiResponse } from '~/types'

definePageMeta({
  title: 'Search Results',
  layout: 'design'
})

type Pill = 'Comments' | 'Showcase' | 'Albums' | 'Media' | 'Tags' | string
type Pills = { name: Pill, active: boolean }

const links: Pills[] = [
  {
    name: 'Comments',
    active: true
  },
  {
    name: 'Showcase',
    active: false
  },
  {
    name: 'Albums',
    active: false
  },
  {
    name: 'Media',
    active: false
  },
  {
    name: 'Tags',
    active: false
  }
]

const config = useRuntimeConfig()
// const { customHandleError } = useErrorHandler()
const searchResult = ref<SearchApiResponse>()

const { q } = useRoute().params as RouteIdParamsGeneric

const currentPill = ref<Pill>('Comments')

/**
 *
 */
async function getSearch() {
  // try {
  //   const response = await $client.post<SearchApiResponse>('/search', {
  //     q: route.query.q
  //   })
  //   searchResult.value = response.data
  // } catch(e) {
  //   handleError(e)
  // }
  return await $fetch<SearchApiResponse>('/search', {
    baseURL: config.public.prodDomain,
    method: 'POST',
    body: {
      q
    }
  })
}

watchDebounced<string>(() => q, async (newValue, oldValue) => {
  console.log(newValue, oldValue)
  if (newValue !== oldValue) {
    await getSearch()
  }
}, {
  deep: true,
  debounce: 3000
})

onBeforeMount(getSearch)
</script>
