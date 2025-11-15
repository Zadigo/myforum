<template>
  <volt-dialog v-model:visible="createCommentModal" class="md:w-[700px]" :dismissable-mask="false" modal>
    <volt-input-text placeholder="Title" />
    <base-editor @editor-content="writeEditorContent" />

    <template #footer>
      <volt-secondary-button @click="createCommentModal = false">
        Close
      </volt-secondary-button>

      <volt-button @click="async () => await create(() => createCommentModal = false)">
        <icon name="i-lucide:check" />
        Post comment
      </volt-button>
    </template>
  </volt-dialog>
</template>

<script setup lang="ts">
const createCommentModal = useState<boolean>('createCommentModal')

/**
 * Create comment composable
 */

const { create, writeEditorContent } = useCreateCommentComposable()
</script>
