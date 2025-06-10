<template>
  <VoltCard class="shadow-sm">
    <template #content>
      <div id="infos" class="flex justify-between align-center">
        <div class="flex items-center gap-2">
          <span class="fw-semibold text-muted">#{{ comment.id }}</span>
          <Icon name="fa-solid:star-of-life" />
          <span class="font-bold">{{ comment.user.username }}</span>
        </div>

        <VoltDropButton id="something" :items="[{ label: 'Google' }]" />

        <v-btn v-if="authStore.isAuthenticated" color="dark" variant="text" rounded>
          <font-awesome icon="ellipsis-vertical" />

          <v-menu activator="parent">
            <v-list>
              <v-list-item>
                <v-list-item-title @click="handleEdit">
                  Edit
                </v-list-item-title>
              </v-list-item>

              <v-list-item @click="handleReport">
                <v-list-item-title>
                  Report
                </v-list-item-title>
              </v-list-item>

              <v-list-item @click="handleDeletion">
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
      <BaseCommentCardActions :comment="comment" @reply="handleReply" />
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import type { Comment } from '~/types'

const props = defineProps<{ comment: Comment }>()

const emit = defineEmits({
  reply(_comment: Comment) {
    return true
  }
})

const authStore = useAuthentication()

/**
 *
 */
function handleEdit() {

}

/**
 *
 */
function handleReply() {
  emit('reply', props.comment)
}

/**
 *
 */
async function handleReport() {

}

/**
 *
 */
async function handleDeletion() {

}
</script>
