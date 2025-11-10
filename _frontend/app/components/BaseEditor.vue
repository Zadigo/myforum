<template>
  <div id="editor-wrapper" class="my-3">
    <ClientOnly>
      <QuillEditor ref="editorEl" v-model:content="content" :options="options" @text-change="editorContent" @ready="initializeEditor" />
      {{ content }}
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import type { Delta } from '@vueup/vue-quill'
import type { EditorData } from '~/types'

const { vueApp } = useNuxtApp()
const emit = defineEmits<{ 'editor-content': [data: EditorData] }>()

if (import.meta.browser) {
  const { QuillEditor } = await import('@vueup/vue-quill')  
  vueApp.component('QuillEditor', QuillEditor)
}

const editorEl = useTemplateRef('editorEl')
const content = ref<string | Delta | undefined | null>('')

const options = {
  theme: 'snow',
  modules: {},
  placeholder: 'Write your text'
}

/**
 * Initializes the editor with default settings
 */
function initializeEditor () {}

/**
 *
 */
function editorContent () {
  emit('editor-content', {
    delta: editorEl.value?.getContents(),
    html: editorEl.value?.getHTML(),
    text: editorEl.value?.getText()
  })
}
</script>
