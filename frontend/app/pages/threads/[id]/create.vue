<template>
  <section id="create-thread" class="my-5">
    <VoltCard class="shadow-sm">
      <template #content>
        <form id="creation" @submit.prevent>
          <!-- Thread Type -->
          <VoltSelect v-model="newThread.category" :options="threadTypes" label="Select" class="w-6/12" />

          <!-- Title -->
          <div v-if="newThread.category === 'General discussion' || newThread.category === 'Poll'" class="my-3">
            <VoltInputText v-model="newThread.title" placeholder="Title" class="w-full" />
          </div>
          <ThreadsCreateResultEditor v-else-if="newThread.category === 'Result'" v-model="newThread" :preview-thread-title="previewThreadTitle" />
          
          <!-- Base editor -->
          <BaseEditor @editor-content="(data) => newThread.content = data" />

          <!-- Notifications -->
          <VoltLabel class="my-4">
            <VoltToggleSwitch v-model="newThread.watch" />
            <label>Watch this discussion</label>
          </VoltLabel >

          <VoltMessage v-if="newThread.watch" severity="warn" class="my-3">
            You will be receiving notifications on each new post and interraction
            for your newly created thread
          </VoltMessage>

          <!-- Tags -->
          <VoltAutoComplete v-model="search" :suggestions="tags" input-id="multiple-tags" placeholder="Select multiple tags" class="my-4 w-full" multiple fluid @complete="searchComplete" />

          <!-- Poll -->
          <div id="poll">
            <VoltToggleButton v-model="newThread.add_poll" on-label="Remove poll" off-label="Add poll" />
            <ThreadsCreatePoll v-if="newThread.add_poll" v-model="newPoll" />
          </div>
        </form>
      </template>

      <template #footer>
        <div class="space-x-2 py-5">
          <VoltButton color="primary" @click="() => create">
            Create
          </VoltButton>
          <VoltButton color="secondary" @click="showSchedulingModal=true">
            Schedule
          </VoltButton>
          <VoltButton color="secondary" @click="() => create">
            Save draft
          </VoltButton>
          <VoltButton color="secondary">
            Preview
          </VoltButton>
          <VoltButton :to="`/forums/${$route.params.id}`" color="warning">
            Cancel
          </VoltButton>
        </div>
      </template>
    </VoltCard>

    <!-- Modal -->
    <VoltDialog v-model:visible="showSchedulingModal" width="500">
      <VoltDatePicker />
      <VoltDatePicker />

      <VoltButton color="primary" block @click="showSchedulingModal=false">
        Cancel
      </VoltButton>
      <VoltButton color="primary" block @click="() => create">
        Create
      </VoltButton>
    </VoltDialog>
  </section>
</template>

<script setup lang="ts">
import { useThread, useCreatePoll, useSearchTags } from '~/composables/use/thread'
import { threadTypes } from '~/data/constants/threads'

const { newThread, showSchedulingModal, previewThreadTitle, create } = await useThread()
const { newPoll } = useCreatePoll(newThread)
const { searchComplete, search, tags } = await useSearchTags(newThread)

useHead({
  title: 'Create a new thread'
})
</script>
