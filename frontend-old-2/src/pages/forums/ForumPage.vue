<template>
  <base-forum-layout-vue v-if="store.currentForum">
    <template #header>
      <forum-header-vue />
    </template>

    <template #default>
      <section class="threads">
        <div class="row">
          <div class="col-12 d-flex justify-content-between align-items-center my-3">
            <div class="d-flex justify-content-start align-items-center gap-2" style="width: 200px;">
              <!-- Sorting -->
              <v-btn id="sort" color="primary" variant="tonal">
                <font-awesome-icon :icon="['fas', 'sort']"></font-awesome-icon>
              </v-btn>

              <v-menu activator="#sort">
                <v-list>
                  <v-list-item v-for="(method, index) in sortMethods" :key="method.name" :value="index" @click="sortThreads(index)">
                    <v-list-item-title>{{ method.name }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>

              <!-- Filtering -->
              <v-btn id="filter" color="primary" variant="tonal">
                <font-awesome-icon :icon="['fas', 'filter']"></font-awesome-icon>
              </v-btn>

              <v-menu activator="#filter">
                <v-list>
                  <v-list-item v-for="(category, index) in categories" :key="category" :value="index">
                    <v-list-item-title>{{ category.name }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>

            <!-- Pagination -->
            <base-pagination />
          </div>

          <!-- Threads -->
          <suspense>
            <async-threads-list />
          </suspense>
        </div>
      </section>
    </template>
  </base-forum-layout-vue>

  <div v-else class="container my-5">
    <div class="row">
      <div class="col-sm-12 col-md-8 offset-md-2">
        <div class="card my-2">
          <!-- <img :src="'../../../assets/town.png'" alt=""> -->
          <div class="card-body text-center">
            <h3 class="card-title">This website has no active threads</h3>
            
            <router-link :to="{ name: 'forums_view' }" class="btn btn-lg btn-primary my-3">
              <i class="mdi mdi-refresh mdi-24px me-2 lh-1"></i>
              Back to forums
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'
import { defineAsyncComponent } from 'vue'
import { dayjs } from '@/plugins'

import { storeToRefs } from 'pinia'
import { useForum } from '@/stores//forum'
import { useMessages } from '@/stores//messages'

import BasePagination from '../../layouts/BasePagination.vue'
import BaseForumLayoutVue from '../../layouts/BaseForumLayout.vue'
import ForumHeaderVue from '../../components/forums/ForumHeader.vue'

const sortMethods = [
  {
    name: 'Sort alphabetically A-Z'
  },
  {
    name: 'Sort alphabetically Z-A'
  },
  {
    name: 'Most recent'
  },
  {
    name: 'Number of comments'
  }
]

export default {
  name: 'ForumView',
  components: {
    BaseForumLayoutVue,
    BasePagination,
    ForumHeaderVue,
    AsyncThreadsList: defineAsyncComponent({
      loader: () => import('@/components/forum/ThreadsList.vue')
    })
  },
  setup () {
    const store = useForum()
    const messagesStore = useMessages()
    const { threads, currentForum } = storeToRefs(store)

    return {
      store,
      messagesStore,
      threads,
      currentForum
    }
  },
  data () {
    return {
      sortingMethod: 'Created on',
      categoryMethod: 'All',
      sortMethods
    }
  },
  computed: {
    hasThreads () {
      return this.threads.length > 0
    },
    categories () {
      const results = _.uniq(_.map(this.threads, (thread) => {
        return thread.category
      })).sort((a, b) => {
        return b - a
      })

      results.push('All')

      return _.map(results, (result) => {
        return { name: result }
      })
    }
  },
  created () {
    if (this.store.forums.length === 0) {
      this.store.loadFromCache()
    }
    this.store.setCurrentForum(this.$route.params.id)
  },
  beforeMount () {
    const forumId = this.$route.params.id
    // Get the previous sorting method for the Threads
    //  for this specific forum that was previously
    //  selected by the user 
    const sortingMethod = this.$session.dictGet('threads_parameters', forumId)
    this.getThreads(forumId, sortingMethod?.sort)
  },
  methods: {
    async getThreads (id, sort = 0) {
      // Return all the threads for the
      // given forum
      try {
        const response = await this.$http.get(`/forums/${id}`, { params: { sort } })
        this.store.$patch((state) => {
          state.threads = response.data
          this.$session.dictSet('threads_parameters', this.currentForum.id, {
            sort
          })
          // Save any retrieval of threads so that
          // they can eventually be queried back
          // at a latter stage
          this.$session.create('threads', state.threads)
        })
      } catch (e) {
        this.messagesStore.addErrorMessage(e.response)
      }
    },
    async sortThreads (index) {
      // Handles the sorting action for the threads
      await this.getThreads(this.$route.params.id, index)
    },
    formatDate (d) {
      return dayjs(d).format('MMM, DD YYYY')
    },
    formatDuration (d) {
      const creationDate = dayjs(d)
      const currentDate = dayjs()
      return dayjs.duration(creationDate.diff(currentDate)).humanize(true)
    }
  }
}
</script>
