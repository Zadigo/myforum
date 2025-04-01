<template>
  <keep-alive>
    <base-forum-layout-vue>
      <template #header>
        <thread-header-vue @new-comment="createCommentForm=true" @jump-to-latest="jumpToLast" @delete="deleteThread" />
      </template>

      <template #aside>
        <thread-aside-vue :number-of-comments="cachedComments.count" />
      </template>

      <section id="comments">
        <!-- Editor -->
        <div v-if="createCommentForm" class="row">
          <div class="col-12">
            <div class="card">
              <div class="card-body">
                <input v-model="newPost.title" type="text" class="form-control p-3" placeholder="Title">
                <!-- <base-editor-vue @editorContent="setContent" /> -->
                <textarea v-model="newPost.content" cols="30" rows="10" class="form-control my-2"></textarea>

                <div v-for="quote in newPost.quotes" :key="quote" class="alert alert-info">
                  {{ quote }}
                </div>
              </div>

              <div class="card-actions text-right">
                <div class="btn-group">
                  <button class="btn btn-primary" @click="createNewPost">Post</button>
                  <button class="btn btn-info" @click="saveDraft">Save draft</button>
                  <button class="btn btn-info" @click="createCommentForm=false">Cancel</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="row">
          <!-- Poll -->
          <!-- <keep-alive>
            <async-poll-section-vue class="mb-5" />
          </keep-alive> -->

          <div class="col-12">
            <div class="row">
              <div class="col-12 d-flex justify-content-between mb-3">
                <!-- <span class="text-muted">{{ countPhrase }}</span> -->
                <base-pagination-vue :pages="cachedComments.pages" :sync-current-page="syncCurrrentPage" @get-page="getComments" />
              </div>

              <!-- Comments -->
              <iterator-comments-vue :comments="comments" @reply="reply" />

              <div class="col-12 d-flex justify-content-end mt-3">
                <base-pagination-vue :pages="cachedComments.pages" :sync-current-page="syncCurrentPage" @get-page="getComments" />
              </div>
            </div>

            <div class="row">
              <div class="col-12">
                <h1 class="fw-bold display-6 my-5">Recommended reading</h1>

                <div v-for="i in 5" :key="i" class="card mb-2">
                  <div class="card-body">{{ i }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </base-forum-layout-vue>
  </keep-alive>

    <!-- <div v-else class="container my-5">
      <div class="row">
        <div class="col-sm-12 col-md-8 offset-md-2">
          <div class="card my-2">
            <div class="card-body text-center">
              <h3 class="card-title">This website has no comments</h3>
              <router-link :to="{ name: 'forums_view' }" class="btn btn-lg btn-primary my-3">
                Back to forums
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div> -->
</template>

<script>
import _ from 'lodash'
import { useForum } from '@/stores//forum'
import { useMessages } from '@/stores//messages'
import { defineAsyncComponent } from 'vue'
import { listManager } from '../../utils'

import BasePaginationVue from '../../layouts/BasePagination.vue'
import BaseForumLayoutVue from '../../layouts/BaseForumLayout.vue'
import IteratorCommentsVue from '../../components/threads/IteratorComments.vue'
// import PollSectionVue from '../../components/threads/PollSection.vue'
import ThreadAsideVue from '../../components/threads/ThreadAside.vue'
import ThreadHeaderVue from '../../components/threads/ThreadHeader.vue'

export default {
  name: 'CommentsView',
  setup() {
    const store = useForum()
    const messagesStore = useMessages()
    return {
      store,
      messagesStore
    }
  }, 
  components: {
    BasePaginationVue,
    BaseForumLayoutVue,
    IteratorCommentsVue,
    // PollSectionVue,
    ThreadAsideVue,
    ThreadHeaderVue,
    AsyncPollSectionVue: defineAsyncComponent({
      loader: () => import('../../components/threads/PollSection.vue')
    })
  },
  data () {
    return {
      cachedComments: {},
      comments: [],
      createCommentForm: false,
      newPost: {
        title: null,
        content: null,
        content_html: null,
        draft: false,
        quotes: []
      },
      syncCurrentPage: 1
    }
  },
  created() {
    // This is necessary in case the page is refreshed
    // so that we can keep track of the current thread
    // within a given forum thread's
    // TODO: If a person comes directly unto this page
    // without passing by the /forums then there would
    // be no "threads" in the session
    // TODO: If we already have a current thread
    // and forum, then skip this section
    try {
      this.store.loadFromCache()
      this.store.setCurrentThread(this.$route.params.id)
      this.store.setCurrentForum(this.store.currentThread.forum.id)
    } catch(error) {
      console.error(error)
    }
  },
  beforeMount() {
    // When reloading the page, if the user was viewing for ex.
    // page 3, it loads back to page 1. This corrects that.
    const existingCurrentPage = this.$session.retrieve('currentPage')
    
    existingCurrentPage = existingCurrentPage || 1
    this.getComments(existingCurrentPage)
  },
  mounted() {
    const viewCounts = this.$session.retrieve('viewCounts')
    viewCounts = viewCounts ? viewCounts : {}

    const currentThreadId = this.store.currentThread.id
    
    viewCounts[currentThreadId] = viewCounts[currentThreadId] ? viewCounts[currentThreadId] + 1 : 0 
    this.$session.create('viewCounts', viewCounts)
    this.$session.listPush('history', this.store.currentThread.title)
  },
  beforeRouteLeave(to, from, next) {
    // From the above, we should not be able to
    // fall on the same page number of a previous
    // thread if we happen to change thread
    this.$session.create('currentPage', 1)
    next()
  },
  computed: {
    countPhrase() {
      var firstComment = _.first(this.comments)
      var lastComment = _.last(this.comments)
      return `${firstComment.id} - ${lastComment.id} of ${this.cachedComments.count} posts`
    }
  },
  methods: {
    async getComments(page = 1) {
      try {
        var currentThreadId = this.store.currentThread.id
        this.syncCurrrentPage = page

        var response = await this.$http.get(`/threads/${currentThreadId}/comments`, { params: { page: page } })
        this.cachedComments = response.data
        this.comments = response.data.results
      } catch(error) {
        this.messagesStore.addErrorMessage(error.message)
      }
    },
    async createNewPost() {
      try {
        var response = await this.$http.post(`comments/create`, {
          thread: this.store.currentThread.id,
          ...this.newPost
        })
        this.comments.push(response.data)
        this.reset()
        this.createCommentForm = false
      } catch(error) {
        console.error(error)
      }
    },
    async saveDraft() {
      this.newPost.draft = true
      await this.createNewPost()
    },
    async deleteThread() {
      try {
        await this.$http.delete(`/threads/${this.store.currentThread.id}/delete`)
        this.$router.push({ name: 'forums_view' })
      } catch(error) {
        this.messagesStore.addErrorMessage('Could not delete thread. An error occured.')
      }
    },
    reset() {
      this.newPost = {
        title: null,
        content: null,
        content_html: null,
        draft: false,
        quotes: []
      }
    },
    reply(comment) {
      this.newPost.quotes = listManager(this.newPost.quotes, comment.id)
      this.createCommentForm = true
    },
    setContent(params) {
      this.newPost.content = params.text
      this.newPost.content_html = params.html
    },
    jumpToLast() {
      this.getComments(this.cachedComments.pages)

      var lastComment = _.last(this.comments)
      var itemId = `#post-${lastComment.id}`
      var commentOject = document.querySelector(itemId)

      commentOject.scrollIntoView()
    }
  }
}
</script>

<style scoped>
.card-actions {
  align-items: center;
  display: flex;
  padding: 8px;
}
.card-actions > .btn {
  padding: 0 8px;
}
.btn-text {
  background: transparent;
  color: inherit;
}
</style>
