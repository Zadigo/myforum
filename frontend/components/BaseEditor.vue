<template>
  <div id="editor-wrapper" class="my-3">
    <ClientOnly>
      <QuillEditor ref="editorEl" v-model:content="content" :options="options" @text-change="editorContent" @ready="initializeEditor" />
    </ClientOnly>
  </div>
</template>

<script setup lang="ts">
import '@vueup/vue-quill/dist/vue-quill.snow.css'

import type { EditorData } from '~/types'

const emit = defineEmits<{
  'editor-content': (_data: EditorData) => void  
}>()

const editorEl = useTemplateRef('editorEl')

const content = ref<string>('')

if (import.meta.browser) {
  const { QuillEditor } = await import('@vueup/vue-quill')
  const { vueApp } = useNuxtApp()
  vueApp.component('QuillEditor', QuillEditor)
}

const options = {
  theme: 'snow',
  modules: {},
  placeholder: 'Write your text'
}

/**
 *
 */
function initializeEditor () {}

/**
 *
 */
function editorContent () {
  emit('editor-content', {
    delta: editorEl.value.getContents(),
    html: editorEl.value.getHTML(),
    text: editorEl.value.getText()
  })
}
</script>
