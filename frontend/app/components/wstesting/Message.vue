<template>
  <div class="p-3 bg-red-700/10 dark:bg-red-700/50 backdrop-blur-3xl ">
    <div class="w-full mb-2">
      <volt-button v-for="key in keys" :key="key" @click="copyValue(key)">
        <icon name="lucide:copy" />
        {{ key }}
      </volt-button>

      <volt-button @click="copySelection()">
        <icon name="lucide:copy" />
        Copy Selection
      </volt-button>
    </div>
        
    <pre class="overflow-y-scroll rounded-2xl text-primary-50 p-3">
      <code>
        {{ _message }}
      </code>
    </pre>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  message: string
}>()

const _message = computed(() => {
  try {
    return JSON.stringify(JSON.parse(props.message), null, 2).trim()
  } catch {
    return props.message
  }
})

const _jsonMessage = computed(() => {
  try {
    return JSON.parse(props.message) as Record<string, unknown>
  } catch {
    return null
  }
})

const keys = computed(() => {
  if (!_jsonMessage.value) return []
  return Object.keys(_jsonMessage.value)
    .map((key) => key.trim())
    .filter((key) => key.toLowerCase()
    .includes("id"))
})

function copyValue(key: string) {
  if (isDefined(_jsonMessage)) {
    const { copy } = useClipboard({source: String(_jsonMessage.value[key])})
    copy()
  }
}

const { selection } = useTextSelection()
function copySelection() {
  if (isDefined(selection.value)) {
    const { copy } = useClipboard({source: selection.value.toString()})
    copy()
  }
}
</script>
