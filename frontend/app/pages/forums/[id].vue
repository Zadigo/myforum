<template>
  <section class="threads">
    <div class="flex justify-between items-center my-3">
      <client-only>
        <volt-dropdown  id="sort-threads" :items="sortMethods">
          <template #default="{ attrs }">
            <volt-button @click="attrs.toggle">
              <icon name="i-fa-solid:sort" />
              {{ sortingMethod }}
            </volt-button>
          </template>
        </volt-dropdown>
      </client-only>

      <client-only>
        <!-- Filtering -->
        <volt-button id="filter">
          <icon name="i-fa-solid:filter" />
        </volt-button>
      </client-only>
    </div>

    <!-- Threads -->
    <suspense>
      <async-threads-iterator />

      <template #fallback>
        <volt-skeleton height="5rem" />
      </template>
    </suspense>
  </section>
</template>

<script setup lang="ts">
import type { SortMenuItem, SortMethodNames } from '~/types'

definePageMeta({
  name: 'Forum Threads',
  layout: 'forum'
})

const asyncThreadsIterator = defineAsyncComponent({
  loader: async () => import('~/components/threads/Iterator.vue')
})

const sortingMethod = ref<SortMethodNames>('Most recent')
provide('sortingMethod', sortingMethod)

const query = useUrlSearchParams('history') as { ordering: SortMethodNames }
const sortMethods: SortMenuItem[] = [
  {
    label: 'Sort alphabetically A-Z',
    command(event) {
      sortingMethod.value = event.item.label as SortMethodNames
      query.ordering = event.item.label as SortMethodNames
    }
  },
  {
    label: 'Sort alphabetically Z-A',
    command(event) {
      sortingMethod.value = event.item.label as SortMethodNames
      query.ordering = event.item.label as SortMethodNames
    }
  },
  {
    label: 'Most recent',
    command(event) {
      sortingMethod.value = event.item.label as SortMethodNames
      query.ordering = event.item.label as SortMethodNames
    },
  },
  {
    label: 'Number of comments',
    command(event) {
      sortingMethod.value = event.item.label as SortMethodNames
      query.ordering = event.item.label as SortMethodNames
    }
  }
]
</script>
