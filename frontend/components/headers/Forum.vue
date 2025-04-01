<template>
  <BasePageHeader>
    <template #title>
      <span v-if="currentForum">
        {{ currentForum.title }}
      </span>
      <span v-else>
        Loading...
      </span>
    </template>

    <template #breadcrumbs>
      <li v-if="currentForum" class="breadcrumb-item active" aria-current="page">
        {{ currentForum.title }}
      </li>
      <li v-else class="breadcrumb-item active" aria-current="page">
        Loading...
      </li>
    </template>

    <template #actions>
      <div class="btn-group">
        <button type="button" class="btn btn-lg btn-info" @click="emit('follow', currentForum)">
          Follow forum
        </button>

        <NuxtLink to="/threads/1/create" class="btn btn-lg btn-primary">
          New thread
        </NuxtLink>
      </div>
    </template>
  </BasePageHeader>
</template>

<script setup lang="ts">
import { useSessionStorage } from '@vueuse/core';
import type { Forum } from '~/types';

const emit = defineEmits({
  follow (_data: Forum | undefined) {
    return true
  }
})

const forumStore = useForums()
const route = useRoute();

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

const currentForum = computed((): Forum | undefined => {
  if (cachedForums.value) {
    return cachedForums.value.find(item => item.id === parseInt(route.params.id))
  } else {
    return undefined
  }
})
</script>
