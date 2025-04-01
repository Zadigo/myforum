<template>
  <div id="editor-wrapper" class="my-3">
    <quill-editor ref="editor" v-model:content="content" :options="options" @text-change="editorContent" @ready="initializeEditor" />
  </div>
</template>

<script>
// import Quill from 'quill'
import { QuillEditor } from '@vueup/vue-quill'

export default {
  name: 'BaseEditor',
  components: { QuillEditor },
  emits: {
    'editor-content' () {
      return true
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
}
</script>
