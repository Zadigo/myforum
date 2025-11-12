<template>
  <div>
    <VoltDivider />

    <!-- Question -->
    <volt-input-text placeholder="Question" />

    <!-- Possibilities -->
    <div>
      <p class="font-bold mt-4 mb-2">Possibilities</p>

      <div class="space-y-2 space-x-2">
        <!-- <volt-input-text v-for="(possibility, i) in poll.possibilities" :key="i" v-model="possibility.text" /> -->
        <volt-input-group v-for="(possibility, i) in poll.possibilities" :key="i">
          <volt-input-text v-model="possibility.text" pt:root="rounded-none" />

          <template #end>
            <volt-secondary-button color="danger" pt:root="rounded-none" @click="poll.possibilities.splice(i, 1)">
              <icon name="i-lucide:trash" />
            </volt-secondary-button>
          </template>
        </volt-input-group>

        <volt-button @click="handleAddPossibility">
          Add possibility
        </volt-button>
      </div>
    </div>

    <div id="poll-choices">
      <div class="card flex justify-center">
        <div class="flex flex-wrap gap-4">
          <volt-label label-for="single-choice" label="Single choice">
            <volt-radio-button v-model="poll.choice_selection" input-id="Single" name="single" value="Single" />
          </volt-label>

          <volt-label label-for="unlimited-choice" label="Unlimited choice">
            <volt-radio-button v-model="poll.choice_selection" input-id="Unlimited" name="unlimited" value="Unlimited" />
          </volt-label>

          <volt-label label-for="limit-to-choice" label="Limit to choices">
            <volt-radio-button v-model="poll.choice_selection" input-id="Limited" name="limited" value="Limited" />
          </volt-label>
        </div>
      </div>

      <volt-input-text v-if="choicesWillBeLimited" v-model.number="poll.choices_limit" :min="1" :max="maxNumberOfChoices" type="number" label="Number of choices" />
    </div>

    <div id="poll-options" class="space-y-2">
      <p class="font-bold mt-4">Options</p>

      <volt-label label-for="allow-vote-change" label="Allow voters to change their votes">
        <volt-checkbox v-model="poll.allow_vote_change" binary />
      </volt-label>

      <volt-label label-for="display-votes-publicly" label="Display votes publicly">
        <volt-checkbox v-model="poll.display.votes_publicly" binary />
      </volt-label>

      <volt-label label-for="results-without-voting" label="Allow the results to be viewed without voting">
        <volt-checkbox v-model="poll.display.results_without_voting" binary />
      </volt-label>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NewPollData } from '~/types'

const props = defineProps<{ modelValue: NewPollData }>()
const emit = defineEmits<{ 'update:modelValue': [NewPollData] }>()

const poll = useVModel(props, 'modelValue', emit)

const choicesWillBeLimited =  computed(() => poll.value.choice_selection === 'Limited')
// Creates a maximum for the maximum number of choices
// that a user can choose from the poll
const maxNumberOfChoices =  computed(() => poll.value.possibilities.length)

// Handles the addition of a new possibility
// to the current poll
function handleAddPossibility () {
  const template = { text: '' }
  poll.value.possibilities.push(template)
}
</script>
