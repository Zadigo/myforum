<template>
  <base-page-header class="bg-secondary-200">
    <template #title>
      {{ forumStore.currentThread?.title }}
    </template>

    <template #breadcrumbs>
      <volt-breadcrumb :model="breadcrumbs" />
    </template>

    <template #actions>
      <div class="space-x-2">
        <volt-secondary-button rounded @click="emit('jump-to-latest')">
          <Icon name="fa-solid:arrow-down" />
          Jump to latest
        </volt-secondary-button>
        
        <volt-button rounded @click="emit('follow')">
          <Icon name="fa-solid:plus-circle" />
          Follow thread
        </volt-button>
        
        <VoltDangerButton rounded @click="emit('delete')">
          <Icon name="fa-solid:trash" />
          Delete
        </VoltDangerButton>
        
        <volt-button rounded @click="forumStore.showCreateCommentForm=true">
          <Icon name="fa-solid:plus" />
          New comment
        </volt-button>
      </div>
    </template>
  </base-page-header>
</template>

<script setup lang="ts">
import type { CustomRouteIdParamsGeneric } from '~/types'

const { id } = useRoute().params as CustomRouteIdParamsGeneric


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
  
const forumStore = useForums()

const breadcrumbs = computed(() => {
  return [
    {
      label: `${forumStore.currentThread?.forum.title}`,
      route: '/forums',
    },
    {
      label: `${forumStore.currentThread?.title}`,
      route: `/forums/thread/${id}`,
    }
  ]
})
</script>
