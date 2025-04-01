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
          <iterator-comments-vue :comments="searchResult.comments || []" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { useMessages } from '../store/messages'
import IteratorCommentsVue from '../components/threads/IteratorComments.vue'

export default {
  name: 'SearchView',
  setup() {
    var messagesStore = useMessages()
    return {
      messagesStore
    }
  },
  components: {
    IteratorCommentsVue
  },
  data: () => ({
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
  }),
  beforeMount() {
    this.getSearch()
  },
  methods: {
    async getSearch() {
      try {
        var response = await this.$http.post('/search', { q: this.$route.query['q'] })
        this.searchResult = response.data
      } catch(error) {
        this.messagesStore.addErrorMessage('Could not get search')
      }
    }
  }
}
</script>
