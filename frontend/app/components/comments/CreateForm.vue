<template>
  <volt-card class="shadow-sm">
    <template v-if="replyingToComment" #header>
      Replying to <span class="font-bold">@{{ replyingToComment.user.username }}</span>
    </template>

    <template #content>
      <!-- <volt-input-text v-model="newComment.title" type="text" placeholder="Title" /> -->

      <base-editor @editor-content="writeEditorContent" />

      <!-- <div v-for="quote in newComment.quotes" :key="quote" class="alert alert-info">
        {{ quote }}
      </div> -->
    </template>

    <template #footer>
      <div class="space-x-2">
        <volt-button @click="async () => await create(() => $emit('created'))">
          <icon name="i-lucide:check" />
          Post
        </volt-button>

        <volt-button @click="async () => await saveDraft(() => $emit('created'))">
          <icon name="i-lucide:drafting-compass" />
          Save draft
        </volt-button>
        
        <volt-button @click="$emit('close')">
          Cancel
        </volt-button>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import type { EditorData, Undefineableable, UserComment } from '~/types'

defineEmits<{ close: [], created: [] }>()


const replyingToComment = inject<Undefineableable<UserComment>>('replyingToComment', undefined)

/**
 * Create comment composable
 */
 
const { create, saveDraft, writeEditorContent } = useCreateCommentComposable()
</script>
