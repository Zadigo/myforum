<template>
  <VoltCard v-if="poll && poll.has_poll" class="shadow-sm bg-secondary-400">
    <template #content>
      <h5 class="text-2xl font-bold">
        {{ poll.poll.question }}
      </h5>

      <div v-if="!answered" class="row mt-2">
        <div v-if="poll.poll.poll_type === 'Single'" id="single-choices">
          {{ newAnswer.single_answer }}
          <div v-for="possibility in poll.poll.possibility_set" :key="possibility.id">
            <VoltLabel>
              <VoltRadioButton v-model="newAnswer.single_answer" :value="possibility.id" :name="possibility.id" />
              <label>{{ possibility.text }}</label>
            </VoltLabel>
          </div>
        </div>

        <div v-else-if="poll.poll.poll_type === 'Multiple'" id="multiple-choices" class="space-y-5">
          <VoltLabel v-for="possibility in poll.poll.possibility_set" :key="possibility.id">
            <VoltCheckbox v-model="newAnswer.answers" :value="possibility.id" />
            <label>{{ possibility.text }}</label>
          </VoltLabel>
        </div>
      </div>
      
      <div v-else class="row mt-2">
        <VoltButton rounded>
          Show results
        </VoltButton>
      </div>

      <div class="flex justify-end">
        <VoltButton :disabled="answered" @click="async () => await submitAnswer()">
          Submit answer
        </VoltButton>
      </div>
    </template>
  </VoltCard>
</template>

<script setup lang="ts">
import type { CustomRouteIdParamsGeneric, PollApiResponse } from '~/types'

interface NewAnswer {
  single_answer: number | null
  answers: number[]
}

const { id } = useRoute().params as CustomRouteIdParamsGeneric
const answered = ref<boolean>(false)

const newAnswer = ref<NewAnswer>({
  single_answer: null,
  answers: []
})

const { data: poll } = await useFetch<PollApiResponse>(`/v1/threads/${id}/poll`, {
  baseURL: useRuntimeConfig().public.prodDomain,
  server: false
})

console.log('poll', poll.value)

/**
 * Submits the user's answer to the poll
 */
async function submitAnswer() {
  await useFetch(`/api/threads/${id}/poll/answer`, {
    baseURL: useRuntimeConfig().public.prodDomain,
    method: 'post',
    body: newAnswer.value,
    onResponseError(error) {
      console.error('Error answering poll:', error)
      // Handle error, e.g., show a message to the user
    },
    onResponse(response) {
      answered.value = true
      // Optionally, handle successful response
    }
  })
}
</script>
