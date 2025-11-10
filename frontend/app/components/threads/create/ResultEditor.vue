<template>
  <div class="my-3">
    <div class="flex justify-around items-center my-2 gap-2">
      <VoltInputText v-model="newThread.result_thread_title.tournament" class="w-full" placeholder="Tournament" />
      <VoltAutoComplete v-model="newThread.result_thread_title.round" :suggestions="roundTypes" class="w-full" placeholder="Round" />
    </div>

    <div class="flex justify-around items-center gap-2 my-2">
      <VoltInputText v-model="newThread.result_thread_title.winner" class="w-full" placeholder="Winner" />
      <VoltInputText v-model="newThread.result_thread_title.looser" class="w-full" placeholder="Loser" />
    </div>

    <VoltInputText v-model="newThread.result_thread_title.score" class="w-full" placeholder="Score" />
    <p class="my-1 font-bold">
      {{ previewThreadTitle }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { roundTypes } from '~/data/constants/threads'

import type { NewThreadData } from '~/types'

const props = defineProps<{ modelValue: NewThreadData, previewThreadTitle: string }>()
const emit = defineEmits<{ 'update:modelValue': [data: NewThreadData] }>()

const newThread = useVModel(props, 'modelValue', emit)
</script>
