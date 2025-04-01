<template>
  <keep-alive>
    <base-forum-layout-vue>
      <template #header>
        <thread-header-vue @new-comment="showCreateCommentForm = true" @jump-to-latest="handleJumpToLastPost" @delete="deleteThread" />
      </template>

      <template #aside>
        <thread-aside-vue :number-of-comments="cachedComments.count" />
      </template>

      <section id="comments">
        <!-- Editor -->
        <div v-if="showCreateCommentForm" class="row">
          <div class="col-12">
            <div class="card">
              <div class="card-body">
                <v-text-field v-model="requestData.title" type="text" placeholder="Title" variant="outlined"></v-text-field>
                <base-editor @editor-content="handleEditorContent" />

                <div v-for="quote in requestData.quotes" :key="quote" class="alert alert-info">
                  {{ quote }}
                </div>
              </div>

              <div class="card-actions text-right">
                <div class="btn-group">
                  <button type="button" class="btn btn-primary" @click="createNewPost">
                    Post
                  </button>
                  <button type="button" class="btn btn-info" @click="saveDraft">
                    Save draft
                  </button>
                  <button type="button" class="btn btn-info" @click="handleCancel">
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="row">
          <!-- Poll -->
          <suspense>
            <async-poll-section class="mb-5" />
          </suspense>

          <!-- <keep-alive>
            <async-poll-section-vue class="mb-5" />
          </keep-alive> -->

          <div class="col-12">
            <div class="row">
              <div class="col-12 d-flex justify-content-between mb-3">
                <!-- <span class="text-muted">{{ countPhrase }}</span> -->
                <!-- <base-pagination-vue :pages="cachedComments.pages" :sync-current-page="syncCurrentPage" @page-click="getComments" /> -->
                <base-pagination-vue :pages="cachedComments.pages" @page-click="getComments"
                />
              </div>

              <!-- Comments -->
              <iterator-comments-vue :comments="comments" @reply="handleReply" />

              <div class="col-12 d-flex justify-content-end mt-3">
                <base-pagination-vue :pages="cachedComments.pages" :sync-current-page="syncCurrentPage" @page-click="getComments"
                />
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
</template>

<script>
import _ from "lodash"
import { ref, defineAsyncComponent } from "vue"
import { useForum } from "@/stores//forum"
import { useMessages } from "@/stores//messages"
import { useUtilities } from "@/composables/utils"

import BaseEditor from "@/layouts/BaseEditor.vue"
import BasePaginationVue from "../../layouts/BasePagination.vue"
import BaseForumLayoutVue from "../../layouts/BaseForumLayout.vue"
import IteratorCommentsVue from "../../components/threads/IteratorComments.vue"
import ThreadAsideVue from "../../components/threads/ThreadAside.vue"
import ThreadHeaderVue from "../../components/threads/ThreadHeader.vue"

export default {
  name: "CommentsView",
  components: {
    BaseEditor,
    BasePaginationVue,
    BaseForumLayoutVue,
    IteratorCommentsVue,
    ThreadAsideVue,
    ThreadHeaderVue,
    AsyncPollSection: defineAsyncComponent({
      loader: () => import("../../components/threads/PollSection.vue"),
    }),
  },
  beforeRouteLeave(to, from, next) {
    // From the above, we should not be able to
    // fall on the page number of a previous
    // thread if we happen to change thread
    this.$session.create("currentPage", 1)
    next()
  },
  props: {},
  setup() {
    const store = useForum()
    const messagesStore = useMessages()
    const { listManager } = useUtilities()
    const requestData = ref({
      title: null,
      content: null,
      content_delta: null,
      content_html: null,
      draft: false,
      quotes: [],
    })
    return {
      store,
      messagesStore,
      requestData,
      listManager,
    }
  },
  data() {
    return {
      cachedComments: {},
      comments: [],
      showCreateCommentForm: false,
      syncCurrentPage: 1,
    }
  },
  computed: {
    countPhrase() {
      var firstComment = _.first(this.comments)
      var lastComment = _.last(this.comments)
      return `${firstComment.id} - ${lastComment.id} of ${this.cachedComments.count} posts`
    },
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
    } catch (error) {
      console.error(error)
    }
  },
  beforeMount() {
    // When reloading the page, if the user was viewing for ex.
    // page 3, it loads back to page 1. This corrects that.
    let existingCurrentPage = this.$session.retrieve("currentPage")

    existingCurrentPage = existingCurrentPage || 1
    this.getComments(existingCurrentPage)
  },
  mounted() {
    this.$session.incrementDictKeyBy("viewCounts", this.store.currentThread.id)
    // this.$session.listPushUnique('history', this.store.currentThread.title)
  },
  methods: {
    async getComments(page = 1) {
      // Return the comments for the current
      // visited thread
      try {
        const currentThreadId = this.store.currentThread.id
        this.syncCurrentPage = page

        const response = await this.$http.get(`threads/${currentThreadId}/comments`, {
          params: { page: page },
        })
        this.cachedComments = response.data
        this.comments = response.data.results
        this.$session.create("comments", this.comments)
      } catch (e) {
        this.messagesStore.addErrorMessage(e.response.data)
      }
    },
    async createNewPost() {
      try {
        const currentThreadId = this.store.currentThread.id
        const response = await this.$http.post(`comments/create`, {
          thread: currentThreadId,
          ...this.requestData,
        })
        this.comments.push(response.data)
        this.showCreateCommentForm = false
        this.reset()
      } catch (e) {
        console.error(e)
        this.messagesStore.addErrorMessage(e.response.data)
      }
    },
    async saveDraft() {
      this.requestData.draft = true
      await this.createNewPost()
    },
    async deleteThread() {
      try {
        await this.$http.delete(`/threads/${this.store.currentThread.id}/delete`)
        this.$router.push({ name: "forums_view" })
      } catch (e) {
        this.messagesStore.addErrorMessage("Could not delete thread. An error occured.")
      }
    },
    handleEditorContent(data) {
      // Sets the Quill content to the final
      // request data for the API
      this.requestData.content = data.text
      this.requestData.content_delta = data.delta
      this.requestData.content_html = data.html
    },
    handleCancel() {
      // Handle the action where the user decides
      // to finally not create the comment
      this.reset()
      this.showCreateCommentForm = false
    },
    handleReply(comment) {
      // Sets the selected comment to reply to as a Quote
      // and then opens the comment form
      this.listManager(this.requestData.quotes, comment.id)
      this.showCreateCommentForm = true
    },
    handleJumpToLastPost() {
      // Jump to the last post of the thread. We have
      // to query the last page and once we have it
      // scroll down to the comment
      this.getComments(this.cachedComments.pages)

      const lastComment = _.last(this.comments)
      const itemId = `#post-${lastComment.id}`
      const commentOject = document.querySelector(itemId)

      commentOject.scrollIntoView({ block: "start", inline: "nearest" })
    },
    reset() {
      this.requestData = {
        title: null,
        content: null,
        content_html: null,
        draft: false,
        quotes: [],
      }
    },
  },
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
