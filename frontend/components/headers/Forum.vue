<template>
  <BasePageHeader class="bg-blue-50">
    <template #title>
      <ClientOnly>
        <span v-if="currentForum">
          {{ currentForum.title }}
        </span>

        <VoltSkeleton v-else height="2rem" />
      </ClientOnly>
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
