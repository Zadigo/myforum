<template>
  <VoltDialog v-model:visible="forumStore.openSearchModal" @close="forumStore.openSearchModal=false">
    <div>
      <VoltInputText v-model="search" type="search" placeholder="Search" @keypress.enter="handleGoToSearch" />
      <VoltToggleSwitch v-model="requestData.search_titles_only" label="Search titles only" inset />

      <VoltButton rounded @click="showAdvancedSearch=!showAdvancedSearch">
        Advanced search
        <icon name="i-lucide:arrow-down" />
      </VoltButton>

      <div v-if="showAdvancedSearch">
        <!-- Poster -->
        <div class="py-3">
          <VoltInputText v-model="requestData.posted_by" type="search" placeholder="Posted by" @keypress.enter="handleGoToSearch" />

          <div class="mt-2">
            <VoltButton class="me-2" @click="() => showFromDatePicker = true">
              <span>From</span>
              <span v-if="requestData.from_date">: {{ requestData.from_date }}</span>
            </VoltButton>
            
            <VoltButton @click="() => showToDatePicker = true">
              <span>To</span>
              <span v-if="requestData.to_date">: {{ requestData.from_date }}</span>
            </VoltButton>
          </div>
        </div>

        <!-- Forums -->
        <div class="py-3">
          <VoltAutoComplete v-model="requestData.search_in_forums" :suggestions="['1', '2']" placeholder="Search in forums..." @complete="() => {}" />
          <VoltToggleSwitch v-model="requestData.include_subforums" label="Include sub-forums in search" inset />
        </div>
      </div>
    </div>

    <div>
      <VoltButton @click="forumStore.openSearchModal=false">
        Close
      </VoltButton>

      <VoltButton @click="handleGoToSearch">
        Search
      </VoltButton>
    </div>

    <VoltDialog v-model:visible="showFromDatePicker">
      <VoltDatePicker v-model="requestData.to_date" />
    </VoltDialog>

    <VoltDialog v-model:visible="showToDatePicker">
      <VoltDatePicker v-model="requestData.to_date" />
    </VoltDialog>
  </VoltDialog>
</template>

<script setup lang="ts">
import { useRefHistory, useStorage, useUrlSearchParams } from '@vueuse/core'

interface RequestData {
  search: string,
  search_titles_only: boolean,
  posted_by: string,
  from_date: string,
  to_date: string,
  search_in_forums: string[],
  include_subforums: boolean,
}

// const rules = {
//   searchRule: (value: string) => !!value || 'Field is required'
// }

const route = useRoute()
const router = useRouter()

const forumStore = useForums()
const { $dayjs } = useNuxtApp()

const searchHistory = useStorage<string[]>('searchHistory', [])

const searchParams = useUrlSearchParams('history')

const showAdvancedSearch = ref<boolean>(false)
const showToDatePicker = ref<boolean>(false)
const showFromDatePicker = ref<boolean>(false)

const search = ref<string>('')
const { last } = useRefHistory<string>(search)

const requestData = ref<RequestData>({
  search: search.value,
  search_titles_only: false,
  posted_by: '',
  from_date: '',
  to_date: '',
  search_in_forums: [],
  include_subforums: false
})

const currentDate = $dayjs().format('YYYY-MM-DD')

watch(search, (value) => {
  searchParams.q = value
})

/**
 *
 */
function saveSearch () {
  console.log('saveSearch')
}

/**
 *
 */
function handleGoToSearch () {
  forumStore.openSearchModal = false
  searchHistory.value.push(last.value.snapshot)

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
