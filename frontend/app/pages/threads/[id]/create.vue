<template>
  <section id="create-thread" class="my-5">
    <volt-card class="shadow-sm">
      <template #content>
        <form id="creation" @submit.prevent>
          <!-- Thread Type -->
          <VoltSelect v-model="newThread.category" :options="threadTypes" label="Select" class="w-6/12" />

          <!-- Title -->
          <div v-if="newThread.category === 'General discussion' || newThread.category === 'Poll'" class="my-3">
            <volt-input-text v-model="newThread.title" placeholder="Title" class="w-full" />
          </div>
          <ThreadsCreateResultEditor v-else-if="newThread.category === 'Result'" v-model="newThread" :preview-thread-title="previewThreadTitle" />
          
          <!-- Base editor -->
          <base-editor @editor-content="(data) => newThread.content = data" />

          <!-- Notifications -->
          <volt-label label-for="notifications" class="my-4">
            <VoltToggleSwitch v-model="newThread.watch" />
            <label>Watch this discussion</label>
          </volt-label >

          <volt-message v-if="newThread.watch" severity="warn" class="my-3">
            You will be receiving notifications on each new post and interraction
            for your newly created thread
          </volt-message>

          <!-- Tags -->
          <volt-auto-complete v-model="search" :suggestions="tags" input-id="multiple-tags" placeholder="Select multiple tags" class="my-4 w-full" multiple fluid @complete="searchComplete" />

          <!-- Poll -->
          <div id="poll">
            <volt-toggle-button v-model="newThread.add_poll" on-label="Remove poll" off-label="Add poll" />
            <threads-create-poll v-if="newThread.add_poll" v-model="newPoll" />
          </div>
        </form>
      </template>

      <template #footer>
        <div class="space-x-2 py-5">
          <volt-button @click="() => create">
            Create
          </volt-button>
          <volt-button @click="showSchedulingModal=true">
            Schedule
          </volt-button>
          <volt-button @click="() => create">
            Save draft
          </volt-button>
          <volt-button>
            Preview
          </volt-button>
          <volt-button :to="`/forums/${$route.params.id}`">
            Cancel
          </volt-button>
        </div>
      </template>
    </volt-card>

    <!-- Modal -->
    <volt-dialog v-model:visible="showSchedulingModal" modal>
      <VoltDatePicker class="w-full" />

      <template #footer>
        <volt-secondary-button color="primary" block @click="showSchedulingModal=false">
          Cancel
        </volt-secondary-button>
  
        <volt-button color="primary" block @click="() => create">
          Schedule
        </volt-button>
      </template>
    </volt-dialog>
  </section>
</template>

<script setup lang="ts">
import { useThread, useCreatePoll, useSearchTags } from '~/composables/use/thread'
import { threadTypes } from '~/data/constants/threads'

definePageMeta({
  name: 'Create Thread'
})

const { newThread, showSchedulingModal, previewThreadTitle, create } = await useThread()
const { newPoll } = useCreatePoll(newThread)
const { searchComplete, search, tags } = await useSearchTags(newThread)

useHead({
  title: 'Create a new thread'
})
</script>
