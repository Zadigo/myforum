<template>
  <section id="create-thread" class="my-5">
    <VoltCard class="shadow-sm">
      <template #content>
        <VoltSelect v-model="requestData.category" :items="threadTypes" label="Select" />

        <div v-if="requestData.category === 'General discussion' || requestData.category === 'Poll'" class="my-3">
          <VoltInputText v-model="requestData.title" :rules="rules.titleRules" placeholder="Title" />
        </div>
        <div v-else-if="requestData.category === 'Result'" class="my-3">
          <div class="flex justify-around items-center my-2 gap-2">
            <VoltInputText v-model="requestData.result_thread_title.tournament" type="text" placeholder="Tournament" aria-label="Tournament" />
            <VoltAutoComplete v-model="requestData.result_thread_title.round" :items="roundTypes" placeholder="Round" aria-label="Round" />
          </div>

          <div class="flex justify-around items-center gap-2 my-2">
            <VoltInputText v-model="requestData.result_thread_title.winner" type="text" placeholder="Winner" aria-label="Winner" />
            <VoltInputText v-model="requestData.result_thread_title.looser" type="text" placeholder="Loser" aria-label="Loser" />
          </div>

          <VoltInputText v-model="requestData.result_thread_title.score" type="text" placeholder="Score" aria-label="Score" />
          <p class="my-1 fw-bold">
            {{ threadTitle }}
          </p>
        </div>

        <!-- Base editor -->
        <BaseEditor @editor-content="(data) => requestData.content = data" />

        <div class="my-4">
          <VoltToggleSwitch v-model="requestData.watch" />
          <label>Watch this discussion</label>
        </div>

        <VoltMessage v-if="requestData.watch" severity="warn">
          You will be receiving notifications on each new post and interraction
          for your newly created thread
        </VoltMessage>

        <VoltAutoComplete v-model="requestData.tags" label="Select multiple tags" clearable chips multiple />

        <!-- Poll -->
        <div id="poll">
          <VoltToggleButton v-model="requestData.add_poll" on-label="Remove poll" off-label="Add poll" />
          <ThreadsCreatePoll v-if="requestData.add_poll" />
        </div>
      </template>

      <template #footer>
        <VoltButton color="primary" @click="handleCreateThread">
          Create
        </VoltButton>
        <VoltButton color="secondary" @click="showSchedulingModal=true">
          Schedule
        </VoltButton>
        <VoltButton color="secondary" @click="handleCreateDraft">
          Save draft
        </VoltButton>
        <VoltButton color="secondary">
          Preview
        </VoltButton>
        <VoltButton :to="`/forums/${$route.params.id}`" color="warning">
          Cancel
        </VoltButton>
      </template>
    </VoltCard>

    <!-- Modal -->
    <VoltDialog v-model:visible="showSchedulingModal" width="500">
      <VoltDatePicker elevation="24" />
      <VoltDatePicker elevation="24" />
      <VoltButton color="primary" block @click="showSchedulingModal=false">
        Cancel
      </VoltButton>
      <VoltButton color="primary" block @click="handleScheduleThread">
        Create
      </VoltButton>
    </VoltDialog>
  </section>
</template>

<script setup lang="ts">
import { roundTypes, threadTypes } from '~/data/constants/threads'

import type { CustomRouteIdParamsGeneric, NewPollData, NewThreadData } from '~/types'

const router = useRouter()
const { $client } = useNuxtApp()
const { handleError } = useErrorHandler()

const { id } = useRoute().params as CustomRouteIdParamsGeneric

const pollRequestData = ref<NewPollData>({
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

const requestData = ref<NewThreadData>({
  forum_id: id,
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

const threadTitle =  computed(() => {
  return `${requestData.value.result_thread_title.tournament} Round 4 - ${requestData.value.result_thread_title.winner} defeat ${requestData.value.result_thread_title.looser} - ${requestData.value.result_thread_title.score}`
})

/**
 *
 */
async function handleCreateThread () {
  // Handles the creation of a thread
  try {
    if (requestData.value.add_poll) {
      requestData.value.poll = pollRequestData.value
    }

    await $client.post('threads/create', requestData.value)
    router.push(`/forums/${route.params.id}`)
  } catch (e) {
    handleError(e)
  }
}

/**
 *
 */
async function handleScheduleThread () {
  // Handle error
}

/**
 *
 */
async function handleCreateDraft () {
  requestData.value.is_draft = true
  await handleCreateThread()
}

useHead({
  title: 'Create a new thread'
})
</script>
