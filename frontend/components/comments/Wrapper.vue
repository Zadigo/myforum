<template>
  <article v-for="(comment, i) in comments" :key="comment.id" :class="{ 'mt-6': i >= 1 }" :aria-label="comment.title || `Comment from ${comment.user.username}`">
    <div class="card shadow-sm">
      <div class="card-body">
        <div id="infos" class="flex justify-between align-center">
          <div class="flex items-center gap-2">
            <span class="fw-semibold text-muted">#{{ comment.id }}</span>
            <Icon name="fa-solid:star-of-life" />
            <span class="font-bold">{{ comment.user.username }}</span>
          </div>

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
                  <Icon name="fa-solid:exclamation-circle" />
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

        <!-- Content -->
        <div class="bg-gray-50 p-3 rounded-sm mt-6" v-html="comment.content_html" />

        <!-- Actions -->
        <BaseCommentCardActions :comment="comment" />
      </div>
    </div>
    
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

const authStore = useAuthentication()
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

async function handleReport() {

}

async function handleDeletion(comment: Comment) {

}
</script>
