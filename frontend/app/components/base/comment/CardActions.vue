<template>
  <div v-if="isAuthenticated" class="flex justify-end gap-2 mt-8">
    <volt-secondary-button color="primary" variant="text" @click="handleReply">
      <icon name="i-lucide:reply" class="me-2" />Reply
    </volt-secondary-button>

    <volt-secondary-button color="primary" variant="text" @click="handleQuoteFrom">
      <icon name="i-lucide:quote" class="me-2" />Quote from
    </volt-secondary-button>
    
    <volt-secondary-button color="primary" variant="text" @click="handleBookmark">
      <icon v-if="comment.bookmarked_by_user" name="i-lucide:bookmark" class="me-2" />
      <icon v-else name="i-lucide:bookmark" class="me-2" />Bookmark
    </volt-secondary-button>
    
    <volt-secondary-button color="primary" variant="text" @click="handleShare">
      <icon name="i-lucide:share" class="me-2" />Share
    </volt-secondary-button>
  </div>

  <div v-else class="flex justify-end gap-2 mt-8">
    <volt-secondary-button color="dark" variant="text" @click="loginModal=true">
      <icon name="i-lucide:reply" class="me-2" />Reply
    </volt-secondary-button>

    <volt-secondary-button color="dark" variant="text" @click="loginModal=true">
      <icon name="i-lucide:quote" class="me-2" />Quote from
    </volt-secondary-button>
    
    <volt-secondary-button color="dark" variant="text" @click="loginModal=true">
      <icon name="i-lucide:bookmark" class="me-2" />Bookmark
    </volt-secondary-button>
    
    <volt-secondary-button color="dark" variant="text" @click="loginModal=true">
      <icon name="i-lucide:share" class="me-2" />Share
    </volt-secondary-button>
  </div>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

const loginModal = useState('loginModal')
const { isAuthenticated } = useUser()

const props = defineProps<{ comment: UserComment }>()
const emit = defineEmits<{
  reply: [comment: UserComment],
  quote: [commentId: number],
  bookmark: [commentId: number],
  share: [commentId: number]
}>()

//
async function handleQuoteFrom() {
  emit('quote', props.comment.id)
}

//
async function handleBookmark() {
  emit('bookmark', props.comment.id)
}

const { share, isSupported } = useShare()

//
function handleShare() {
  if (!isSupported) {
    alert('Sharing is not supported in your browser.')
    return
  }

  share({
    title: props.comment.title || `Comment from ${props.comment.user.username}`,
    text: props.comment.content,
    url: window.location.href + `#comment-${props.comment.id}`
  })
}

//
async function handleReply() {
  emit('reply', props.comment)
}
</script>
