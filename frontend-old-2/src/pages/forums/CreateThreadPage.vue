<template>
  <section id="create-thread" class="my-5">
    <div class="container">
      <div class="col-sm-12 col-md-8 offset-md-2">
        <div class="card shadow-sm">
          <div class="card-body">
            <div class="row">
              <div class="col-12">
                <v-select v-model="requestData.category" :items="threadTypes" label="Select" variant="outlined"></v-select>

                <div v-if="requestData.category === 'General discussion' || requestData.category === 'Poll'" class="my-3">
                  <v-text-field v-model="requestData.title" :rules="titleRules" label="Title" aria-label="Title" variant="outlined"></v-text-field>
                </div>
                <div v-else-if="requestData.category === 'Result'" class="my-3">
                  <div class="d-flex justify-content-around align-items-center my-2 gap-2">
                    <v-text-field v-model="requestData.result_thread_title.tournament" type="text" placeholder="Tournament" aria-label="Tournament" variant="outlined"></v-text-field>
                    <v-autocomplete v-model="requestData.result_thread_title.round" :items="roundTypes" variant="outlined" placeholder="Round" aria-label="Round"></v-autocomplete>
                  </div>

                  <div class="d-flex justify-content-around align-items-center gap-2 my-2">
                    <v-text-field v-model="requestData.result_thread_title.winner" type="text" placeholder="Winner" aria-label="Winner" variant="outlined"></v-text-field>
                    <v-text-field v-model="requestData.result_thread_title.looser" type="text" placeholder="Loser" aria-label="Loser" variant="outlined"></v-text-field>
                  </div>

                  <v-text-field v-model="requestData.result_thread_title.score" type="text" placeholder="Score" aria-label="Score" variant="outlined"></v-text-field>
                  <p class="my-1 fw-bold">{{ threadTitle }}</p>
                </div>

                <!-- Base editor -->
                <base-editor @editor-content="(data) => requestData.content = data" />

                <div class="form-check my-4">
                  <v-switch v-model="requestData.watch" label="Watch this discussion" inset hide-details></v-switch>
                </div>

                <div v-if="requestData.watch" class="alert alert-info">
                  You will be receiving notifications on each new post and interraction
                  for your newly created thread
                </div>

                <v-autocomplete v-model="requestData.tags" label="Select multiple tags" variant="outlined" clearable chips multiple></v-autocomplete>

                <!-- Poll -->
                <div id="poll">
                  <v-btn :class="{ disabled: requestData.category === 'Poll' }" variant="tonal" color="primary" @click="requestData.add_poll = !requestData.add_poll">
                    <span v-if="requestData.add_poll">Remove poll</span>
                    <span v-else>Add poll</span>
                  </v-btn>

                  <div v-if="requestData.add_poll">
                    <hr>
                    <v-text-field :rules="titleRules" label="Question" variant="outlined"></v-text-field>

                    <p class="fw-bold mt-4">Possibilities</p>
                    <v-text-field v-for="(possibility, i) in pollRequestData.possibilities" :key="i" v-model="possibility.text" :rules="possibilityRules" label="Possibility" variant="outlined"></v-text-field>
                    <v-btn color="primary" @click="addPossibility">Add possibility</v-btn>

                    <div id="poll-choices">
                      <v-radio-group v-model="pollRequestData.choice_selection" class="mt-4">
                        <v-radio label="Single choice" value="Single"></v-radio>
                        <v-radio label="Unlimited choice" value="Unlimited"></v-radio>
                        <v-radio label="Limit to choices" value="Limited"></v-radio>
                      </v-radio-group>

                      <v-text-field v-if="pollRequestData.choice_selection === 'limited'" v-model="pollRequestData.choices_limit" :min="1" :max="maxNumberOfChoices" type="number" variant="outlined" label="Number of choices"></v-text-field>
                    </div>

                    <div id="poll-options">
                      <p class="fw-bold mt-4">Options</p>
                      <v-checkbox v-model="pollRequestData.allow_vote_change" label="Allow voters to change their votes"></v-checkbox>
                      <v-checkbox v-model="pollRequestData.display.votes_publicly" label="Display votes publicly"></v-checkbox>
                      <v-checkbox v-model="pollRequestData.display.results_without_voting" label="Allow the results to be viewed without voting"></v-checkbox>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <v-btn color="primary" @click="createThread">
              Create
            </v-btn>
            <v-btn color="secondary" @click="showSchedulingModal=true">
              Schedule
            </v-btn>
            <v-btn color="secondary" @click="createDraft">
              Save draft
            </v-btn>
            <v-btn color="secondary">
              Preview
            </v-btn>
            <v-btn :to="{ name: 'forum_view', params: { id: $route.params.id } }" color="warning">
              Cancel
            </v-btn>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <v-dialog v-model="showSchedulingModal" width="500">
      <v-card>
        <v-card-text>
          <v-date-picker elevation="24"></v-date-picker>
          <v-date-picker elevation="24"></v-date-picker>
        </v-card-text>

        <v-card-actions>
          <v-btn color="primary" block @click="showSchedulingModal=false">
            Cancel
          </v-btn>
          <v-btn color="primary" block @click="scheduleThread">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </section>
