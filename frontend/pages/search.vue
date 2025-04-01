<template>
  <section id="search" class="my-5">
    <div class="container">
      <div class="row">
        <div class="col-12 mb-3">
          <ul class="nav nav-pills">
            <li v-for="link in links" :key="link.name" class="nav-item">
              <a :class="{ active: currentPill === link.name }" href="#" class="nav-link" aria-current="page" @click.prevent="currentPill=link.name">
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>
        
        <div class="col-sm-12 col-md-9">
          <!-- Comments -->
          <CommentsIterator v-if="searchResult" :comments="searchResult.comments" />
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import type { SearchApiResponse } from '~/types';

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

const { $client } = useNuxtApp()
const { handleError } = useErrorHandler()
const searchResult = ref<SearchApiResponse>()
const route = useRoute()

const currentPill = ref<Pill>('Comments')

async function getSearch() {
  try {
    const response = await $client.post<SearchApiResponse>('/search', {
      q: route.query.q
    })
    searchResult.value = response.data
  } catch(e) {
    handleError(e)
  }
} 

onBeforeMount(getSearch)

watch<string>(route.query.q, async (newValue, oldValue) => {
  console.log(newValue, oldValue)
  if (newValue !== oldValue) {
    await getSearch()
  }
}, {
  deep: true
})
</script>
