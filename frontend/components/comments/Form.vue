<template>
  <div class="row">
    <div class="col-12">
      <div class="card">
        <div v-if="replyingToComment" class="card-header">
          Replying to <span class="fw-bold">@{{ replyingToComment.user.username }}</span>
        </div>

        <div class="card-body">
          <v-text-field v-model="requestData.title" type="text" placeholder="Title" variant="solo-filled" flat />

          <BaseEditor @editor-content="handleEditorContent" />

          <div v-for="quote in requestData.quotes" :key="quote" class="alert alert-info">
            {{ quote }}
          </div>
        </div>

        <div class="card-footer d-flex">
          <div class="ms-auto d-flex gap-2">
            <v-btn color="primary" variant="tonal" rounded @click="createNewPost">
              Post
            </v-btn>

            <v-btn color="info" variant="tonal" rounded @click="saveDraft">
              Save draft
            </v-btn>
            
            <v-btn color="info" variant="tonal" rounded @click="emit('close')">
              Cancel
            </v-btn>
          </div>
        </div>
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

const route = useRoute()

const requestData = ref<RequestData>({
  thread: route.params.id,
  title: '',
  content: '',
  content_delta: {},
  content_html: '',
  quotes: []
})

const replyingToComment = inject<Comment>('replyingToComment')
const { handleError } = useErrorHandler()
const { $client } = useNuxtApp()

async function createNewPost () {
  try {
    $client.post('/comments/create', requestData.value)
    emit('created')
  } catch (e) {
    handleError(e)
  }
}

async function saveDraft () {}

function handleEditorContent (data: EditorData) {
  requestData.value.content = data.text
  requestData.value.content_html = data.html
  requestData.value.content_delta = data.delta
}
</script>
