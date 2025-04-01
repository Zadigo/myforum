<template>
  <div class="row">
    <div class="col-12">
      <div v-for="(message, i) in store.messages" :key="i" :class="`alert-${message.type}`" class="alert rounded-0" style="z-index: -1;">
        {{ message.content }}
      </div>
    </div>
  </div>
</template>

<script>
import { useMessages } from '../store/messages'

export default {
  name: 'BaseMessage',
  setup() {
    var store = useMessages()
    return {
      store
    }
  }
}
</script>
