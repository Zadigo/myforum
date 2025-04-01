<template>
  <v-dialog v-model="forumStore.openSearchModal" width="600" @close="forumStore.openSearchModal=false">
    <v-card>
      <v-card-text>
        <v-text-field v-model="search" :rules="[rules.searchRule]" type="search" variant="outlined" placeholder="Search" aria-placeholder="Search" hint="Search titles, keywords..." @keypress.enter="handleGoToSearch" />
        <v-switch v-model="requestData.search_titles_only" label="Search titles only" inset />

        <v-btn variant="tonal" rounded @click="showAdvancedSearch=!showAdvancedSearch">
          Advanced search
          <font-awesome icon="arrow-down" />
        </v-btn>

        <div v-if="showAdvancedSearch">
          <!-- Poster -->
          <div class="py-3">
            <v-text-field v-model="requestData.posted_by" type="search" variant="outlined" placeholder="Posted by" aria-placeholder="Posted by" @keypress.enter="handleGoToSearch" />

            <div class="mt-2">
              <v-btn class="me-2" variant="tonal" rounded>
                <span>From</span>
                <span v-if="requestData.from_date">: {{ requestData.from_date }}</span>
    
                <v-dialog v-model="showFromDatePicker" activator="parent" width="auto">
                  <v-card>
                    <v-card-text>
                      <v-date-picker v-model="requestData.to_date" elevation="0" />
                    </v-card-text>
                  </v-card>
                </v-dialog>
              </v-btn>
              
              <v-btn variant="tonal" rounded>
                <span>To</span>
                <span v-if="requestData.to_date">: {{ requestData.from_date }}</span>
    
                <v-dialog v-model="showFromDatePicker" activator="parent" width="auto">
                  <v-card>
                    <v-card-text>
                      <v-date-picker v-model="requestData.to_date" :max="currentDate" elevation="0" />
                    </v-card-text>
                  </v-card>
                </v-dialog>
              </v-btn>
            </div>
          </div>

          <!-- Forums -->
          <div class="py-3">
            <v-autocomplete v-model="requestData.search_in_forums" :items="['1', '2']" variant="solo-filled" placeholder="Search in forums..." flat clearable multiple />
            <v-switch v-model="requestData.include_subforums" label="Include sub-forums in search" inset />
          </div>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" @click="forumStore.openSearchModal=false">
          Close
        </v-btn>

        <v-btn color="primary" @click="handleGoToSearch">
          Search
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import { useRefHistory, useSessionStorage } from '@vueuse/core';

interface RequestData {
  search: string,
  search_titles_only: boolean,
  posted_by: string,
  from_date: string,
  to_date: string,
  search_in_forums: string[],
  include_subforums: boolean,
}

const forumStore = useForums()
const showAdvancedSearch = ref(false)
const showFromDatePicker = ref(false)
const rules = {
  searchRule: (value: string) => !!value || 'Field is required'
}
const search = ref<string>('')
const requestData = ref<RequestData>({
  search: search.value,
  search_titles_only: false,
  posted_by: '',
  from_date: '',
  to_date: '',
  search_in_forums: [],
  include_subforums: false
})

const { $dayjs } = useNuxtApp()
const { history, last } = useRefHistory(search)
const searchHistory = useSessionStorage<string[]>('searchHistory', [], {
  serializer: {
    read (raw) {
      return JSON.parse(raw)
    },
    write (value) {
      return JSON.stringify(value)
    }
  }
})
const currentDate = $dayjs().format('YYYY-MM-DD')

const route = useRoute()
const router = useRouter()

function saveSearch () {
  console.log('saveSearch')
}

function handleGoToSearch () {
  forumStore.openSearchModal = false
  searchHistory.value = history.value

  if (route.path === '/search') {
    // Do something
  }
  router.push({
    path: '/search',
    query: {
      q: search.value
    }
  })
  search.value = ''
}
</script>
