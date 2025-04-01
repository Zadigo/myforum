<template>
  <div id="pagination" class="d-flex gap-1">
    <v-btn variant="tonal" :disabled="!canPaginate" @click="emit('paginate', 1)">First</v-btn>
    <v-btn variant="tonal" :disabled="!canPaginate" @click="paginateLeft">Left</v-btn>
    <v-btn variant="tonal" :disabled="!canPaginate" @click="paginateRight">Right</v-btn>
    <v-btn variant="tonal" :disabled="!canPaginate" @click="emit('paginate', cachedResponse?.pages || 1)">Last</v-btn>
  </div>
</template>

<script setup lang="ts">
import type { PropType } from 'vue';
import type { ThreadApiResponse } from '~/types';

const { builLimitOffset } = useDjangoUtilies()

const props = defineProps({
  cachedResponse: {
    type: Object as PropType<ThreadApiResponse>,
    required: true
  },
  pagination: {
    type: Number,
    required: true
  }
})

const emit = defineEmits({
  paginate(_value: number) {
    return true
  }
})

const limits = computed(() => {
  if (props.cachedResponse) {
    return builLimitOffset(props.cachedResponse.next)
  } else {
    return null
  }
})

const currentPagination = computed({
  get: () => props.pagination,
  set: (value) => {
    emit('paginate', value)
  }
})

const canPaginate = computed(() => {
  if (props.cachedResponse) {
    return props.cachedResponse.pages > 1
  } else {
    return false
  }
})

function paginateLeft () {
  const result = props.pagination - 1
  if (result < 0) {
    currentPagination.value = props.cachedResponse.pages
  } else {
    currentPagination.value = result
  }
}

function paginateRight () {
  const result = currentPagination.value + 1
  if (result > props.cachedResponse.pages) {
    currentPagination.value = 1
  } else {
    currentPagination.value = currentPagination.value + 1
  }
}
</script>
