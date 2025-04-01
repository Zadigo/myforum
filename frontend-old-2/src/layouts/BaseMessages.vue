<template>
  <div v-if="store.hasMessages" class="row my-5">
    <div class="col-12">
      <div v-for="(message, i) in store.messages" :key="i" :class="`alert-${message.type}`" class="alert alert-dismissible rounded-0" role="alert">
        {{ message.content }}
        <button type="button" class="btn-close" aria-label="Close" @click="dismissAlert(i)"></button>
      </div>
    </div>
  </div>
</template>

<script>
import { storeToRefs } from 'pinia'
import { useMessages } from '@/stores//messages'

export default {
  name: 'BaseMessage',
  setup() {
    const store = useMessages()
    const { messages } = storeToRefs(store)
    return {
      store,
      messages
    }
  },
  methods: {
    dismissAlert (index) {
      // Delete an alert from the list
      this.messages.shift(index, 1)
    }
  }
}
</script>
