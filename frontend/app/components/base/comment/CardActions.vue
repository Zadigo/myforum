<template>
  <div v-if="authStore.isAuthenticated" class="flex justify-end gap-2 mt-8">
    <volt-secondary-button color="primary" variant="text" @click="handleReply">
      <icon name="i-lucide:reply" class="me-2" />Reply
    </volt-secondary-button>

    <volt-secondary-button color="primary" variant="text" @click="handleQuoteFrom">
      <icon name="i-lucide:quote-left" class="me-2" />Quote from
    </volt-secondary-button>
    
    <volt-secondary-button color="primary" variant="text" @click="handleBookmark">
      <icon v-if="comment.bookmarked_by_user" name="i-fa6:bookmark" class="me-2" />
      <icon v-else name="[-fa6:bookmark" class="me-2" />Bookmark
    </volt-secondary-button>
    
    <volt-secondary-button color="primary" variant="text" @click="handleShare">
      <icon name="i-lucide:share" class="me-2" />Share
    </volt-secondary-button>
  </div>

  <div v-else class="flex justify-end gap-2 mt-8">
    <volt-secondary-button color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:reply" class="me-2" />Reply
    </volt-secondary-button>

    <volt-secondary-button color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:quote" class="me-2" />Quote from
    </volt-secondary-button>
    
    <volt-secondary-button color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:bookmark" class="me-2" />Bookmark
    </volt-secondary-button>
    
    <volt-secondary-button color="dark" variant="text" @click="authStore.openLoginModal=true">
      <icon name="i-lucide:share" class="me-2" />Share
    </volt-secondary-button>
  </div>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'

const authStore = useAuthentication()

const props = defineProps<{ comment: UserComment }>()
const emit = defineEmits<{ reply: [comment: UserComment]}>()

//
async function handleQuoteFrom() {}

//
async function handleBookmark() {}

//
function handleShare() {}

//
async function handleReply() {
  emit('reply', props.comment)
}
</script>
