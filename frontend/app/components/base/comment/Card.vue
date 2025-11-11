<template>
  <VoltCard class="shadow-sm">
    <template #content>
      <div id="infos" class="flex justify-between align-center">
        <div class="flex items-center gap-2">
          <span class="fw-semibold text-muted">#{{ comment.id }}</span>
          <Icon name="fa-solid:star-of-life" />
          <span class="font-bold">{{ comment.user.username }}</span>
        </div>

        <VoltDropButton id="something" :items="actions">
          <template #button="{ toggle }">
            <VoltSecondaryButton rounded @click="toggle">
              <Icon name="fa-solid:ellipsis-vertical" />
            </VoltSecondaryButton>
          </template>
        </VoltDropButton>
      </div>

      <!-- Content -->
      <div class="bg-gray-50 p-3 rounded-sm mt-6" v-html="comment.content_html" />

      <!-- Actions -->
      <BaseCommentCardActions :comment="comment" @reply="handleReply" />
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

const props = defineProps<{ comment: UserComment }>()

const emit = defineEmits({
  reply(_comment: UserComment) {
    return true
  }
})

const actions = [
  { label: 'Edit' },
  { label: 'Report' },
  { label: 'Delete' }
]

const authStore = useAuthentication()

/**
 *
 */
function handleEdit() {

}

/**
 *
 */
function handleReply() {
  emit('reply', props.comment)
}

/**
 *
 */
async function handleReport() {

}

/**
 *
 */
async function handleDeletion() {

}
</script>
