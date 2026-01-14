<template>
  <volt-card class="shadow-sm">
    <template #content>
      <div id="infos" class="flex justify-between align-center">
        <div class="flex items-center gap-2">
          <span class="fw-semibold text-muted">#{{ comment.node.id }}</span>
          <icon name="fa-solid:star-of-life" />
          <span class="font-bold">{{ comment.node.user.username }}</span>
        </div>

        <volt-dropdown id="something" :items="actions">
          <template #button="{ toggle }">
            <volt-secondary-button rounded @click="toggle">
              <icon name="fa-solid:ellipsis-vertical" />
            </volt-secondary-button>
          </template>
        </volt-dropdown>
      </div>

      <!-- Content -->
      <div class="bg-gray-50 dark:bg-primary-800 p-3 rounded-sm mt-6" v-html="comment.node.contentHtml" />

      <!-- Actions -->
      <base-comment-card-actions :comment="comment" @reply="handleReply" />
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import type { UserCommentNode } from '~/types'

const props = defineProps<{ comment: UserCommentNode }>()
const emit = defineEmits<{ reply: [comment: UserCommentNode] }>()

const actions = [
  { label: 'Edit' },
  { label: 'Report' },
  { label: 'Delete' }
]

//
function handleEdit() {}

//
function handleReply() {
  emit('reply', props.comment)
}

//
async function handleReport() {}

//
async function handleDeletion() {}
</script>
