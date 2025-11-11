<template>
  <div id="latest-comments">
    <article v-for="category in forumCategories" :key="category" class="mb-5">
      <div class="mb-2">
        <h3 class="font-bold text-2xl">
          {{ category }}
        </h3>
      </div>
  
      <article v-for="(forum, i) in forumsByCategory[category]" :key="forum.id">
        <volt-card :class="{ 'mt-1': i > 0 }" :aria-label="forum.title" class="shadow-sm" role="article">
          <template #content>
            <NuxtLinkLocale :to="`/forums/${forum.id}`">
              <h4 class="font-bold">
                {{ forum.title }}
              </h4>
  
              <p class="font-light my-2">
                {{ forum.description }}
              </p>
  
              <div id="infos" class="space-x-3 mt-5">
                <volt-tag>
                  {{ forum.number_of_threads }} <icon name="i-lucide:users" />
                </volt-tag>
  
                <volt-tag>
                  200000 <icon name="i-lucide:eye" />
                </volt-tag>
  
                <volt-tag>
                  {{ $dayjs(forum.created_on).fromNow() }}
                </volt-tag>
              </div>
            </NuxtLinkLocale>
          </template>
        </volt-card>
      </article>
    </article>
  </div>
</template>

<script setup lang="ts">
import type { Forum } from '~/types'

const { forumsList, forumCategories, forumsByCategory } = storeToRefs(useForums())

const { data } = await useFetch<Forum[]>('/api/forums', { method: 'GET' })

if (data.value) {
  forumsList.value = data.value
}
</script>
