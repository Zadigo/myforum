<template>
  <quill-editor ref="editor" v-model="content" :options="additionalOptions" class="my-3" @change="editorContent" />
</template>

<script>
export default {
  name: 'BaseEditor',
  emits: ['editor-content'],
  data: () => ({
    content: null,
    additionalOptions: {}
  }),
  // mounted() {
  //   // Set the editors height to be slightly bigger
  //   // than the default standard height
  //   var editor = this.$refs.editor.$el.getElementsByClassName('ql-editor')[0]
  //   editor.style.height = '200px'
  // },
  methods: {
    editorContent (params) {
      this.$emit('editor-content', params)
    }
  }
}
</script>
