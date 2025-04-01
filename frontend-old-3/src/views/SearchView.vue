<template>
  <section id="search" class="my-5">
    <div class="container">
      <div class="row">
        <div class="col-12 mb-3">
          <ul class="nav nav-pills">
            <li v-for="link in links" :key="link.name" class="nav-item">
              <a :class="{ active: currentPage === link.name }" href class="nav-link" aria-current="page" @click.prevent="currentPage=link.name">
                {{ link.name }}
              </a>
            </li>
          </ul>
        </div>

        <div class="col-sm-12 col-md-9">
          <!-- Comments -->
          <iterator-comments :comments="searchResult.comments || []" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
// import { ref } from 'vue'
import { useMessages } from '../store/messages'
import IteratorComments from '../components/threads/IteratorComments.vue'

export default {
  name: 'SearchView',
  components: {
    IteratorComments
  },
  setup() {
    const messagesStore = useMessages()
    const requestData = {}
    return {
      requestData,
      messagesStore
    }
  },
  data () {
    return {
      searchResult: {},
      currentPage: 'Comments',
      links: [
        {
          name: 'Comments',
          active: true
        },
        {
          name: 'Showcase',
          active: false
        },
        {
          name: 'Albums',
          active: false
        },
        {
          name: 'Media',
          active: false
        },
        {
          name: 'Tags',
          active: false
        }
      ]
    }
  },
  created () {
    this.requestData = this.$session.retrieve('search') || {}
  },
  beforeMount() {
    this.getSearch()
  },
  methods: {
    async getSearch() {
      // Returns the search results
      try {
        const response = await this.$http.post('/search', {
          q: this.requestData.search
        })
        this.searchResult = response.data
      } catch(e) {
        this.messagesStore.addErrorMessage(e.response.data)
      }
    }
  }
}
</script>
