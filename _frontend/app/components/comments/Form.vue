<template>
  <VoltCard class="shadow-sm">
    <template v-if="replyingToComment" #header>
      Replying to <span class="fw-bold">@{{ replyingToComment.user.username }}</span>
    </template>

    <template #content>
      <VoltInputText v-model="requestData.title" type="text" placeholder="Title" />

      <BaseEditor @editor-content="handleEditorContent" />

      <div v-for="quote in requestData.quotes" :key="quote" class="alert alert-info">
        {{ quote }}
      </div>
    </template>

    <template #footer>
      <div class="space-x-2">
        <VoltButton @click="createNewPost">
          <Icon name="fa-solid:check" />
          Post
        </VoltButton>

        <VoltButton @click="saveDraft">
          <Icon name="fa-solid:drafting-compass" />
          Save draft
        </VoltButton>
        
        <VoltButton @click="emit('close')">
          Cancel
        </VoltButton>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import type { Comment, CustomRouteIdParamsGeneric, EditorData } from '~/types'

interface NewComment {
  thread: string | number
  title: string
  content: string
  content_delta: object | null
  content_html: string
  quotes: number[]
}
const emit = defineEmits<{ close: [], created: [] }>()

const { id } = useRoute().params as CustomRouteIdParamsGeneric

const requestData = ref<NewComment>({
  thread: id,
  title: '',
  content: '',
  content_delta: {},
  content_html: '',
  quotes: []
})

const replyingToComment = inject<Comment>('replyingToComment')
const { handleError } = useErrorHandler()

const access = useCookie('access')
const refresh = useCookie('refresh')
const { authenticatedClient: client } = useAuthenticatedAxiosClient(access.value, refresh.value)

/**
 * 
 */
async function createNewPost () {
  try {
    client.post('v1/comments/create', requestData.value)
    emit('created')
  } catch (e) {
    handleError(e)
  }
}

/**
 * 
 */
async function saveDraft () {}

/**
 *
 * @param data
 */
function handleEditorContent (data: EditorData) {
  requestData.value.content = data.text
  requestData.value.content_html = data.html
  requestData.value.content_delta = data.delta
}
</script>
