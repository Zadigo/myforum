<template>
  <div v-if="poll.has_poll" class="col-12">
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ poll.question }}</h5>

        <div v-if="!answered" class="row mt-2">
          <div v-if="poll.poll_type==='Single'" class="col-12 mt-2">
            <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
              <input v-model.number="answer" :value="possibility.id" class="form-check-input" type="radio" name="possibility-multiple">
              <label class="form-check-label" for="possibility-multiple">
                {{ possibility.text }}
              </label>
            </div>
          </div>

          <div v-else class="col-12">
            <div v-for="possibility in poll.possibility_set" :key="possibility.id" class="form-check">
              <input v-model="answers" class="form-check-input" type="checkbox" name="possibility-single">
              <label class="form-check-label" for="possibility-single">
                {{ possibility.text }}
              </label>
            </div>
          </div>

        </div>

        <div v-else class="row mt-2">
          Show results
        </div>

        <div class="col-12 mt-3">
          <button class="btn btn-sm btn-primary" @click="answerPoll">
            Submit answer
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'pinia'
import { useForum } from '@/stores//forum'
import { useMessages } from '@/stores//messages'
import _ from 'lodash'

export default {
  name: 'PollSection',
  setup() {
    var messagesStore = useMessages()
    return {
      messagesStore
    }
  },
  data: () => ({
    poll: {},
    answer: null,
    answers: [],
    answered: false
  }),
  mounted() {
    try {
      var polls = this.$session.retrieve('polls')
      var poll = polls[this.currentThread.id]
      this.poll = poll
    } catch {
      this.getPoll()
    }
    
  },
  computed: {
    ...mapState(useForum, ['currentThread'])
  },
  methods: {
    async getPoll() {
      try {
        var response = await this.$http.get(`polls/${this.currentThread.id}`)
        this.poll = response.data
        this.$session.create('polls', { [`${this.currentThread.id}`]: this.poll })

        var firstPossibility = _.first(this.poll.possibility_set)
        this.answer = firstPossibility['text']
      } catch(error) {
        this.messagesStore.addErrorMessage('Could not get poll')
      }
    },
    async answerPoll() {
      try {
        await this.$http.get(`polls/${this.currentThread.id}/answer`)
        this.answered = true
      } catch (error) {
        this.messagesStore.addErrorMessage('Your answer could not be submitted')
      }
    }
  }
}
</script>
