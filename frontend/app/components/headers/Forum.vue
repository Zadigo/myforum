<template>
  <base-page-header class="bg-primary-100 mt-5">
    <template #title>
      <client-only>
        <h1 v-if="currentForum">
          {{ currentForum.title }}
        </h1>

        <volt-skeleton v-else height="2rem" />
      </client-only>
    </template>

    <template #breadcrumbs>
      <volt-breadcrumb :home="{ icon: 'i-lucide:home', route: '/forums' }" :model="breadcrumbs" />
    </template>

    <template #actions>
      <div class="space-x-2">
        <volt-button @click="handleFollowForum">
          <icon name="i-lucide:circle-plus" />
          Follow forum
        </volt-button>

        <volt-contrast-button>
          <icon name="i-lucide:stars" />
          <NuxtLink to="/threads/1/create" @click="handleNewThread">
            New thread
          </NuxtLink>
        </volt-contrast-button>
      </div>
    </template>
  </base-page-header>
</template>

<script setup lang="ts">
import type { Forum } from '~/types'

const emit = defineEmits<{ 'follow': [forum: Forum] }>()

const forumStore = useForums()
const { currentForum } = storeToRefs(forumStore)

const breadcrumbs = ref([
  {
    label: currentForum.value?.title
  }
])

/**
 * Function to handle the follow forum action
 */
async function handleFollowForum() {
  if (currentForum.value !== undefined) {
    emit('follow', currentForum.value)
  }
}

/**
 *
 */
async function handleNewThread() {}
</script>
