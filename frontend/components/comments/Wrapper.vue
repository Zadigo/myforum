<template>
  <article v-for="(comment, i) in comments" :key="comment.id" :class="{ 'mt-6': i >= 1 }" :aria-label="comment.title || `Comment from ${comment.user.username}`">
    <BaseCommentCard :comment="comment" @reply="handleReply" />
    
    <div id="replies" class="w-full flex justify-end mt-6">
      <div class="w-5/6">
        <!-- <p class="my-1 text-right">Replies</p> -->
        <div v-for="x in 3" :key="x" class="card shadow-sm mt-1">
          <div class="card-body">
            Reply {{ x }}
          </div>
        </div>
      </div>
    </div>
  </article>
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
    type: Array as PropType<Comment[]>,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  }
})

// const { $dayjs } = useNuxtApp()
// const authStore = useAuthentication()
// const { handleError } = useErrorHandler()
// const store = useForums()
// const { $client } = useNuxtApp()

// /**
//  * Checks that the author of the comment
//  * is from the current authenticated user 
//  */
// function isAuthor(comment: Comment) {
//   if (!authStore.isAuthenticated) {
//     return false
//   } else {
//     if (!authStore.userProfile) {
//       return false
//     } else {
//       if (comment.user.id === authStore.userProfile.id) {
//         return true
//       }
//     }
//   }
// }

function handleReply(comment: Comment) {
  emit('reply', comment)
}
</script>
