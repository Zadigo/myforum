<template>
  <div id="comments">
    <article v-for="comment in comments" :id="`post-${comment.id}`" :key="comment.id" :class="{ 'bg-light mb-5': comment.initial_comment }" class="card shadow-sm mb-2">
      <div class="card-toolbar border-bottom">
        <div class="card-toolbar-content d-flex justify-content-between align-items-center">
          <span :aria-label="comment.title">{{ comment.title }}</span>

          <v-btn color="dark" variant="icon">
            <font-awesome-icon :icon="['fas', 'ellipsis-vertical']" />

            <v-menu activator="parent">
              <v-list>
                <v-list-item v-for="(item, index) in menuItems" :key="index" :value="index">
                  <!-- <font-awesome-icon :icon="['fas', 'bookmark']" /> -->
                  <v-list-item-title @click="handleMenuAction(item)">
                    {{ item }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-btn>
        </div>
      </div>

      <div class="card-body">
        <div class="mb-4">
          <span class="fw-bold text-muted">#{{ comment.id }}</span> <span class="mx-2">-</span> by <span class="fw-bold">{{ comment.user.username }}</span> <span class="text-muted">{{ formatDate(comment.created_on) }}</span>
        </div>
        <div v-html="comment.content_html"></div>
      </div>

      <div v-if="showActions" class="card-actions ms-auto ">
        <div v-if="isAuthenticated" class="d-flex gap-2">
          <v-btn color="primary" variant="tonal" @click="$emit('reply', comment)">
            <font-awesome-icon :icon="['fas', 'reply']" class="me-2" />Reply
          </v-btn>

          <v-btn color="primary" variant="tonal" @click="quoteFrom">
            <font-awesome-icon :icon="['fas', 'quote-left']" class="me-2" />Quote from
          </v-btn>
          
          <v-btn color="primary" variant="tonal" @click="bookmark">
            <font-awesome-icon v-if="comment.bookmarked_by_user" :icon="['fas', 'bookmark']" class="me-2" />
            <font-awesome-icon v-else :icon="['far', 'bookmark']" class="me-2" />Bookmark
          </v-btn>
          
          <v-btn color="primary" variant="tonal" @click="share">
            <font-awesome-icon :icon="['fas', 'share']" class="me-2" />Share
          </v-btn>
        </div>

        <div v-else class="d-flex gap-2">
          <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal = true">
            <font-awesome-icon :icon="['fas', 'reply']" class="me-2" />Reply
          </v-btn>
          <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal = true">
            <font-awesome-icon :icon="['fas', 'quote-left']" class="me-2" />Quote from
          </v-btn>
          <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal = true">
            <font-awesome-icon :icon="['far', 'bookmark']" class="me-2" />Bookmark
          </v-btn>
          <v-btn color="dark" variant="tonal" @click="authStore.openLoginModal = true">
            <font-awesome-icon :icon="['fas', 'share']" class="me-2" />Share
          </v-btn>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import dayjs from '../../plugins/dayjs'
import { mapState, storeToRefs } from 'pinia'
import { useAuthentication } from '@/stores//authentication'
import { useForum } from '@/stores/forum'
import { useMessages } from '@/stores/messages'

export default {
  name: 'IteratorComments',
  props: {
    comments: {
      type: Array,
      required: true
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },
  emits: {
    'reply' () {
      return true
    }
  },
  setup () {
    const messagesStore = useMessages()
    const authStore = useAuthentication()
    const threadStore = useForum()
    const { currentThread } = storeToRefs(threadStore)
    const menuItems = [
      'Edit',
      'Delete',
      'Report'
    ]
    return {
      messagesStore,
      currentThread,
      menuItems,
      authStore,
      dayjs
    }
  },
  computed: {
    ...mapState(useAuthentication, ['isAuthenticated'])
  },
  methods: {
    formatDate (d) {
      // TODO: Move to a composable
      // Formats the date to be humanly readable
      return this.dayjs(d).format('ddd, MMM YYYY')
    },
    async quoteFrom () {
      // pass
    },
    async bookmark () {
      // pass
    },
    async share () {
      // pass
    },
    async requestDelete () {
      try {
        const response = await this.$http.post(`comments/${this.currentThread.id}/delete`)
        console.log(response.data)
        this.messagesStore.addSuccessMessage('Comment deleted successfully')
      } catch (e) {
        this.messagesStore.addErrorMessage(e.response.data)
      }
    },
    async report () {
      // pass 
    },
    async handleMenuAction (action) {
      switch (action) {
        case 'Bookmark':
          await this.bookmark()
          break

        case 'Report':
          await this.report()
          break

        case 'Delete':
          await this.requestDelete()
          break
      
        default:
          break
      }
    }
  }
}
</script>

<style scoped>
.card-toolbar {
  contain: layout;
  display: block;
  flex: 1 1 auto;
  max-width: 100%;
  transition: transform .2s cubic-bezier(.4, 0, .2, 1), background-color .2s cubic-bezier(.4, 0, .2, 1), left .2s cubic-bezier(.4, 0, .2, 1), right .2s cubic-bezier(.4, 0, .2, 1), box-shadow .28s cubic-bezier(.4, 0, .2, 1), max-width .25s cubic-bezier(.4, 0, .2, 1), width .25s cubic-bezier(.4, 0, .2, 1);
  position: relative;
  /* background-color: #fff; */
  border-top-left-radius: .5rem;
  border-top-right-radius: .5rem;
  /* box-shadow: 0 10px 15px -3px rgb(0 0 0 / 7%), 0 4px 6px -2px rgb(0 0 0 / 5%); */
}

.card-toolbar .card-toolbar-content {
  padding: 4px 16px;
  height: 64px;
}

.btn-icon {
  color: rgba(0, 0, 0, .54);
  min-height: 0;
  min-width: 0;
  padding: 0;
  /* box-shadow: none; */
  height: 48px;
  width: 48px;
}
</style>
