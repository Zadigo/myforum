<template>
  <volt-card class="shadow-sm">
    <template v-if="replyingToComment" #header>
      Replying to <span class="fw-bold">@{{ replyingToComment.user.username }}</span>
    </template>

    <template #content>
      <!-- <volt-input-text v-model="requestData.title" type="text" placeholder="Title" /> -->

      <base-editor @editor-content="handleEditorContent" />

      <!-- <div v-for="quote in requestData.quotes" :key="quote" class="alert alert-info">
        {{ quote }}
      </div> -->
    </template>

    <template #footer>
      <div class="space-x-2">
        <volt-button @click="createNewPost">
          <Icon name="fa-solid:check" />
          Post
        </volt-button>

        <volt-button @click="saveDraft">
          <Icon name="fa-solid:drafting-compass" />
          Save draft
        </volt-button>
        
        <volt-button @click="emit('close')">
          Cancel
        </volt-button>
      </div>
    </template>
  </volt-card>
</template>

<script setup lang="ts">
import type { Delta } from '@vueup/vue-quill'
import type { UserComment, CustomRouteIdParamsGeneric, EditorData, Undefineableable, Arrayable } from '~/types'

interface NewComment {
  thread: string | number
  title: string
  content: string
  content_delta: Undefineableable<string | Delta>
  content_html: string
  quotes: Arrayable<number>
}

const emit = defineEmits<{ close: [], created: [] }>()

const { id } = useRoute().params as CustomRouteIdParamsGeneric

const requestData = ref<NewComment>({
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

//
async function createNewPost () {
  try {
    $nuxtAuthentication('/v1/comments/create', {
      method: 'POST',
      body: requestData.value
    })
    emit('created')
  } catch (e) {
    customHandleError(e)
  }
}

//
async function saveDraft () {}

//
function handleEditorContent (data: EditorData) {
  requestData.value.content = data.text
  requestData.value.content_html = data.html
  requestData.value.content_delta = data.delta
}
</script>
