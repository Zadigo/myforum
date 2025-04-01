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
            <article class="card" role="article">
              <div class="card red lighten-1">
                <div class="card-body">
                  <h3 class="card-title">Site rules / FAQ</h3>
                  
                  <p class="card-text">
                    See here for detailed specifics of Tennis Forum site rules, policy, FAQ
                  </p>
                </div>
              </div>
            </article>
          </router-link>
        </div>
      </div>

      <div v-if="!store.hasForums" class="row mb-5">
        <div class="col-12">
          <div class="card text-center">
            <div class="card-body">
              <h2>There are no forums on this this website</h2>
            </div>
          </div>
        </div>
      </div>

      <!-- Forums -->
      <div v-for="category in Object.keys(store.forumsByGroup)" :key="category" :aria-labelledby="category"
        class="row mb-5">
        <div class="col-12">
          <h3>{{ category }}</h3>
        </div>

        <div class="col-12">
          <article v-for="(forum, i) in store.forumsByGroup[category]" :key="forum.id" :class="{ 'mt-1': i > 0 }"
            :aria-label="forum.title" class="card" role="article">
            <router-link :to="{ name: 'forum_view', params: { id: forum.id } }" class="text-dark">
              <div class="card-body">
                <h3 class="card-title">
                  {{ forum.title}}
                </h3>

                <p class="card-text">{{ forum.description }}</p>

                <div class="card-info">
                  <span class="badge bg-info p-2">100 <span class="mdi mdi-comment ms-2" /></span>
                  <span class="badge bg-info p-2 ms-2">200000 <span class="mdi mdi-eye ms-2" /></span>
                  <span class="badge bg-info p-2 ms-2">{{ forum.created_on }}</span>
                </div>
              </div>
            </router-link>
          </article>
        </div>
      </div>

      <!-- Latest posts -->
      <div class="col-12 d-flex justify-content-between">
        <h3>Latest posts</h3>

        <router-link :to="{ name: 'whats_new_view'}" class="lh-lg">
          All new posts
        </router-link>
      </div>

      <div class="col-12">
        <div v-for="i in 5" :key="i" class="card mb-2">
          <div class="card-body">
            {{ i }}
          </div>
        </div>
      </div>
    </section>
  </base-forum-layout-vue>
</template>

<script>
import { useForum } from '@/stores//forum'
import BaseForumLayoutVue from '../../layouts/BaseForumLayout.vue'
import ForumsAsideVue from '../../components/forums/ForumsAside.vue'

export default {
  name: 'ForumsView',
  setup() {
    var store = useForum()
    return {
      store
    }
  },
  components: {
    BaseForumLayoutVue,
    ForumsAsideVue
  },
  beforeMount() {
    var forums = this.$session.retrieve('/forums')
    if (forums) {
      this.store.forums = forums
    } else {
      this.getForums()
    }
  },
  methods: {
    async getForums() {
      try {
        var response = await this.$http.get('/forums/')
        
        this.store.forums = response.data
        this.$session.create('forums', this.store.forums)
      } catch(error) {
        console.error(error)
      }
    }
  }
}
</script>
