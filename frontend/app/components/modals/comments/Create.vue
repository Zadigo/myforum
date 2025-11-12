<template>
  <volt-dialog v-model:visible="createCommentModal" class="md:w-[700px]" :dismissable-mask="false" modal>
    <volt-input-text placeholder="Title" />
    <base-editor />
  </volt-dialog>
</template>

<script setup lang="ts">
const createCommentModal = useState<boolean>('createCommentModal')
</script>
