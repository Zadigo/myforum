<template>
  <div v-if="poll.has_poll" class="col-12">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ poll.question }}</h5>

        <div v-if="!answered" class="row mt-2">
          <div class="col-12">
            <div v-if="poll.poll_type === 'Single'" id="single-choices">
              <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
                <v-radio v-model="requestData.answers" :label="possibility.text" :value="possibility.id"></v-radio>
              </div>
            </div>
            <div v-else-if="poll.poll_type === 'Multiple'" id="single-choices">
              <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
                <v-checkbox v-model="requestData.answers" :label="possibility.text" :value="possibility.id" hide-details></v-checkbox>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="row mt-2">
          Show results
        </div>

        <div class="col-12 mt-3 d-flex justify-content-end">
          <v-btn color="secondary" variant="tonal" rounded @click="answerPoll">
            Submit answer
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { ref } from 'vue'
import { mapState } from 'pinia'
import { useForum } from '@/stores//forum'
import { useMessages } from '@/stores//messages'

export default {
  name: 'PollSection',
  setup() {
    const messagesStore = useMessages()
    const requestData = ref({
      answers: []
    })
    return {
      requestData,
      messagesStore
    }
  },
  data () {
    return {
      poll: {},
      answer: null,
      answered: false
    }
  },
  computed: {
    ...mapState(useForum, ['currentThread'])
  },
  created() {
    // try {
    //   const polls = this.$session.retrieve('polls')
    //   const poll = polls[this.currentThread.id]
    //   this.poll = poll
    // } catch {
    // }
    this.getPoll()
  },
  methods: {
    async getPoll() {
      // The poll for the current thread
      try {
        const response = await this.$http.get(`polls/${this.currentThread.id}`)
        if (response.data.has_poll) {
          this.poll = response.data
          this.$session.create('polls', { [`${this.currentThread.id}`]: this.poll })
  
          const firstPossibility = _.first(this.poll.possibility_set)
          this.answer = firstPossibility.text
        }
      } catch(e) {
        this.messagesStore.addErrorMessage(e)
      }
    },
    async answerPoll() {
      // Handles the answer to a given poll
      try {
        await this.$http.get(`polls/${this.currentThread.id}/answer`, this.requestData)
        this.answered = true
      } catch (e) {
        this.messagesStore.addErrorMessage(e.response.data)
      }
    }
  }
}
</script>
