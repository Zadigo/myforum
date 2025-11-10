<template>
  <div v-if="authStore.isAuthenticated" class="flex justify-end gap-2 mt-8">
    <VoltSecondaryButton color="primary" variant="text" @click="handleReply">
      <font-awesome icon="reply" class="me-2" />Reply
    </VoltSecondaryButton>

    <VoltSecondaryButton color="primary" variant="text" @click="handleQuoteFrom">
      <font-awesome icon="quote-left" class="me-2" />Quote from
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="primary" variant="text" @click="handleBookmark">
      <font-awesome v-if="comment.bookmarked_by_user" :icon="['fas', 'bookmark']" class="me-2" />
      <font-awesome v-else :icon="['far', 'bookmark']" class="me-2" />Bookmark
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="primary" variant="text" @click="handleShare">
      <font-awesome icon="share" class="me-2" />Share
    </VoltSecondaryButton>
  </div>

  <div v-else class="flex justify-end gap-2 mt-8">
    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <font-awesome icon="reply" class="me-2" />Reply
    </VoltSecondaryButton>

    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <font-awesome icon="quote-left" class="me-2" />Quote from
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <font-awesome icon="bookmark" class="me-2" />Bookmark
    </VoltSecondaryButton>
    
    <VoltSecondaryButton color="dark" variant="text" @click="authStore.openLoginModal=true">
      <font-awesome icon="share" class="me-2" />Share
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
