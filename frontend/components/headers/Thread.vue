<template>
  <BasePageHeader class="bg-red-100">
    <template #title>
      {{ forumStore.currentThread?.title }}
    </template>

    <template #breadcrumbs>
      <li class="breadcrumb-item">
        <NuxtLink to="/forums/1">
          {{ forumStore.currentThread?.forum.title }}
        </NuxtLink>
      </li>

      <li class="breadcrumb-item active" aria-current="page">
        {{ forumStore.currentThread?.title }}
      </li>
    </template>

    <template #actions>
      <div class="space-x-2">
        <VoltButton type="button" rounded @click="emit('jump-to-latest')">
          <Icon name="fa-solid:arrow-down" />
          Jump to latest
        </VoltButton>
        
        <VoltButton type="button" rounded @click="emit('follow')">
          <Icon name="fa-solid:plus-circle" />
          Follow thread
        </VoltButton>
        
        <VoltButton type="button" rounded @click="emit('delete')">
          <Icon name="fa-solid:trash" />
          Delete
        </VoltButton>
        
        <VoltButton type="button" rounded @click="forumStore.showCreateCommentForm=true">
          <Icon name="fa-solid:plus" />
          New comment
        </VoltButton>
      </div>
    </template>
  </BasePageHeader>
</template>

<script setup lang="ts">
import { useStorage } from '@vueuse/core'
import type { CustomRouteIdParamsGeneric, Forum, ForumThread } from '~/types'

const { id } = useRoute().params as CustomRouteIdParamsGeneric
const forumStore = useForums()

const cachedForums = useStorage<Forum[]>('forums', [])
const cachedThreads = useStorage<ForumThread[]>('threads', [])

const emit = defineEmits<{
  'jump-to-latest': [],
  'follow': [],
  'delete': [],
  'new-comment': [],
}>()

const userCreatedThread = computed(() => {
  return false
  // if (!this.user) {
  //   return false
  // }
  // return this.currentThread.user.id === this.user.id
})

onBeforeMount(() => {
  if (cachedForums.value) {
    forumStore.currentForum = cachedForums.value.find(forum => forum.id === parseInt(id))
  }

  if (cachedThreads.value) {
    forumStore.currentThread = cachedThreads.value.find(thread => thread.id === parseInt(id))
  }
})
</script>
