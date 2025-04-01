<template>
  <base-forum-layout-vue>
    <template #header></template>

    <template #aside>
      <forums-aside-vue />
    </template>

    <section id="forums">
      <!-- Site rules -->
      <div class="row mb-5">
        <div class="col-12">
          <router-link :to="{ name: 'site_rules_view' }" aria-label="Site rules / FAQ" class="text-dark">
            <article class="card shadow-sm" role="article">
              <div class="card-body">
                <h3 class="card-title">Site rules / FAQ</h3>
                
                <p class="card-text">
                  See here for detailed specifics of Tennis Forum site rules, policy, FAQ
                </p>
              </div>
            </article>
          </router-link>
        </div>
      </div>

      <div v-if="!store.hasForums" class="row mb-5">
        <div class="col-12">
          <div class="card text-center shadow-sm">
            <div class="card-body">
              <h2 class="fw-bold">There are no forums on this this website</h2>
            </div>
          </div>
        </div>
      </div>

      <!-- Forums -->
      <article v-for="category in Object.keys(store.forumsByGroup)" :key="category" :aria-label="category" class="row mb-5">
        <div class="col-12">
          <h3>{{ category }}</h3>
        </div>

        <div class="col-12">
          <base-template-card v-for="(forum, i) in store.forumsByGroup[category]" :key="forum.id" :class="{ 'mt-1': i > 0 }" :aria-label="forum.title" class="shadow-sm" role="article">
            <router-link :to="{ name: 'forum_view', params: { id: forum.id } }" class="text-dark">
              <div class="card-body">
                <h3 class="card-title">
                  {{ forum.title }}
                </h3>

                <p class="card-text fw-light">{{ forum.description }}</p>

                <div class="card-info">
                  <span class="badge bg-info p-2">{{ forum.number_of_threads }} <font-awesome-icon :icon="['fas', 'users']" /></span>
                  <span class="badge bg-info p-2 ms-2">200000 <font-awesome-icon :icon="['fas', 'eye']" /></span>
                  <span class="badge bg-info p-2 ms-2">{{ formatDate(forum.created_on) }}</span>
                </div>
              </div>
            </router-link>
          </base-template-card>
        </div>
      </article>

      <!-- Latest posts -->
      <latest-posts :posts="[]" class="d-none" />
    </section>
  </base-forum-layout-vue>
</template>

<script>
import { useForum } from '@/stores/forum'
import { useMessages } from '@/stores/messages'
import { useFormatDates } from '../../composables/dates'

import BaseForumLayoutVue from '../../layouts/BaseForumLayout.vue'
import BaseTemplateCard from '@/layouts/BaseTemplateCard.vue'
import ForumsAsideVue from '../../components/forums/ForumsAside.vue'
import LatestPosts from '@/components/LatestPosts.vue'

export default {
  name: 'ForumsView',
  components: {
    BaseForumLayoutVue,
    BaseTemplateCard,
    ForumsAsideVue,
    LatestPosts
  },
  // TODO:
  // beforeRouteEnter (to, from, next) {
  //   next(vm => {
  //     if (!vm.$session.exists('forums')) {
  //       vm.store.forums = vm.getForums()
  //     }
  //   })
  // },
  setup () {
    const messagesStore = useMessages()
    const store = useForum()
    const { formatDate } = useFormatDates()
    return {
      formatDate,
      messagesStore,
      store
    }
  },
  beforeMount() {
    if (this.$session.keyExists('forums') && this.$session.listCount('forums') > 0) {
      this.store.forums = this.sessionStorage.forums
    } else {
      this.getForums()
    }
  },
  methods: {
    async getForums() {
      // Gets the list of available forums
      // from the database
      try {
        const response = await this.$http.get('/forums/')
        
        this.store.forums = response.data
        this.$session.create('forums', this.store.forums) 
      } catch(error) {
        console.error(error)
        this.messagesStore.addErrorMessage('Could not get forums')
      }
    }
  }
}
</script>
