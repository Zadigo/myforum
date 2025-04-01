<template>
  <section id="whats-new">
    <base-forum-layout-vue>
      <template #aside>
        <thread-aside-vue />
      </template>

      <article v-for="(thread, i) in threads" :key="thread.id" :class="{ 'mt-1': i > 0 }" role="article" @click="setInformation(thread)">
        <router-link :to="{ name: 'thread_comments_view', params: { id: thread.id } }" class="text-dark">
          <div :aria-label="thread.title" class="card">
            <div class="card-body">
              <div class="row">
                <div class="col-2">
                  <img src="https://via.placeholder.com/300x300" class="img-fluid" alt="">
                </div>

                <div class="col-10">
                  <h3 class="card-title fs-5 mb-2">
                    {{ thread.title }}
                  </h3>            

                  <div class="card-info">
                    <span class="badge bg-light text-dark p-2"><span class="mdi mdi-comment ms-2" /> {{ thread.number_of_comments }}</span>
                    <!-- <span class="badge bg-light text-dark p-2 ms-2"><span class="mdi mdi-calendar ms-2" /> {{ formatDate(thread.created_on) }}</span> -->
                    <!-- <span class="badge bg-light text-dark p-2 ms-2">{{ formatDuration(thread.latest_comment.created_on) }}</span> -->
                  </div>
                </div>
              </div>
    
            </div>
          </div>
        </router-link>
      </article>

      </base-forum-layout-vue>
  </section>
</template>

<script>
import BaseForumLayoutVue from '../../layouts/BaseForumLayout.vue'
import IteratorCommentsVue from '../../components/threads/IteratorComments.vue'
import ThreadAsideVue from '../../components/threads/ThreadAside.vue'
import { useForum } from '@/stores//forum'

export default {
  name: 'WhatsNewView',
  setup() {
    var store = useForum()
    return {
      store
    }
  },
  data: () => ({
    threads: []
  }),
  components: {
    BaseForumLayoutVue,
    IteratorCommentsVue,
    ThreadAsideVue
  },
  mounted() {
    this.getComments()
  },
  methods: {
    async getComments() {
      try {
        var response = await this.$http.get('/comments/whats-new')
        this.threads = response.data
      } catch(error) {
        console.error(error)
      }
    },
    setInformation(thread) {
      this.store.loadFromCache()
      this.store.setCurrentThread(thread)
      this.store.setCurrentForum(thread.forum)
    }
  }
}
</script>
