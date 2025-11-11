<template>
  <div id="pagination" class="d-flex gap-1">
    <v-btn variant="tonal" :disabled="!canPaginate" @click="paginateTo(0, callbackFunction)">
      <Icon name="i-lucide:angle-double-left" />
    </v-btn>
    <v-btn variant="tonal" :disabled="!canPaginatePrevious" @click="paginatPrevious(callbackFunction)">
      <Icon name="i-lucide:angle-left" />
    </v-btn>
    <v-btn variant="tonal" :disabled="!canPaginateNext" @click="paginateNext(callbackFunction)">
      <Icon name="i-lucide:angle-right" />
    </v-btn>
    <v-btn variant="tonal" :disabled="!canPaginate" @click="paginateTo(itemsCount, callbackFunction)">
      <Icon name="i-lucide:angle-double-right" />
    </v-btn>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  },
  previousUrl: {
    type: [String, null, undefined],
    required: true
  },
  nextUrl: {
    type: [String, null, undefined],
    required: true
  },
  itemsCount: {
    type: Number,
    default: 30
  }
})

const emit = defineEmits({
  'update:modelValue'(_page: number) {
    return true
  },
  'paginate'() {
    return true
  }
})

const { canPaginate, paginateTo, paginatPrevious, paginateNext, nextPaginationUrl, previousPaginationUrl, canPaginateNext, canPaginatePrevious } = usePagination()

const internalValue = computed({
  get: () => props.modelValue,
  set: (value) => {
    emit('update:modelValue', value)
    emit('paginate')
  }
})

nextPaginationUrl.value = props.nextUrl
previousPaginationUrl.value = props.previousUrl

function callbackFunction(page: number) {
  internalValue.value = page
}
</script>
