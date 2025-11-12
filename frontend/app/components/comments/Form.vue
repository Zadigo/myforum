<template>
  <volt-card class="shadow-sm">
    <template v-if="replyingToComment" #header>
      Replying to <span class="font-bold">@{{ replyingToComment.user.username }}</span>
    </template>

    <template #content>
      <!-- <volt-input-text v-model="newComment.title" type="text" placeholder="Title" /> -->

      <base-editor @editor-content="handleEditorContent" />

      <!-- <div v-for="quote in newComment.quotes" :key="quote" class="alert alert-info">
        {{ quote }}
      </div> -->
    </template>

    <template #footer>
      <div class="space-x-2">
        <volt-button @click="createNewPost">
          <icon name="i-lucide:check" />
          Post
        </volt-button>

        <volt-button @click="saveDraft">
          <icon name="i-lucide:drafting-compass" />
          Save draft
        </volt-button>
        
        <volt-button @click="$emit('close')">
          Cancel
        </volt-button>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import type { Delta } from '@vueup/vue-quill'
import type { Arrayable, EditorData, RouteIdParamsGeneric, Undefineableable, UserComment } from '~/types'

interface NewComment {
  thread: string | number
  title: string
  content: string
  content_delta: Undefineableable<string | Delta>
  content_html: string
  quotes: Arrayable<number>
}

const emit = defineEmits<{ close: [], created: [] }>()

const { id } = useRoute().params as RouteIdParamsGeneric

const newComment = ref<NewComment>({
  thread: id,
  title: '',
  content: '',
  content_delta: undefined,
  content_html: '',
  quotes: []
})

const replyingToComment = inject<Undefineableable<UserComment>>('replyingToComment', undefined)
const { customHandleError } = useErrorHandler()

const { $nuxtAuthentication } = useNuxtApp()

// Create a new comment
async function createNewPost () {
  try {
    await $nuxtAuthentication('/v1/comments/create', { method: 'POST', body: newComment.value })
    emit('created')
  } catch (e) {
    console.log(e)
    customHandleError(e)
  }
}

//
async function saveDraft () {
  try {
    await $nuxtAuthentication('/v1/comments/create', { method: 'POST', body: newComment.value })
    emit('created')
  } catch (e) {
    console.log(e)
    customHandleError(e)
  }
}

//
function handleEditorContent (data: EditorData) {
  newComment.value.content = data.text
  newComment.value.content_html = data.html
  newComment.value.content_delta = data.delta
}
</script>
