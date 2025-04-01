<template>
  <section id="create-thread" class="my-5">
    <div class="container">
      <div class="col-sm-12 col-md-8 offset-md-2">
        <div class="card">
          <div class="card-body">
            <div class="row">
              <div class="col-12">
                <select class="form-select p-2" aria-label="Thread category" @change="newThread.type=$event.target.value">
                  <option v-for="threadType in threadTypes" :key="threadType">
                    {{ threadType }}
                  </option>
                </select>

                <div v-if="newThread.type==='General discussion' || newThread.type==='Poll'" class="my-3">
                  <input v-model="newThread.title" type="text" class="form-control p-2" placeholder="TItle" aria-label="Title">
                </div>

                <div v-else-if="newThread.type==='Result'" class="my-3">
                  <div class="d-flex justify-content-around my-2">
                    <input v-model="resulThreadTitle.tournament" type="text" class="form-control p-2 me-2" placeholder="Tournament" aria-label="Tournament">
                    <input type="text" class="form-control p-2" placeholder="Round" aria-label="Round">
                  </div>

                  <div class="d-flex justify-content-around my-2">
                    <input v-model="resulThreadTitle.winner" type="text" class="form-control p-2 me-2" placeholder="Winner" aria-label="Winner">
                    <input v-model="resulThreadTitle.loser" type="text" class="form-control p-2" placeholder="Loser" aria-label="Loser">
                  </div>
                  <input type="text" class="form-control p-2" placeholder="Score" aria-label="score">
                  <p class="my-1 fw-bold">{{ threadTitle }}</p>
                </div>

                <!-- Base editor -->

                <div class="form-check my-4">
                  <input v-model="newThread.watch" class="form-check-input" type="checkbox" id="watch">
                  <label class="form-check-label" for="watch">
                    Watch this discussion
                  </label>
                </div>

                <div v-if="newThread.watch" class="alert alert-info">
                  You will be receiving notifications on each new post and interraction
                  for your newly created thread
                </div>

                <select class="form-select" size="3" aria-label="size 3 select example">
                  <option selected>Select one or multiple tags</option>
                </select>

                <button :class="{ disabled: newThread.type === 'Poll' }" class="btn btn-secondary my-4" @click="newThread.addPoll=!newThread.addPoll">
                  <span v-if="newThread.addPoll">Remove poll</span>
                  <span v-else>Add poll</span>
                </button>

                <div v-if="newThread.addPoll">
                  <hr>
                  <input type="text" class="form-control" placeholder="Question">

                  <p class="fw-bold mt-4">Possibilities</p>

                  <input v-for="(possibility, i) in newThread.poll.possibilities" :key="i" v-model="possibility.text" :placeholder="`Possibility ${i}`" :class="{ 'mt-2': i > 0 }" type="text" class="form-control">
                  <button class="btn btn-info bttn-sm mt-2 pull-right" @click="addPossibility">Add possibility</button>
                  
                  <div class="form-check mt-4">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1">
                    <label class="form-check-label" for="flexRadioDefault1">
                      Single choice
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" checked>
                    <label class="form-check-label" for="flexRadioDefault2">
                      Unlimited choice
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault3" checked>
                    <label class="form-check-label" for="flexRadioDefault3">
                      Limit to choices
                    </label>
                  </div>

                  <input v-if="choicesWillBeLimited" type="number">

                  <p class="fw-bold mt-4">Options</p>

                  <div class="form-check my-2">
                    <input v-model="newThread.poll.allowVoteChange" class="form-check-input" type="checkbox" id="watch-checkbox">
                    <label class="form-check-label" for="watch-checkbox">
                      Allow voters to change their votes
                    </label>
                  </div>
                  <div class="form-check my-2">
                    <input v-model="newThread.poll.display.votesPublicly" class="form-check-input" type="checkbox" id="watch-checkbox">
                    <label class="form-check-label" for="watch-checkbox">
                      Display votes publicly
                    </label>
                  </div>
                  <div class="form-check my-2">
                    <input v-model="newThread.poll.display.resultsWithoutVoting" class="form-check-input" type="checkbox" id="watch-checkbox">
                    <label class="form-check-label" for="watch-checkbox">
                      Allow the results to be viewed without voting
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="card-actions">
            <div class="btn-group">
              <button class="btn btn-md btn-primary">
                Create
              </button>
              <button class="btn btn-md btn-primary">
                Schedule
              </button>
              <button class="btn btn-md btn-primary">
                Save draft
              </button>
              <button class="btn btn-md btn-primary">
                Preview
              </button>
              <router-link :to="{ name: 'forum_view', params: { id: $route.params.id} }" class="btn btn-md btn-warning">
                Cancel
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'CreateThreadView',
  data: () => ({
    threadTypes: [
      'General discussion',
      'Result',
      'WWW',
      'Bombshell',
      'Draw',
      'Poll'
    ],

    resulThreadTitle: {
      tournament: null,
      round: null,
      winner: null,
      loser: null,
      score: null
    },

    newThread: {
      title: null,
      content: null,
      type: 'Result',
      watch: true,
      tags: [],
      addPoll: false,
      poll: {
        question: null,
        possibilities: [
          { text: null }
        ],
        choiceSelection: 'single',
        choicesLimit: 2,
        allowVoteChange: true,
        display: {
          votesPublicly: false,
          resultsWithoutVoting: true
        },
        closing: {
          pollCloses: false,
          days: 7
        }
      }
    }
  }),

  watch: {
    'newThread.type'(newValue) {
      if (newValue === 'Poll') {
        this.newThread.addPoll = true
      } else {
        this.newThread.addPoll = false
      }
    }
  },
  
  computed: {
    choicesWillBeLimited () {
      return this.newThread.poll.choiceSelection === 'limited'
    },
    threadTitle() {
      return `${this.resulThreadTitle.tournament} Round 4 - ${this.resulThreadTitle.winner} defeat ${this.resulThreadTitle.loser} - ${this.resulThreadTitle.score}`
    }
  },
  
  methods: {
    addPossibility () {
      var template = { text: null }
      this.newThread.poll.possibilities.push(template)
    }
  }
}
</script>
