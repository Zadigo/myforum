<template>
  <volt-dialog v-model:visible="searchModal" class="md:w-[400px]" modal>
    <div v-if="newSearch" class="space-y-3">
      <volt-input-text v-model="newSearch.q" type="search" class="w-full" placeholder="Search" @keypress.enter="handleGoToSearch" />

      <volt-label label-for="titles-only" label="Search titles only">
        <volt-toggle-switch v-model="newSearch.title_only" />
      </volt-label>

      <volt-button rounded @click="showAdvancedSearch=!showAdvancedSearch">
        Advanced search
        <icon :name="showAdvancedSearch ? 'i-lucide:arrow-up' : 'i-lucide:arrow-down'" />
      </volt-button>

      <div v-if="showAdvancedSearch">
        <volt-divider />

        <!-- Poster -->
        <div class="py-3">
          <volt-input-text v-model="newSearch.posted_by" class="w-full" type="search" placeholder="Posted by" @keypress.enter="handleGoToSearch" />

          <div class="mt-2">
            <volt-button size="small" class="me-2" @click="() => showFromDatePicker = true">
              <span>From</span>
              <span v-if="newSearch.from_date">: {{ newSearch.from_date }}</span>
            </volt-button>

            <volt-button size="small" @click="() => showToDatePicker = true">
              <span>To</span>
              <span v-if="newSearch.to_date">: {{ newSearch.to_date }}</span>
            </volt-button>
          </div>
        </div>

        <!-- Forums -->
        <div class="py-3">
          <volt-auto-complete v-model="newSearch.search_in_forums" :suggestions="['1', '2']" placeholder="Search in forums..." @complete="() => {}" />

          <volt-label label-for="include-subforums" label="Include sub-forums in search">
            <volt-toggle-switch v-model="newSearch.sub_forums" />
          </volt-label>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="space-x-3">
        <volt-secondary-button @click="searchModal = false">
          Close
        </volt-secondary-button>

        <volt-button @click="handleGoToSearch">
          <icon name="i-lucide:search" />
          Search
        </volt-button>
      </div>
    </template>

    <!-- From Date -->
    <volt-dialog v-model:visible="showFromDatePicker">
      <volt-date-picker v-if="newSearch" v-model="newSearch.from_date" show-button-bar />
    </volt-dialog>

    <!-- To Date -->
    <volt-dialog v-model:visible="showToDatePicker">
      <volt-date-picker v-if="newSearch" v-model="newSearch.to_date" />
    </volt-dialog>
  </volt-dialog>
</template>

<script setup lang="ts">
const { newSearch } = useSearchComposable()
/**
 * Modals
 */

const searchModal = useState<boolean>('searchModal')

const route = useRoute()
const router = useRouter()

const { $dayjs } = useNuxtApp()

// const searchHistory = useStorage<string[]>('searchHistory', [])

const showAdvancedSearch = ref<boolean>(false)
const showToDatePicker = ref<boolean>(false)
const showFromDatePicker = ref<boolean>(false)

const currentDate = $dayjs().format('YYYY-MM-DD')

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
  searchModal.value = false
  // searchHistory.value.push(last.value.snapshot)

  if (route.path === '/search') {
    // Do something
  }

  router.push({
    path: '/search',
    query: newSearch?.value
  })
}
</script>
