<template>
  <BasePageHeader class="bg-blue-50">
    <template #title>
      <span v-if="currentForum">
        {{ currentForum.title }}
      </span>

      <VoltSkeleton v-else height="2rem" />
    </template>

    <template #breadcrumbs>
      <VoltBreadcrumb :home="{ icon: 'pi pi-home' }" :items="breadcrumbs" />
    </template>

    <template #actions>
      <div class="space-x-2">
        <VoltButton @click="handleFollowForum">
          <Icon name="fa-solid:plus-circle" />
          Follow forum
        </VoltButton>

        <VoltButton>
          <NuxtLink to="/threads/1/create" @click="handleNewThread">
            New thread
          </NuxtLink>
        </VoltButton>
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

const breadcrumbs = ref([
  {
    label: currentForum.value?.title
  }
])

/**
 *
 */
async function handleFollowForum() {
  emit('follow', currentForum)
}

/**
 *
 */
async function handleNewThread() {}
</script>
