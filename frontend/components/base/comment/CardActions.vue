<template>
  <div v-if="authStore.isAuthenticated" class="flex justify-end gap-2 mt-8">
    <v-btn color="primary" variant="tonal" @click="emit('reply', comment)">
      <font-awesome icon="reply" class="me-2" />Reply
    </v-btn>

    <v-btn color="primary" variant="tonal" @click="handleQuoteFrom">
      <font-awesome icon="quote-left" class="me-2" />Quote from
    </v-btn>
    
    <v-btn color="primary" variant="tonal" @click="handleBookmark(comment)">
      <font-awesome v-if="comment.bookmarked_by_user" :icon="['fas', 'bookmark']" class="me-2" />
      <font-awesome v-else :icon="['far', 'bookmark']" class="me-2" />Bookmark
    </v-btn>
    
    <v-btn color="primary" variant="tonal" @click="handleShare">
      <font-awesome icon="share" class="me-2" />Share
    </v-btn>
  </div>

  <div v-else class="d-flex gap-2">
    <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal=true">
      <font-awesome icon="reply" class="me-2" />Reply
    </v-btn>

    <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal=true">
      <font-awesome icon="quote-left" class="me-2" />Quote from
    </v-btn>
    
    <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal=true">
      <font-awesome icon="bookmark" class="me-2" />Bookmark
    </v-btn>
    
    <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal=true">
      <font-awesome icon="share" class="me-2" />Share
    </v-btn>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';

const authStore = useAuthentication()

defineProps({
  comment: {
    type: Object as PropType<Comment>,
    required: true
  }
})

const emit = defineEmits({
  reply(_comment: Comment) {
    return true
  }
})

async function handleQuoteFrom () {
  // pass
}

async function handleBookmark (comment: Comment) {
  // try {
  //   await $client.post(`comments/${comment.id}/bookmark`)
  // } catch (e) {
  //   handleError(e)
  // }
}

async function handleShare () {
  // pass
}

async function handleDeletion (comment: Comment) {
  // try {
  //   await $client.delete(`comments/${comment.id}`)
  //   const index = store.threadComments.findIndex(oldComment => oldComment.id === comment.id)
  //   store.threadComments.splice(index, 1)
  // } catch (e) {
  //   handleError(e)
  // }
}

async function handleReport () {
  // pass 
}
</script>
