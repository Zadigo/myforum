<template>
  <article v-for="category in forumCategories" :key="category" :aria-label="category" class="mb-5">
    <div class="mb-2">
      <h3 class="font-bold text-2xl font-title">
        {{ category }}
      </h3>
    </div>

    <article v-for="(forum, i) in forumsByCategory[category]" :key="forum.id">
      <VoltCard :class="{ 'mt-1': i > 0 }" :aria-label="forum.title" class="shadow-sm" role="article">
        <template #content>
          <NuxtLinkLocale :to="`/forums/${forum.id}`">
            <h4 :aria-label="forum.title" class="font-bold">
              {{ forum.title }}
            </h4>

            <p class="font-light my-2">
              {{ forum.description }}
            </p>

            <div id="infos" class="space-x-3 mt-5">
              <VoltTag>
                {{ forum.number_of_threads }} <icon icon="users" />
              </VoltTag>

              <VoltTag>
                200000 <icon icon="eye" />
              </VoltTag>

              <VoltTag>
                {{ $dayjs(forum.created_on).fromNow() }}
              </VoltTag>
            </div>
          </NuxtLinkLocale>
        </template>
      </VoltCard>
    </article>
  </article>
</template>

<script setup lang="ts">
import type { Forum } from '~/types'

const { forumsList, forumCategories, forumsByCategory } = storeToRefs(useForums())

const { data } = await useFetch<Forum[]>('/api/forums', { method: 'GET' })

if (data.value) {
  forumsList.value = data.value
}
</script>
