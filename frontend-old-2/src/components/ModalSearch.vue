<template>
  <v-dialog v-model="store.openSearchModal" width="600" @close="store.openSearchModal">
    <v-card>
      <v-card-text>
        <v-text-field v-model="requestData.search" :rules="[rules.searchRule]" type="search" variant="outlined" placeholder="Search" aria-placeholder="Search" hint="Search titles, keywords..." @keypress.enter="handleGoToSearch"></v-text-field>
        <v-switch v-model="requestData.search_titles_only" label="Search titles only" inset></v-switch>

        <v-btn variant="tonal" rounded @click="showAdvancedSearch = !showAdvancedSearch">
          Advanced search
          <font-awesome-icon :icon="['fas', 'arrow-down']"></font-awesome-icon>
        </v-btn>

        <div v-if="showAdvancedSearch">
          <!-- Poster -->
          <div class="py-3">
            <v-text-field v-model="requestData.posted_by" type="search" variant="outlined" placeholder="Posted by" aria-placeholder="Posted by" @keypress.enter="handleGoToSearch"></v-text-field>

            <div class="mt-2">
              <v-btn class="me-2" variant="tonal" rounded>
                <span>From</span>
                <span v-if="requestData.from_date">: {{ requestData.from_date }}</span>
    
                <v-dialog v-model="showFromDatePicker" activator="parent" width="auto">
                  <v-card>
                    <v-card-text>
                      <v-date-picker v-model="requestData.to_date" elevation="0"></v-date-picker>
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
                      <v-date-picker v-model="requestData.to_date" :max="currentDate" elevation="0"></v-date-picker>
                    </v-card-text>
                  </v-card>
                </v-dialog>
              </v-btn>
            </div>
          </div>

          <!-- Forums -->
          <div class="py-3">
            <v-autocomplete v-model="requestData.search_in_forums" :items="['1', '2']" placeholder="Search in forums..." clearable multiple></v-autocomplete>
            <v-switch v-model="requestData.include_subforums" label="Include sub-forums in search" inset></v-switch>
          </div>
        </div>
      </v-card-text>

      <v-card-actions>
        <v-btn color="primary" @click="store.openSearchModal = false">Close</v-btn>
        <v-btn color="primary" @click="handleGoToSearch">Search</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import _ from 'lodash'
import { dayjs } from '@/plugins'
import { useForum } from '@/stores//forum'
import { ref } from 'vue'

export default {
  name: 'ModalSearch',
  setup () {
    const store = useForum()
    const showAdvancedSearch = ref(false)
    const searchHistory = ref([])
    const showFromDatePicker = ref(false)
    const rules = {
      searchRule: value => !!value || 'Field is required'
    }
    const requestData = ref({
      search: null,
      search_titles_only: false,
      posted_by: null,
      from_date: null,
      to_date: null,
      search_in_forums: [],
      include_subforums: false,
    })
    return {
      requestData,
      showAdvancedSearch,
      searchHistory,
      showFromDatePicker,
      rules,
      dayjs,
      store
    }
  },
  computed: {
    currentDate () {
      return this.dayjs().format('YYYY-MM-DD')
    }
  },
  beforeMount () {
    this.searchHistory = _.uniq(this.$session.retrieve('query'))
  },
  methods: {
    saveSearch () {
      console.log('saveSearch')
    },
    deleteSearch (index) {
      index
      // var history = this.$session.retrieve('query')
      // history.splice()
      // this.$session.create('query', history)
    },
    handleGoToSearch () {
      this.$session.listPush('query', this.search)
      this.$router.push({ name: 'search_view', query: { q: this.search } })
      this.$session.create('search', this.requestData)
      this.search = null
      this.store.openSearchModal = false
    }
  }
}
</script>
