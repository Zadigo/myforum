<template>
  <!-- Latest posts -->
  <section id="latest-posts">
    <div class="col-12 d-flex justify-content-between">
      <h3>Latest posts</h3>
  
      <router-link :to="{ name: 'whats_new_view' }" class="lh-lg">
        All new posts
      </router-link>
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
export default {
  name: 'LatestPosts',
  props: {
    posts: {
      type: Array,
      default: () => []
    }
  }  
}
</script>
