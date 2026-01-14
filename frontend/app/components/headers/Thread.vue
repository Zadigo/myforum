<template>
  <base-page-header class="bg-secondary-200 dark:bg-primary-900 dark:text-primary-50">
    <template #title>
      {{ currentThread?.data.mainThread.title }}
    </template>

    <template #breadcrumbs>
      <volt-breadcrumb :model="breadcrumbs" />
    </template>

    <template #actions>
      <div class="space-x-2">
        <volt-secondary-button rounded @click="emit('jump-to-latest')">
          <icon name="i-lucide:arrow-down" />
          Jump to latest
        </volt-secondary-button>
        
        <volt-button rounded @click="emit('follow')">
          <icon name="i-lucide:plus-circle" />
          Follow thread
        </volt-button>

        <volt-danger-button rounded @click="emit('delete')">
          <icon name="i-lucide:trash" />
          Delete
        </volt-danger-button>

        <volt-button rounded @click="() => { togglecreateCommentModal() }">
          <icon name="i-lucide:plus" />
          New comment
        </volt-button>
      </div>
    </template>
  </base-page-header>
</template>

<script setup lang="ts">
import type { RouteIdParamsGeneric } from '~/types'

const emit = defineEmits<{
  'jump-to-latest': [],
  'follow': [],
  'delete': [],
  'new-comment': [],
}>()

/**
 * Modal
 */

const createCommentModal = useState<boolean>('createCommentModal')
const togglecreateCommentModal = useToggle(createCommentModal)
  
/**
 * Breadcrumbs
 */

const { currentThread } = await useCurrentThreadComposable()

console.log('Current Thread in Header:', currentThread)
  
const { id } = useRoute().params as RouteIdParamsGeneric
const breadcrumbs = computed(() => {
  return [
    {
      label: `${currentThread.value?.data.mainThread.forum.title}`,
      url: '/forums',
    },
    {
      label: `${currentThread.value?.data.mainThread.title}`,
      url: `/forums/thread/${id}`,
    }
  ]
})
</script>
