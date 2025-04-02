<template>
  <BasePageHeader class="bg-red-100">
    <template #title>
      {{ forumStore.currentThread?.title }}
    </template>

    <template #breadcrumbs>
      <li class="breadcrumb-item">
        <NuxtLink to="/forums/1">
          {{ forumStore.currentForum?.title }}
        </NuxtLink>
      </li>

      <li class="breadcrumb-item active" aria-current="page">
        {{ forumStore.currentThread?.title }}
      </li>
    </template>

    <template #actions>
      <div class="btn-group shadow-none">
        <button type="button" class="btn btn-lg btn-info btn-sm" @click="emit('jump-to-latest')">
          Jump to latest
        </button>
        
        <button type="button" class="btn btn-lg btn-info btn-sm" @click="emit('follow')">
          Follow thread
        </button>
        
        <button type="button" class="btn btn-lg btn-danger btn-sm" @click="emit('delete')">
          Delete
        </button>
        
        <button type="button" class="btn btn-lg btn-primary btn-sm" @click="forumStore.showCreateCommentForm=true">
          New comment
        </button>
      </div>
    </template>
  </BasePageHeader>
</template>

<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import type { Forum, ForumThread } from '~/types';

const { id } = useRoute().params
const forumStore = useForums()
const route = useRoute()

const cachedForums = useSessionStorage<Forum[]>('forums', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

const cachedThreads = useSessionStorage<ForumThread[]>('threads', null, {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})

const emit = defineEmits({
  'jump-to-latest' () {
    return true
  },
  'follow' () {
    return true
  },
  'delete' () {
    return true
  },
  'new-comment' () {
    return true
  }
})

onBeforeMount(() => {
  if (cachedForums.value) {
    forumStore.currentForum = cachedForums.value.find(forum => forum.id === parseInt(id))
  }

  if (cachedThreads.value) {
    forumStore.currentThread = cachedThreads.value.find(thread => thread.id === parseInt(id))
  }
})

const userCreatedThread = computed(() => {
  return false
  // if (!this.user) {
  //   return false
  // }
  // return this.currentThread.user.id === this.user.id
})
</script>
