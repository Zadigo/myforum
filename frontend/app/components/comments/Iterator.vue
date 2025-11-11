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
        <span class="font-bold text-surface-200">#{{ comment.id }}</span> 
        <span>-</span>
        <span class="font-bold text-primary-700 underline underline-offset-4">@{{ comment.user?.username }}</span> 
        <span>-</span>
        <client-only>
          <span class="text-muted">{{ $dayjs(comment.created_on).fromNow() }}</span>
        </client-only>
      </div>

      <div v-html="comment.content_html" />
    </template>

    <template v-if="showActions" #footer>
      <div v-if="authStore.isAuthenticated" class="flex gap-2">
        <volt-button variant="tonal" @click="emit('reply', comment)">
          <icon name="i-lucide:reply" class="me-2" />Reply
        </volt-button>

        <volt-button variant="tonal" @click="handleQuoteFrom">
          <icon name="i-lucide:quote-left" class="me-2" />Quote from
        </volt-button>
        
        <volt-button variant="tonal" @click="handleBookmark(comment)">
          <icon v-if="comment.bookmarked_by_user" name="i-fa6:bookmark" class="me-2" />
          <icon v-else name="i-fa6:bookmark" class="me-2" />Bookmark
        </volt-button>
        
        <volt-button variant="tonal" @click="handleShare">
          <icon name="i-lucide:share" class="me-2" />Share
        </volt-button>
      </div>

      <div v-else class="flex gap-2">
        <volt-button variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:reply" class="me-2" />Reply
        </volt-button>

        <volt-button variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:quote-left" class="me-2" />Quote from
        </volt-button>
        
        <volt-button variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:bookmark" class="me-2" />Bookmark
        </volt-button>
        
        <volt-button variant="tonal" @click="authStore.openLoginModal=true">
          <icon name="i-lucide:share" class="me-2" />Share
        </volt-button>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

defineProps<{ comments: UserComment[], showActions: boolean }>()
const emit = defineEmits<{ reply: [comment: UserComment], edit: [comment: UserComment] }>()


const { $dayjs, $nuxtAuthentication } = useNuxtApp()
const authStore = useAuthentication()
const { customHandleError } = useErrorHandler()

const store = useForums()

// Checks that the author of the comment
// is from the current authenticated user 
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

//
async function handleQuoteFrom () {
  // pass
}

//
async function handleBookmark(comment: UserComment) {
  try {
    await $nuxtAuthentication(`comments/${comment.id}/bookmark`, {
      method: 'POST'
    })
  } catch (e) {
    customHandleError(e)
  }
}

//
async function handleShare () {
  // pass
}

//
async function handleDeletion(comment: UserComment) {
  try {
    await $nuxtAuthentication(`comments/${comment.id}`, { method: 'DELETE' })
    store.threadComments = store.threadComments.filter(c => c.id !== comment.id)
  } catch (e) {
    customHandleError(e)
  }
}
</script>
