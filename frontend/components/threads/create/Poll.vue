<template>
  <div>
    <VoltDivider />
    
    <VoltInputText label="Question" variant="outlined" />

    <p class="font-bold mt-4">Possibilities</p>
    <VoltInputText v-for="(possibility, i) in pollRequestData.possibilities" :key="i" v-model="possibility.text" />
    <VoltButton @click="handleAddPossibility">Add possibility</VoltButton>

    <div id="poll-choices">
      <div class="card flex justify-center">
        <div class="flex flex-wrap gap-4">
          <div class="flex items-center gap-2">
            <VoltRadioButton v-model="pollRequestData.choice_selection" input-id="Single" name="single" value="Single" />
            <label for="single">Single choice</label>
          </div>

          <div class="flex items-center gap-2">
            <VoltRadioButton v-model="pollRequestData.choice_selection" input-id="Unlimited" name="unlimited" value="Unlimited" />
            <label for="unlimited">Unlimited choice</label>
          </div>
          
          <div class="flex items-center gap-2">
            <VoltRadioButton v-model="pollRequestData.choice_selection" input-id="Limited" name="limited" value="Limited" />
            <label for="limited">Limit to choices</label>
          </div>
        </div>
      </div>

      <VoltInputText v-if="choicesWillBeLimited" v-model.number="pollRequestData.choices_limit" :min="1" :max="maxNumberOfChoices" type="number" label="Number of choices" />
    </div>

    <div id="poll-options">
      <p class="font-bold mt-4">Options</p>
      
      <div>
        <VoltCheckbox v-model="pollRequestData.allow_vote_change" binary />
        <label>Allow voters to change their votes</label>
      </div>

      <div>
        <VoltCheckbox v-model="pollRequestData.display.votes_publicly" binary />
        <label>Display votes publicly</label>
      </div>

      <div>
        <VoltCheckbox v-model="pollRequestData.display.results_without_voting" binary />
        <label>Allow the results to be viewed without voting</label>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { NewPollData } from '~/types'

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

const choicesWillBeLimited =  computed(() => {
  return pollRequestData.value.choice_selection === 'Limited'
})

const maxNumberOfChoices =  computed(() => {
  // Creates a maximum for the maximum number of choices
  // that a user can choose from the poll
  return pollRequestData.value.possibilities.length
})

/**
 *
 */
function handleAddPossibility () {
  // Add a new possibility to the current poll
  const template = { text: '' }
  pollRequestData.value.possibilities.push(template)
}
</script>
