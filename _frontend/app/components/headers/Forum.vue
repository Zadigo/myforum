<template>
  <BasePageHeader class="bg-primary-200">
    <template #title>
      <ClientOnly>
        <h1 v-if="currentForum">
          {{ currentForum.title }}
        </h1>

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

        <VoltSecondaryButton>
          <Icon name="i-fa-solid:plus" />
          <NuxtLink to="/threads/1/create" @click="handleNewThread">
            New thread
          </NuxtLink>
        </VoltSecondaryButton>
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
