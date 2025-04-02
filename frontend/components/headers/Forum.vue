<template>
  <BasePageHeader class="bg-blue-50">
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
      <div class="btn-group shadow-none">
        <button type="button" class="btn btn-lg btn-info btn-sm" @click="handleFollowForum">
          <Icon name="fa-solid:plus-circle" class="me-1" />
          Follow forum
        </button>

        <NuxtLink to="/threads/1/create" class="btn btn-lg btn-primary btn-sm" @click="handleNewThread">
          New thread
        </NuxtLink>
      </div>
    </template>
  </BasePageHeader>
</template>

<script setup lang="ts">
import type { Forum } from '~/types';

const emit = defineEmits({
  follow (_data: Forum | undefined) {
    return true
  }
})

const forumStore = useForums()
const { currentForum } = storeToRefs(forumStore)

async function handleFollowForum() {
  emit('follow', currentForum)
}
async function handleNewThread() {}
</script>
