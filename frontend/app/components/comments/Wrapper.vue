<template>
  <article v-for="(comment, i) in comments" :key="comment.id" :class="{ 'mt-6': i >= 1 }" :aria-label="comment.title || `Comment from ${comment.user.username}`">
    <base-comment-card :comment="comment" @reply="handleReply" />
    
    <div id="replies" class="w-full flex justify-end mt-6">
      <div class="w-5/6">
        <volt-card v-for="x in 3" :key="x" class="shadow-sm mt-1">
          <template #content>
            Reply {{ x }}
          </template>
        </volt-card>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
import type { UserComment } from '~/types'
import type { PropType } from 'vue'

const emit = defineEmits({
  reply(_comment: UserComment) {
    return true
  },
  edit(_comment: UserComment) {
    return true
  }
})

defineProps({
  comments: {
    type: Array as PropType<UserComment[]>,
    required: true
  },
  showActions: {
    type: Boolean,
    default: true
  }
})

// const { $dayjs } = useNuxtApp()
// const authStore = useAuthentication()
// const { customHandleError } = useErrorHandler()
// const store = useForums()
// const { $client } = useNuxtApp()

// /**
//  * Checks that the author of the comment
//  * is from the current authenticated user 
//  */
// function isAuthor(comment: UserComment) {
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

/**
 *
 * @param comment The comment for which the reply is to
 */
function handleReply(comment: UserComment) {
  emit('reply', comment)
}
</script>
