<template>
  <section id="create-thread" class="my-5">
    <div class="container">
      <div class="col-sm-12 col-md-8 offset-md-2">
        <div class="card shadow-sm">
          <div class="card-body">
            <div class="row">
              <div class="col-12">
                <v-select v-model="requestData.category" :items="threadTypes" label="Select" variant="outlined" />

                <div v-if="requestData.category === 'General discussion' || requestData.category === 'Poll'" class="my-3">
                  <v-text-field v-model="requestData.title" :rules="rules.titleRules" label="Title" aria-label="Title" variant="outlined" />
                </div>
                <div v-else-if="requestData.category === 'Result'" class="my-3">
                  <div class="d-flex justify-content-around align-items-center my-2 gap-2">
                    <v-text-field v-model="requestData.result_thread_title.tournament" type="text" placeholder="Tournament" aria-label="Tournament" variant="outlined" />
                    <v-autocomplete v-model="requestData.result_thread_title.round" :items="roundTypes" variant="outlined" placeholder="Round" aria-label="Round" />
                  </div>

                  <div class="d-flex justify-content-around align-items-center gap-2 my-2">
                    <v-text-field v-model="requestData.result_thread_title.winner" type="text" placeholder="Winner" aria-label="Winner" variant="outlined" />
                    <v-text-field v-model="requestData.result_thread_title.looser" type="text" placeholder="Loser" aria-label="Loser" variant="outlined" />
                  </div>

                  <v-text-field v-model="requestData.result_thread_title.score" type="text" placeholder="Score" aria-label="Score" variant="outlined" />
                  <p class="my-1 fw-bold">
                    {{ threadTitle }}
                  </p>
                </div>

                <!-- Base editor -->
                <BaseEditor @editor-content="(data) => requestData.content = data" />

                <div class="form-check my-4">
                  <v-switch v-model="requestData.watch" label="Watch this discussion" inset hide-details />
                </div>

                <div v-if="requestData.watch" class="alert alert-info">
                  You will be receiving notifications on each new post and interraction
                  for your newly created thread
                </div>

                <v-autocomplete v-model="requestData.tags" label="Select multiple tags" variant="outlined" clearable chips multiple />

                <!-- Poll -->
                <div id="poll">
                  <v-btn :class="{ disabled: requestData.category === 'Poll' }" variant="tonal" color="primary" @click="requestData.add_poll = !requestData.add_poll">
                    <span v-if="requestData.add_poll">Remove poll</span>
                    <span v-else>Add poll</span>
                  </v-btn>

                  <div v-if="requestData.add_poll">
                    <hr>
                    <v-text-field :rules="rules.titleRules" label="Question" variant="outlined" />

                    <p class="fw-bold mt-4">Possibilities</p>
                    <v-text-field v-for="(possibility, i) in pollRequestData.possibilities" :key="i" v-model="possibility.text" :rules="rules.possibilityRules" label="Possibility" variant="outlined" />
                    <v-btn color="primary" @click="handleAddPossibility">Add possibility</v-btn>

                    <div id="poll-choices">
                      <v-radio-group v-model="pollRequestData.choice_selection" class="mt-4">
                        <v-radio label="Single choice" value="Single" />
                        <v-radio label="Unlimited choice" value="Unlimited" />
                        <v-radio label="Limit to choices" value="Limited" />
                      </v-radio-group>

                      <v-text-field v-if="pollRequestData.choice_selection === 'Limited'" v-model="pollRequestData.choices_limit" :min="1" :max="maxNumberOfChoices" type="number" variant="outlined" label="Number of choices" />
                    </div>

                    <div id="poll-options">
                      <p class="fw-bold mt-4">Options</p>
                      <v-checkbox v-model="pollRequestData.allow_vote_change" label="Allow voters to change their votes" />
                      <v-checkbox v-model="pollRequestData.display.votes_publicly" label="Display votes publicly" />
                      <v-checkbox v-model="pollRequestData.display.results_without_voting" label="Allow the results to be viewed without voting" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <v-btn color="primary" @click="handleCreateThread">
              Create
            </v-btn>
            <v-btn color="secondary" @click="showSchedulingModal=true">
              Schedule
            </v-btn>
            <v-btn color="secondary" @click="handleCreateDraft">
              Save draft
            </v-btn>
            <v-btn color="secondary">
              Preview
            </v-btn>
            <v-btn :to="`/forums/${$route.params.id}`" color="warning">
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
          <v-date-picker elevation="24" />
          <v-date-picker elevation="24" />
        </v-card-text>

        <v-card-actions>
          <v-btn color="primary" block @click="showSchedulingModal=false">
            Cancel
          </v-btn>
          <v-btn color="primary" block @click="handleScheduleThread">
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </section>
</template>

