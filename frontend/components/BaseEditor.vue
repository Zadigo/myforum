<template>
  <div id="editor-wrapper" class="my-3">
    <QuillEditor ref="editor" v-model:content="content" :options="options" @text-change="editorContent" @ready="initializeEditor" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { EditorData } from '~/types';

import '@vueup/vue-quill/dist/vue-quill.snow.css';

export default defineComponent({
  name: 'BaseEditor',
  emits: {
    'editor-content' (_data: EditorData) {
      return true
    }
  },
  async setup() {
    if (!process.server) {
      const { QuillEditor } = await import('@vueup/vue-quill');
      const { vueApp } = useNuxtApp();
      vueApp.component('QuillEditor', QuillEditor);
    }
  },
  data () {
    return {
      content: null,
      options: {
        theme: 'snow',
        modules: {},
        placeholder: 'Write your text',
      }
    }
  },
  methods: {
    initializeEditor () { },
    editorContent () {
      this.$emit('editor-content', {
        delta: this.$refs.editor.getContents(),
        html: this.$refs.editor.getHTML(),
        text: this.$refs.editor.getText()
      })
    }
  }
})
</script>
