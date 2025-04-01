<template>
  <!-- Latest posts -->
  <section id="latest-posts">
    <div class="col-12 d-flex justify-content-between">
      <h3>Latest posts</h3>
  
      <NuxtLink to="/whats-new" class="lh-lg">
        All new posts
      </NuxtLink>
    </div>
  
    <div class="col-12">
      <article v-for="(post, i) in posts" :key="i" class="card shadow-sm mb-2">
        <div class="card-body">
          {{ post.title }}
        </div>
      </article>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'LatestPosts',
  props: {
    posts: {
      type: Array,
      default: () => []
    }
  },
  async setup () {
    const latestPosts = ref([])

    async function getLatestPosts () {
      latestPosts.value = []
    }
    await getLatestPosts()
    
    return {
      latestPosts
    }
  }
}
</script>
