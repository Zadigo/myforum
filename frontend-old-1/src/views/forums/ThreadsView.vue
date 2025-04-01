<template>
  <base-forum-layout-vue v-if="store.currentForum">
    <template #header>
      <forum-header-vue />
    </template>

    <template #default>
      <section class="threads">
        <div class="row">
          <!-- <div class="col-12 d-flex justify-content-between my-3">
            <div id="d-flex justify-content-around">
              <dropdown-button-vue :items="sortMethods" icon="sort" button-name="Sort" @dropdown-click="doSort" />
              <dropdown-button-vue :items="categories" icon="filter" button-name="Filter" />
            </div>
            <base-pagination />
          </div> -->

          <div class="col-12">
            <article v-for="(thread, i) in sortedItems" :key="thread.id" :class="{ 'mt-1': i > 0 }" role="article" @click="store.setCurrentThread(thread)">
              <!-- <router-link :to="{ name: 'thread_comments_view', params: { id: currentForum.id, thread: thread.id } }" class="text-dark"> -->
              <router-link :to="{ name: 'thread_comments_view', params: { id: thread.id } }" class="text-dark">
                <div :aria-label="thread.title" class="card">
                  <div class="card-body">
                    <h3 class="card-title">
                      <!-- <b-avatar src="http://via.placeholder.com/200x200" height="50" width="50" /> -->
                      {{ thread.title }}
                    </h3>

                    <!-- <v-card-subtitle>
                      <v-chip v-if="thread.type == 'Result'" color="blue" small label>{{ thread.type }}</v-chip> by {{ thread.user.username}} on the 01 Feb 2022
                    </v-card-subtitle> -->

                    <div class="card-text my-2">
                      {{ thread.description }}
                      <!-- <v-slide-group multiple show-arrows center-active>
                        <v-slide-item v-for="tag in thread.tags" :key="tag.name" v-slot="{ active, toggle }">
                          <v-btn :input-value="active" active-class="purple white--text" class="mx-2" depressed rounded @click="toggle">
                            {{ tag.name }}
                          </v-btn>
                        </v-slide-item>
                      </v-slide-group> -->
                    </div>

                    <div class="card-info">
                      <span class="badge bg-light text-dark p-2"><span class="mdi mdi-comment ms-2" /> {{
                        thread.number_of_comments }}</span>
                      <span class="badge bg-light text-dark p-2 ms-2"><span class="mdi mdi-calendar ms-2" /> {{
                        formatDate(thread.created_on) }}</span>
                      <span class="badge bg-light text-dark p-2 ms-2">{{
                        formatDuration(thread.latest_comment.created_on) }}</span>
                    </div>
                  </div>
                </div>
              </router-link>
            </article>
          </div>
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
import { useForum } from '@/stores//forum'
import { storeToRefs } from 'pinia'
import dayjs from '../../plugins/dayjs'
import _ from 'lodash'

import BasePagination from '../../layouts/BasePagination.vue'
import BaseForumLayoutVue from '../../layouts/BaseForumLayout.vue'
import DropdownButtonVue from '../../layouts/DropdownButton.vue'
import ForumHeaderVue from '../../components/forums/ForumHeader.vue'
import { useMessages } from '@/stores//messages'

export default {
  name: 'ThreadsView',
  setup () {
    var store = useForum()
    var messagesStore = useMessages()
    var { threads, currentForum } = storeToRefs(store)

    return {
      store,
      messagesStore,
      threads,
      currentForum
    }
  },
  components: {
    BaseForumLayoutVue,
    DropdownButtonVue,
    ForumHeaderVue,
    BasePagination
  },
  data: () => ({
    sortingMethod: 'Created on',
    sortMethods: [
      {
        name: 'Sort alphabetically A-Z'
      },
      {
        name: 'Sort alphabetically Z-A'
      },
      {
        name: 'Creation date'
      },
      {
        name: 'Number of comments'
      }
    ]
  }),
  computed: {
    hasThreads () {
      return this.threads.length > 0
    },
    categories () {
      const results = _.sortedUniq(_.map(this.threads, (thread) => {
        return thread.category
      }))

      results.push('All')

      return _.map(results, (result) => {
        return { name: result }
      })
    },
    sortedItems () {
      var items = []

      switch (this.sortingMethod) {
        case 'Sort alphabetically A-Z':
          items = _.sortBy(this.threads, ['title'], ['asc'])
          break

        case 'Sort alphabetically Z-A':
          items = _.sortBy(this.threads, ['title'], ['desc'])
          break;

        case 'Creation date':
          items = this.threads.sort((a, b) => {
            return dayjs(b['created_on']) - dayjs(a['created_on'])
          })
          break

        case 'Number of comments':
          items = this.threads.sort((a, b) => {
            return b['number_of_comments'] - a['number_of_comments']
          })
          break

        default:
          items = this.threads
          break
      }

      return items
    }
  },
  created () {
    if (this.store.forums.length == 0) {
      this.store.loadFromCache()
    }
    this.store.setCurrentForum(this.$route.params.id)
  },
  beforeMount () {
    this.getThreads(this.$route.params.id)
  },
  methods: {
    async getThreads (id) {
      // Get all the threads for the given forum
      try {
        const response = await this.$http.get(`/forums/${id}`)
        this.store.$patch((state) => {
          state.threads = response.data
          // Save any retrieval of threads so that
          // they can eventually be retrieved back
          // at a latter stage
          this.$session.create('threads', state.threads)
        })
      } catch (error) {
        this.messagesStore.addErrorMessage(error.response.data)
      }
    },
    formatDate (d) {
      return dayjs(d).format('MMM, DD YYYY')
    },
    formatDuration (d) {
      const creationDate = dayjs(d)
      const currentDate = dayjs()
      return dayjs.duration(creationDate.diff(currentDate)).humanize(true)
    },
    doSort (item) {
      this.sortingMethod = item.name
    }
  }
}
</script>
