<template>
  <div class="col-12">
    <article v-for="(thread, i) in threads" :key="thread.id" :class="{ 'mt-1': i > 0 }" role="article" @click="store.setCurrentThread(thread)">
      <router-link :to="{ name: 'thread_comments_view', params: { id: thread.id } }" :aria-label="thread.title" class="text-dark">
        <div class="card shadow-sm">
          <div class="card-body">
            <div class="d-flex justify-content-start align-items-center gap-2 mb-4">
              <img src="http://via.placeholder.com/200x200" class="rounded-circle" width="50" height="50">
              <h3 class="card-title m-0 h4">{{ thread.title }}</h3>
              <font-awesome-icon v-if="thread.owned_by_user" :icon="['fas', 'bolt-lightning']" class="text-warning" />
            </div>

            <div v-if="thread.description" class="card-text fw-light my-2">
              {{ thread.description }}
            </div>

            <div class="card-info">
              <span class="badge bg-light text-dark p-2"><span class="mdi mdi-comment ms-2" /> {{ thread.number_of_comments }}</span>
              <span class="badge bg-light text-dark p-2 ms-2"><span class="mdi mdi-calendar ms-2" /> {{ formatDate(thread.created_on) }}</span>
              <span class="badge bg-light text-dark p-2 ms-2">{{ formatDuration(thread.latest_comment.created_on) }}</span>
            </div>
          </div>
        </div>
      </router-link>
    </article>
  </div>
</template>

<script>
import { storeToRefs } from 'pinia'
import { useForum } from '@/stores/forum'
import { useMessages } from '@/stores/messages'
import { useFormatDates } from '@/composables/dates'

export default {
  name: 'ThreadsList',
  async setup () {
    const store = useForum()
    const messagesStore = useMessages()
    const { threads, currentForum } = storeToRefs(store)
    const { formatDate, formatDuration } = useFormatDates()

    async function getThreads (id, sort = 0) {
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
        messagesStore.addErrorMessage(e.response)
      }
    }
    await getThreads()

    return {
      threads,
      currentForum,
      formatDate,
      formatDuration
    }
  }
}
</script>