</template>

<script>
import { ref } from 'vue'

import BaseEditor from '@/layouts/BaseEditor.vue'
import { useMessages } from '@/stores/messages'

export default {
  name: 'CreateThreadView',
  components: {
    BaseEditor
  },
  setup () {
    const messagesStore = useMessages()
    const showSchedulingModal = ref(false)
    const roundTypes = [
      'QF1',
      'QF2',
      '1st',
      '2nd',
      '3rd',
      '4th',
      'QF',
      'SF',
      'F'
    ]
    const threadTypes = ref([
      'General discussion',
      'Result',
      'WWW',
      'Bombshell',
      'Draw',
      'Poll'
    ])
    const pollRequestData = ref({
      question: null,
      possibilities: [
        { text: null }
      ],
      choice_selection: 'Single',
      choices_limit: 1,
      allow_vote_change: true,
      display: {
        votes_publicly: false,
        results_without_voting: true
      },
      closing: {
        poll_closes: false,
        days: 7
      }
    })
    const requestData = ref({
      title: null,
      result_thread_title: {
        tournament: null,
        round: null,
        winner: null,
        looser: null,
        score: null
      },
      content: {
        delta: null,
        html: null,
        text: null
      },
      category: 'General discussion',
      watch: true,
      tags: [],
      schedule_date: null,
      is_draft: false,
      add_poll: false,
      poll: null
    })
    return {
      messagesStore,
      showSchedulingModal,
      threadTypes,
      roundTypes,
      pollRequestData,
      requestData
    }
  },
  data () {
    return {
      titleRules: [
        value => value === 'Google' || 'Google is not allowed'
      ],
      possibilityRules: [
        value => !!value || 'Poll requires a possibility'
      ]
    }
  },
  computed: {
    choicesWillBeLimited () {
      return this.requestData.poll.choice_selection === 'limited'
    },
    threadTitle () {
      return `${this.requestData.result_thread_title.tournament} Round 4 - ${this.requestData.result_thread_title.winner} defeat ${this.requestData.result_thread_title.looser} - ${this.requestData.result_thread_title.score}`
    },
    maxNumberOfChoices () {
      // Creates a maximum for the maximum number of choices
      // that a user can choose from the poll
      return this.requestData.poll.possibilities.length
    }
  },
  watch: {
    'requestData.category' (n) {
      if (n === 'Poll') {
        this.requestData.add_poll = true
      } else {
        this.requestData.add_poll = false
      }
    }
  },
  methods: {
    async createThread () {
      // Handles the creation of a thread
      try {
        this.requestData.forum_id = this.$route.params.id

        if (this.requestData.add_poll) {
          this.requestData.poll = this.pollRequestData
        }

        const response = await this.$http.post('threads/create', this.requestData)
        console.log(response.data)
        this.$router.push({ name: 'forum_view', params: { id: this.$route.params.id } })
      } catch (e) {
        this.messagesStore.addErrorMessage(e.response.data)
      }
    },
    async scheduleThread () { },
    async createDraft () {
      this.requestData.is_draft = true
      await this.createThread()
    },
    addPossibility () {
      // Add a new possibility to the current poll
      const template = { text: null }
      this.requestData.poll.possibilities.push(template)
    }
  }
}
</script>