<script setup lang="ts">
interface PollRequestData {
  question: string,
  possibilities: { text: string }[]
  choice_selection: 'Single' | 'Limited'
  choices_limit: number
  allow_vote_change: boolean
  display: {
    votes_publicly: boolean
    results_without_voting: boolean
  },
  closing: {
    poll_closes: boolean
    days: number
  }
}

interface RequestData {
  forum_id: string | number
  title: string
  result_thread_title: {
    tournament: string | null
    round: string | null
    winner: string | null
    looser: string | null
    score: string | null
  },
  content: {
    delta: string | null
    html: string | null
    text: string | null
  },
  category:  'General discussion' | 'Result' | 'WWW' | 'Bombshell' | 'Draw' | 'Poll'
  watch: boolean,
  tags: string[],
  schedule_date: string | null
  is_draft: boolean
  add_poll: boolean
  poll: PollRequestData
}

const pollRequestData = ref<PollRequestData>({
  question: '',
  possibilities: [
    {
      text: ''
    }
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

const requestData = ref<RequestData>({
  title: '',
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

const showSchedulingModal = ref(false)

const rules = {
  titleRules: [
    (value: string) => value === 'Google' || 'Google is not allowed'
  ],
  possibilityRules: [
    (value: string) => !!value || 'Poll requires a possibility'
  ]
}

function useThread () {
  const threadTypes = [
    'General discussion',
    'Result',
    'WWW',
    'Bombshell',
    'Draw',
    'Poll'
  ]
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
  
  const router = useRouter()
  const route = useRoute()
  const { $client } = useNuxtApp()
  const { handleError } = useErrorHandler()

  const threadTitle =  computed(() => {
    return `${requestData.value.result_thread_title.tournament} Round 4 - ${requestData.value.result_thread_title.winner} defeat ${requestData.value.result_thread_title.looser} - ${requestData.value.result_thread_title.score}`
  })

  async function handleCreateThread () {
    // Handles the creation of a thread
    try {
      requestData.value.forum_id = route.params.id

      if (requestData.value.add_poll) {
        requestData.value.poll = pollRequestData.value
      }

      await $client.post('threads/create', requestData.value)
      router.push(`/forums/${route.params.id}`)
    } catch (e) {
      handleError(e)
    }
  }

  async function handleScheduleThread () {
    // Handle error
  }

  async function handleCreateDraft () {
    requestData.value.is_draft = true
    await handleCreateThread()
  }

  return {
    handleScheduleThread,
    handleCreateDraft,
    handleCreateThread,
    roundTypes,
    threadTypes,
    threadTitle
  }
}

function usePoll () {
    const choicesWillBeLimited =  computed(() => {
      return requestData.value.poll.choice_selection === 'limited'
    })

    const maxNumberOfChoices =  computed(() => {
      // Creates a maximum for the maximum number of choices
      // that a user can choose from the poll
      return pollRequestData.value.poll.possibilities.length
    })

    function handleAddPossibility () {
      // Add a new possibility to the current poll
      const template = { text: null }
      this.requestData.poll.possibilities.push(template)
    }

    return {
      handleAddPossibility,
      choicesWillBeLimited,
      threadTitle,
      maxNumberOfChoices
    }
}

const { threadTitle, handleCreateThread, handleScheduleThread, handleCreateDraft, threadTypes, roundTypes } = useThread()
const { choicesWillBeLimited, maxNumberOfChoices, handleAddPossibility } = usePoll()
</script>
