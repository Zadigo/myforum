<template>
  <VoltCard v-for="comment in comments" :id="`post-${comment.id}`" :key="comment.id" class="mb-2 shadow-sm">
    <template v-if="showActions" #header>
      <div class="flex justify-between items-center">
        <span :aria-label="comment.title || ''">
          {{ comment.title }}
        </span>

        <!-- <v-btn v-if="authStore.isAuthenticated" variant="text" rounded>
          <icon icon="ellipsis-vertical" />

          <v-menu activator="parent">
            <v-list>
              <v-list-item>
                <v-list-item-title @click="emit('edit', comment)">
                  Edit
                </v-list-item-title>
              </v-list-item>

              <v-list-item @click="handleReport">
                <v-list-item-title>
                  Report
                </v-list-item-title>
              </v-list-item>

              <v-list-item @click="handleDeletion(comment)">
                <v-list-item-title>
                  Delete
                </v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </v-btn> -->
      </div>
    </template>

    <template #content>
      <div class="mb-4 space-x-1">
        <span class="font-bold text-surface-700">#{{ comment.id }}</span> 
        <span>-</span>
        <span class="font-bold text-blue-700 underline underline-offset-4">@{{ comment.user?.username }}</span> 
        <span>-</span>
        <span class="text-muted">{{ $dayjs(comment.created_on).fromNow() }}</span>
      </div>
      <div v-html="comment.content_html" />
    </template>

    <template v-if="showActions" #footer>
      <div v-if="authStore.isAuthenticated" class="d-flex gap-2">
        <VoltButton variant="tonal" @click="emit('reply', comment)">
          <icon name="i-lucide:reply" class="me-2" />Reply
        </VoltButton>

        <VoltButton variant="tonal" @click="handleQuoteFrom">
          <icon name="i-lucide:quote-left" class="me-2" />Quote from
        </VoltButton>
        
        <VoltButton variant="tonal" @click="handleBookmark(comment)">
          <icon v-if="comment.bookmarked_by_user" name="i-fa6:bookmark" class="me-2" />
          <icon v-else name="i-fa6:bookmark" class="me-2" />Bookmark
        </VoltButton>
        
        <VoltButton variant="tonal" @click="handleShare">
          <icon name="i-lucide:share" class="me-2" />Share
        </VoltButton>
      </div>

      <div v-else class="d-flex gap-2">
        <VoltButton variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:reply" class="me-2" />Reply
        </VoltButton>

        <VoltButton variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:quote-left" class="me-2" />Quote from
        </VoltButton>
        
        <VoltButton variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:bookmark" class="me-2" />Bookmark
        </VoltButton>
        
        <VoltButton variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:share" class="me-2" />Share
        </VoltButton>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

const emit = defineEmits({
  reply(_comment: UserComment) {
    return true
  },
  edit(_comment: UserComment) {
    return true
  }
})

defineProps<{
  comments: UserComment[],
  showActions: boolean
}>()

const { $dayjs } = useNuxtApp()
const authStore = useAuthentication()
const { customHandleError } = useErrorHandler()

const store = useForums()
const { $client } = useNuxtApp()

/**
 * Checks that the author of the comment
 * is from the current authenticated user 
 */
function isAuthor(comment: UserComment) {
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

/**
 *
 */
async function handleQuoteFrom () {
  // pass
}

/**
 *
 * @param comment 
 */
async function handleBookmark(comment: UserComment) {
  try {
    await $client.post(`comments/${comment.id}/bookmark`)
  } catch (e) {
    handleError(e)
  }
}

/**
 *
 */
async function handleShare () {
  // pass
}

/**
 *
 */
async function handleDeletion(comment: UserComment) {
  try {
    await $client.delete(`comments/${comment.id}`)
    const index = store.threadComments.findIndex(oldComment => oldComment.id === comment.id)
    store.threadComments.splice(index, 1)
  } catch (e) {
    handleError(e)
  }
}

/**
 *
 */
async function handleReport () {
  // pass 
}
</script>
