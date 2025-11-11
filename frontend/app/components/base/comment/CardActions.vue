<template>
  <div v-if="authStore.isAuthenticated" class="flex justify-end gap-2 mt-8">
    <VoltSecondaryButton color="primary" variant="text" @click="handleReply">
      <icon name="i-lucide:reply" class="me-2" />Reply
    </VoltSecondaryButton>

    <VoltSecondaryButton color="primary" variant="text" @click="handleQuoteFrom">
      <icon name="i-lucide:quote-left" class="me-2" />Quote from
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="primary" variant="text" @click="handleBookmark">
      <icon v-if="comment.bookmarked_by_user" name="i-fa6:bookmark" class="me-2" />
      <icon v-else name="[-fa6:bookmark" class="me-2" />Bookmark
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="primary" variant="text" @click="handleShare">
      <icon name="i-lucide:share" class="me-2" />Share
    </VoltSecondaryButton>
  </div>

  <div v-else class="flex justify-end gap-2 mt-8">
    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:reply" class="me-2" />Reply
    </VoltSecondaryButton>

    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:quote-left" class="me-2" />Quote from
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:bookmark" class="me-2" />Bookmark
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:share" class="me-2" />Share
    </VoltSecondaryButton>
  </div>
</template>

<script setup lang="ts">
import { VoltSecondaryButton } from '#components'

const authStore = useAuthentication()

const props = defineProps<{ comment: Comment }>()

const emit = defineEmits({
  reply(_comment: Comment) {
    return true
  }
})

/**
 * 
 */
async function handleQuoteFrom() {

}

/**
 * 
 */
async function handleBookmark() {
  // try {
  //   await $client.post(`comments/${comment.id}/bookmark`)
  // } catch (e) {
  //   handleError(e)
  // }
}

/**
 * 
 */
function handleShare() {

}

/**
 * 
 */
async function handleReply() {
  emit('reply', props.comment)
}
</script>
