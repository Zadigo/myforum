<template>
  <section id="signup" class="my-5">
    <div class="container">
      <div class="row">
        <div class="col-sm-12 col-md-8 offset-md-2">
          <div v-if="currentStage == 1" class="card">
            <div class="card-body">
              <form @submit.prevent>
                <div>
                  <input v-model="credentials.username" id="username" type="text" autocomplete="username"
                    class="form-control p-3" placeholder="Username">
                  <label class="form-label my-2" for="username">
                    This is the name that will be shown with your messages. You may use any name you wish. Once set, it
                    can only be changed once within 90 days of registering.
                  </label>
                </div>
                <input v-model="credentials.email" type="email" autocomplete="email" class="form-control p-3 my-1"
                  placeholder="Email address">
                <input v-model="credentials.password1" type="password" autocomplete="new-password"
                  class="form-control p-3 my-1" placeholder="Password">
                <input v-model="credentials.password2" type="password" autocomplete="new-password"
                  class="form-control p-3 my-1" placeholder="Enter password again">

                <div class="form-check form-switch mt-4">
                  <input v-model="termsAndPolicies" class="form-check-input" type="checkbox" role="switch"
                    id="terms-and-policies">
                  <label class="form-check-label" for="terms-and-policies">I agree to terms and privacy policies</label>
                </div>

                <button :class="{ disabled: !canBeSubmitted }" class="btn btn-lg btn-primary mt-4" @click="register">
                  Register
                </button>
              </form>
            </div>
          </div>

          <div v-if="currentStage == 2" class="card">
            <div class="card-body">
              <p>Select bunch of topics in which you are interested in</p>
              <select v-model="additionalDetails.topics" class="form-select" multiple aria-label="multiple select example">
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </select>

              <p class="mt-4">Select the main player in which you are interested</p>
              <select v-model="additionalDetails.mainPlayer" class="form-select form-select-lg mb-3" aria-label=".form-select-lg example">
                <option selected>Open this select menu</option>
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </select>

              <p class="mt-4">Select alternative players that you will be supporting</p>
              <select v-model="additionalDetails.otherPlayers" class="form-select" multiple aria-label="multiple select example">
                <option value="1">One</option>
                <option value="2">Two</option>
                <option value="3">Three</option>
              </select>

              <button class="btn btn-lg btn-primary mt-4" @click="completeRegistration">
                Complete registration
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { useMessages } from '../store/messages'

export default {
  name: 'SignupView',
  setup() {
    var store = useMessages()
    var messagesStore = useMessages()
    return {
      store,
      messagesStore
    }
  },
  data: () => ({
    currentStage: 1,
    credentials: {
      username: null,
      email: null,
      password1: null,
      password2: null
    },
    additionalDetails: {
      topics: [],
      mainPlayer: null,
      otherPlayers: []
    },
    termsAndPolicies: false,
    isCompleted: false
  }),
  computed: {
    canBeSubmitted() {
      return this.termsAndPolicies ? true : false
    }
  },
  beforeMount() {
    var registered = this.$session.retrieve('registered')
    if (registered) {
      this.currentStage = 2
    }
  },
  beforeUnmount() {
    if (!this.isCompleted) {
      this.$session.create('registration_complete', false)
    }
  },
  methods: {
    async register() {
      try {
        this.currentStage = 2
        // Check for if the user has already done
        // the registration process and if, yes,
        // just show him the second screen
        this.$session.create('registered', true)
        this.isCompleted = true
      } catch(error) {
        this.store.addErrorMessage(error.message)
      }
    },
    async completeRegistration() {
      try {
        this.$router.push({ name: 'forums_view' })
        this.$session.remove('registered')
        this.isCompleted = true
        this.$session.create('registration_complete', true)
        this.messagesStore.addSuccessMessage('You earned new badges. Check them out now!')
      } catch (error) {
        this.store.addErrorMessage(error.message)
      }
    }
  }
}
</script>
