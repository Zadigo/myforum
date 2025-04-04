<template>
  <div  class="col-md-12">
    <div v-if="poll" class="card shadow-sm bg-yellow-100">
      <div class="card-body">
        <h5 class="card-title">
          {{ poll.question }}
        </h5>

        <div v-if="!answered" class="row mt-2">
          <div class="col-12">
            <div v-if="poll.poll_type === 'Single'" id="single-choices">
              <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
                <v-radio-group v-model="requestData.single_answer">
                  <v-radio :label="possibility.text" :value="possibility.id" />
                </v-radio-group>
              </div>
            </div>

            <div v-else-if="poll.poll_type === 'Multiple'" id="multiple-choices">
              <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
                <v-checkbox v-model="requestData.answers" :label="possibility.text" :value="possibility.id" hide-details />
              </div>
            </div>
          </div>
        </div>
        
        <div v-else class="row mt-2">
          <v-btn color="secondary" variant="tonal" rounded>
            Show results
          </v-btn>
        </div>

        <div class="col-12 mt-3 d-flex justify-content-end">
          <v-btn color="secondary" variant="tonal" rounded @click="answerPoll">
            Submit answer
          </v-btn>
        </div>
      </div>
    </div>

    <div v-else>
      Loading...
    </div>
  </div>
</template>

<script setup lang="ts">
import type { PollApiResponse } from '~/types'

const { id } = useRoute().params
const answered = ref<boolean>(false)
const poll = ref<PollApiResponse>()

const requestData = ref({
  single_answer: null,
  answers: []
})

useFetch(`/api/threads/${id}/poll`, {
  server: false,
  transform(data) {
    poll.value = data
    return data
  }
})

async function answerPoll() {
  // Handles the answer to a given poll
  try {
    await this.$http.get(`polls/${this.currentThread.id}/answer`, this.requestData)
    this.answered = true
  } catch (e) {
    this.messagesStore.addErrorMessage(e.response.data)
  }
}
</script>
