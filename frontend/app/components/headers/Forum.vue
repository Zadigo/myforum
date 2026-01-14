<template>
  <base-page-header class="bg-primary-100 dark:bg-primary-900 dark:text-primary-50 mt-5">
    <template #title>
      <client-only>
        <template #default>
          <h1 v-if="currentForum">
            {{ currentForum.data.forum.title }}
          </h1>
          <volt-skeleton v-else height="2rem" />
        </template>

        <template #fallback>
          <volt-skeleton height="2rem" />
        </template>
      </client-only>
    </template>

    <template #breadcrumbs>
      <volt-breadcrumb v-if="currentForum" :home="{ icon: 'i-lucide:home', route: '/forums' }" :model="breadcrumbs" />
      <volt-skeleton v-else height="2rem" width="15rem" />
    </template>

    <template #actions>
      <div class="space-x-2">
        <volt-button @click="handleFollowForum">
          <icon name="i-lucide:circle-plus" />
          Follow forum
        </volt-button>

        <volt-contrast-button>
          <icon name="i-lucide:stars" />

          <nuxt-link-locale :to="`/threads/${currentForum?.data.forum.id}/create`" @click="handleNewThread">
            New thread
          </nuxt-link-locale>
        </volt-contrast-button>
      </div>
    </template>
  </base-page-header>
</template>

<script setup lang="ts">
import type { MenuItem } from 'primevue/menuitem'
import type { BaseForum, Undefineable } from '~/types'

const emit = defineEmits<{ 'follow': [forum: Undefineable<BaseForum>] }>()

const { currentForum } = await useForumComposable()

const breadcrumbs = ref<MenuItem[]>([
  {
    label: 'Forums',
    url: '/forums'
  },
  {
    label: currentForum.value?.data?.forum.title,
    disabled: true
  }
])

async function handleFollowForum() {
  emit('follow', currentForum.value?.data?.forum)
}

async function handleNewThread() {}
</script>
