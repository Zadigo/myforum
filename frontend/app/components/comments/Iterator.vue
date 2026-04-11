<template>
  <volt-card v-for="comment in iteratedComments" :id="`post-${comment.node.id}`" :key="comment.node.id" class="mb-2 shadow-sm">
    <template v-if="showActions" #header>
      <div class="flex justify-between items-center">
        <span>
          {{ comment.node.title }}
        </span>

        <volt-dropdown v-if="isAuthenticated" id="actions" :items="menuItems">
          <template #default="{ attrs }">
            <volt-button @click="attrs.toggle">
              <icon name="lucide:ellipsis-vertical" />
            </volt-button>
          </template>
        </volt-dropdown>
      </div>
    </template>

    <template #content>
      <div class="mb-4 space-x-1">
        <span class="font-bold text-surface-200">#{{ comment.node.id }}</span>
        <span>-</span>
        <span class="font-bold text-primary-700 underline underline-offset-4">@{{ comment.node.user.username }}</span>
        <span>-</span>
        <span class="text-muted">
          <nuxt-time :datetime="comment.node.createdOn" relative />
        </span>
      </div>

      <div v-html="comment.node.contentHtml" />
    </template>

    <template v-if="showActions" #footer>
      <div v-if="isAuthenticated" class="flex gap-2">
        <volt-button variant="tonal" @click="$emit('reply', comment)">
          <icon name="i-lucide:reply" class="me-2" />Reply
        </volt-button>

        <volt-button variant="tonal" @click="handleQuoteFrom">
          <icon name="i-lucide:quote" class="me-2" />Quote from
        </volt-button>

        <volt-button variant="tonal" @click="handleBookmark(comment)">
          <icon v-if="comment.node.bookmarkedByUser" name="i-lucide:bookmark" class="me-2" />
          <icon v-else name="i-lucide:bookmark" class="me-2" />Bookmark
        </volt-button>

        <volt-button variant="tonal" @click="handleShare(comment)">
          <icon name="i-lucide:share" class="me-2" />Share
        </volt-button>
      </div>

      <div v-else class="flex gap-2">
        <volt-button variant="tonal" @click="loginModal=true">
          <icon name="i-lucide:reply" class="me-2" />Reply
        </volt-button>

        <volt-button variant="tonal" @click="loginModal=true">
          <icon name="i-lucide:quote" class="me-2" />Quote from
        </volt-button>

        <volt-button variant="tonal" @click="loginModal=true">
          <icon name="i-lucide:bookmark" class="me-2" />Bookmark
        </volt-button>

        <volt-button variant="tonal" @click="loginModal=true">
          <icon name="i-lucide:share" class="me-2" />Share
        </volt-button>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import type { MenuItem } from 'primevue/menuitem'
import type { LatestCommentNode, LatestComments, UserCommentNode, UserComments } from '~/types'

const { showActions = true, comments } = defineProps<{ 
  comments: UserComments | LatestComments, 
  showActions?: boolean
}>()

defineEmits<{ 
  reply: [comment: UserCommentNode], 
  edit: [comment: UserCommentNode | LatestCommentNode]
}>()

const iteratedComments = computed(() => {
  if ('commentsForThread' in comments.data) {
    return comments.data.commentsForThread.edges
  } else if ('latestComments' in comments.data) {
    return comments.data.latestComments.edges
  } else {
    return []
  }
})

/**
 * Handlers
 */

const { userId, isAuthenticated } = useUser<{ id: number }>()

// Checks that the author of the comment
// is from the current authenticated user 
const checkIsAuthor = reactify((comment: UserCommentNode) => {
  if (!isAuthenticated) return false
  return isAuthenticated && comment.node.user.id === parseInt(userId.value)
})

//
async function handleQuoteFrom () {
  // pass
}

//
async function handleBookmark(_comment: UserCommentNode | LatestCommentNode) {
  // try {
  //   await $nuxtAuthentication(`comments/${comment.node.id}/bookmark`, {
  //     method: 'POST'
  //   })
  // } catch (e) {
  //   // customHandleError(e)
  // }
}

//
async function handleShare (_comment: UserCommentNode | LatestCommentNode) {
  // pass
}

//
async function handleDeletion(_comment: UserCommentNode | LatestCommentNode) {
  // try {
  //   await $nuxtAuthentication(`comments/${comment.node.id}`, { method: 'DELETE' })
  //   store.threadComments = store.threadComments.filter(c => c.id !== comment.node.id)
  // } catch (e) {
  //   // customHandleError(e)
  // }
}

/**
 * Menu Items
 */

const menuItems = ref<MenuItem[]>([
  {
    Label: 'Report',
    command: (_event) => {
      // emit report event
    }
  },
  {
    label: 'Edit',
    command: (_event) => {
      // emit edit event
    }
  },
  {
    label: 'Delete',
    command: (_event) => {
      // handleDeletion()
    }
  }
])

/**
 * Modals
 */

const loginModal = useState<boolean>('loginModal')
</script>
