<template>
  <div v-if="comments" id="comments">
    <!-- TODO: :class="{ 'bg-light mb-5': comment.initial_comment }" -->
    <article v-for="comment in comments" :id="`post-${comment.id}`" :key="comment.id" class="card shadow-sm mb-2">
      <div v-if="showActions" class="card-toolbar border-bottom">
        <div class="card-toolbar-content d-flex justify-content-between align-items-center">
          <span :aria-label="comment.title || ''">
            {{ comment.title }}
          </span>

          <v-btn v-if="authStore.isAuthenticated" color="dark" variant="text" rounded>
            <font-awesome icon="ellipsis-vertical" />

            <v-menu activator="parent">
              <v-list>
                <v-list-item>
                  <!-- <font-awesome-icon :icon="['fas', 'bookmark']" /> -->
                  <v-list-item-title @click="emit('edit', comment)">
                    Edit
                  </v-list-item-title>
                </v-list-item>

                <v-list-item @click="handleReport">
                  <!-- <font-awesome-icon :icon="['fas', 'bookmark']" /> -->
                  <v-list-item-title>
                    Report
                  </v-list-item-title>
                </v-list-item>

                <v-list-item @click="handleDeletion(comment)">
                  <!-- <font-awesome-icon :icon="['fas', 'bookmark']" /> -->
                  <v-list-item-title>
                    Delete
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-btn>
        </div>
      </div>

      <div class="card-body">
        <div class="mb-4">
          <span class="fw-bold text-muted">#{{ comment.id }}</span> 
          <span class="mx-2">-</span> by <span class="fw-bold">{{ comment.user?.username }}</span> 
          <span class="text-muted">{{ $dayjs(comment.created_on).fromNow() }}</span>
        </div>
        <div v-html="comment.content_html" />
      </div>

      <div v-if="showActions" class="card-footer ms-auto ">
        <div v-if="authStore.isAuthenticated" class="d-flex gap-2">
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
      </div>
    </article>
  </div>

  <div v-else>
    No comments
  </div>
</template>

<script setup lang="ts">
import type { Comment } from '~/types'
import type { PropType } from 'vue'



const emit = defineEmits({
  reply (_comment: Comment) {
    return true
  },
  edit (_comment: Comment) {
    return true
  }
})

defineProps({
  comments: {
    type: Array as PropType<Comment[] | undefined>,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  }
})

const { $dayjs } = useNuxtApp()
const authStore = useAuthentication()
const { handleError } = useErrorHandler()

function useCommentActions() {
  const store = useForums()
  const { $client } = useNuxtApp()

  /**
   * Checks that the author of the comment
   * is from the current authenticated user 
   */
  function isAuthor(comment: Comment) {
    if (!authStore.isAuthenticated) {
      return false
    } else {
      if (!authStore.userProfile) {
        return false
      } else {
        if (comment.user.id === authStore.userProfile.id) {
          return true
        }
      }
    }
  }

  async function handleQuoteFrom () {
    // pass
  }
  
  async function handleBookmark (comment: Comment) {
    try {
      await $client.post(`comments/${comment.id}/bookmark`)
    } catch (e) {
      handleError(e)
    }
  }
  
  async function handleShare () {
    // pass
  }
  
  async function handleDeletion (comment: Comment) {
    try {
      await $client.delete(`comments/${comment.id}`)
      const index = store.threadComments.findIndex(oldComment => oldComment.id === comment.id)
      store.threadComments.splice(index, 1)
    } catch (e) {
      handleError(e)
    }
  }
  
  async function handleReport () {
    // pass 
  }

  return {
    isAuthor,
    handleQuoteFrom,
    handleBookmark,
    handleShare,
    handleDeletion,
    handleReport
  }
}

const { handleQuoteFrom, handleDeletion, handleReport, handleShare, handleBookmark } = useCommentActions()
</script>

<style lang="scss" scoped>
.card-toolbar {
  contain: layout;
  display: block;
  flex: 1 1 auto;
  max-width: 100%;
  transition: transform .2s cubic-bezier(.4, 0, .2, 1), background-color .2s cubic-bezier(.4, 0, .2, 1), left .2s cubic-bezier(.4, 0, .2, 1), right .2s cubic-bezier(.4, 0, .2, 1), box-shadow .28s cubic-bezier(.4, 0, .2, 1), max-width .25s cubic-bezier(.4, 0, .2, 1), width .25s cubic-bezier(.4, 0, .2, 1);
  position: relative;
  /* background-color: #fff; */
  border-top-left-radius: .5rem;
  border-top-right-radius: .5rem;
  /* box-shadow: 0 10px 15px -3px rgb(0 0 0 / 7%), 0 4px 6px -2px rgb(0 0 0 / 5%); */
}

.card-toolbar .card-toolbar-content {
  padding: 4px 16px;
  height: 64px;
}

.btn-icon {
  color: rgba(0, 0, 0, .54);
  min-height: 0;
  min-width: 0;
  padding: 0;
  /* box-shadow: none; */
  height: 48px;
  width: 48px;
}
</style>
