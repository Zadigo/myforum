<template>
  <div  class="col-md-12">
    <VoltCard v-if="poll" class="shadow-sm bg-yellow-100">
      <template #content>
        <h5 class="font-title text-2xl font-bold">
          {{ poll.question }}
        </h5>

        <div v-if="!answered" class="row mt-2">
          <div v-if="poll.poll_type === 'Single'" id="single-choices">
            <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
              <v-radio-group v-model="requestData.single_answer">
                <v-radio :label="possibility.text" :value="possibility.id" />
              </v-radio-group>
            </div>
          </div>

          <div v-else-if="poll.poll_type === 'Multiple'" id="multiple-choices">
            <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="flex items-center gap-2">
              <VoltCheckbox v-model="requestData.answers" :value="possibility.id" hide-details />
              <label>{{ possibility.text }}</label>
            </div>
          </div>
        </div>
        
        <div v-else class="row mt-2">
          <VoltButton rounded>
            Show results
          </VoltButton>
        </div>

        <div class="flex justify-end">
          <VoltButton @click="answerPoll">
            Submit answer
          </VoltButton>
        </div>
      </template>
    </VoltCard>

    <div v-else>
      Loading...
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CustomRouteIdParamsGeneric, PollApiResponse } from '~/types'

const { id } = useRoute().params as CustomRouteIdParamsGeneric
const answered = ref<boolean>(false)
// const poll = ref<PollApiResponse>()

const requestData = ref({
  single_answer: null,
  answers: []
})

const { data: poll } = useFetch<PollApiResponse>(`/api/threads/${id}/poll`, { server: false })

/**
 * Handles the answer to a given poll
 */
async function answerPoll() {
  try {
    await this.$http.get(`polls/${this.currentThread.id}/answer`, this.requestData)
    this.answered = true
  } catch (e) {
    this.messagesStore.addErrorMessage(e.response.data)
  }
}
</script>
