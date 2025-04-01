<script setup>
import { reactive, computed } from 'vue'

  const state = reactive({
    name: null
  })

  const authors = computed(() => {
    return true
  })

  defineProps({
    something: String
  })

  function press() {
    state.name = 'Kendall' 
  }
</script>

<template>
  <div>
    <h1>{{ something }}</h1>
    <h2>{{ state.name }}</h2>
    <h4>{{ authors }}</h4>
    <button class="btn btn-lg btn-primary" @click="press">
      Press
    </button>
  </div>
</template>
