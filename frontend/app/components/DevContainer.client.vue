<template>
  <div ref="containerEl" :style="style" class="fixed top-0 left-0 rounded-lg shadow-sm bg-primary-500/10 dark:bg-primary-100/10 backdrop-blur-3xl w-100 h-auto py-2 px-10 z-50">
    <volt-button @click="() => { toggleWrapper() }">
      <icon name="i-lucide:x" />
    </volt-button>

    <div v-if="showWrapper" class="space-y-3">
      <slot />
    </div>
  </div>  
</template>

<script setup lang="ts">
const containerEl = useTemplateRef('containerEl')

const coordinates = useLocalStorage('dev-container-coordinates', { x: 20, y: 20 }, {
  serializer: {
    read: (value) => JSON.parse(value),
    write: (value) => JSON.stringify(value)
  }
})
const { style, x, y } = useDraggable(containerEl, { initialValue: coordinates })


watch([x, y], ([newX, newY]) => {
  coordinates.value = { x: newX, y: newY }
})

const showWrapper = ref(false)
const toggleWrapper = useToggle(showWrapper)
</script>
