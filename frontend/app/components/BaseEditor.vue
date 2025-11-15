<template>
  <div id="editor-wrapper" class="my-3">
    <client-only>
      <template #default>
        <quill-editor ref="editorEl" v-model:content="content" :options="options" @text-change="editorContent" @ready="initializeEditor" />
        {{ content }}
      </template>

      <template #fallback>
        <volt-skeleton height="200px" width="100%" />
      </template>
    </client-only>
  </div>
</template>

<script setup lang="ts">
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import type { Delta } from '@vueup/vue-quill'
import type { EditorData } from '~/types'

const { vueApp } = useNuxtApp()
const emit = defineEmits<{ 'editor-content': [data: EditorData] }>()

const loadedQuillEditor = useState<boolean>('loadedQuillEditor')

if (import.meta.browser) {
  if (!loadedQuillEditor.value) {
    const { QuillEditor } = await import('@vueup/vue-quill')  
    vueApp.component('QuillEditor', QuillEditor)
    loadedQuillEditor.value = true
  }
}

const editorEl = useTemplateRef('editorEl')
const content = ref<string | Delta | undefined | null>('')

const options = {
  theme: 'snow',
  modules: {},
  placeholder: 'Write your text'
}

// Initializes the editor with default settings
function initializeEditor () {}

// Emit content on change
function editorContent () {
  emit('editor-content', {
    delta: editorEl.value?.getContents(),
    html: editorEl.value?.getHTML(),
    text: editorEl.value?.getText()
  })
}

/**
 * Height
 */

onMounted(() => {
  if (isDefined(editorEl)) {
    editorEl.value.querySelector('.ql-editor.ql-blank')!.setAttribute('style', 'height: 200px;')
  }
})
</script>
