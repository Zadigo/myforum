<template>
  <div class="card shadow-sm">
    <div v-if="replyingToComment" class="card-header">
      Replying to <span class="fw-bold">@{{ replyingToComment.user.username }}</span>
    </div>

    <div class="card-body">
      <VoltInputText v-model="requestData.title" type="text" placeholder="Title" />

      <BaseEditor @editor-content="handleEditorContent" />

      <div v-for="quote in requestData.quotes" :key="quote" class="alert alert-info">
        {{ quote }}
      </div>
    </div>

    <div class="card-footer d-flex">
      <div class="ms-auto d-flex gap-2">
        <VoltButton rounded @click="createNewPost">
          Post
        </VoltButton>

        <VoltButton @click="saveDraft">
          Save draft
        </VoltButton>
        
        <VoltButton @click="emit('close')">
          Cancel
        </VoltButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Comment, EditorData } from '~/types';
import BaseEditor from '../BaseEditor.vue';

interface RequestData {
  thread: string | number
  title: string
  content: string
  content_delta: object | null
  content_html: string
  quotes: number[]
}

const emit = defineEmits({
  close () {
    return true
  },
  created() {
    return true
  }
})

const { id } = useRoute().params

const requestData = ref<RequestData>({
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
