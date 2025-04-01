<template>
  <section id="forum" :class="{ 'bg-dark text-light': darkMode }">
    <!-- Header -->
    <slot name="header" />

    <div class="container">
      <div class="row my-5">
        <!-- Main -->
        <div class="col-sm-12 col-md-8 offset-md-1" role="main">
          <slot />
        </div>

        <!-- Aside -->
        <aside class="col-sm-12 col-md-3">
          <slot name="aside" />
        </aside>

        <a ref="totop" href class="btn btn-primary btn-lg btn-floating" role="button" @click.prevent="scrollToTop">
          <span class="mdi mdi-arrow-up" />
        </a>
      </div>
    </div>
  </section>
</template>

<script>
import { inject } from 'vue'
import { scrollToTop, getVerticalScrollPercentage } from '../utils'

export default {
  name: 'ForumLayout',
  setup() {
    var { darkMode } = inject('dark_mode')
    return {
      scrollToTop,
      darkMode
    }
  }, 
  mounted() {
    document.querySelector('html').addEventListener('scroll', this.showBackToTop, { passive: false })
  },
  beforeUnmount() {
    document.querySelector('html').removeEventListener('scroll', this.showBackToTop, { passive: false })
  },
  methods: {
    showBackToTop() {
      var el = document.querySelector('body')
      var percentage = getVerticalScrollPercentage(el)

      if (percentage < 20) {
        this.$refs.totop.style.display = 'none'
      } else {
        this.$refs.totop.style.display = 'block'
      }
    }
  }
}
</script>

<style scoped>
.btn-floating {
  position: fixed;
  right: 5%;
  bottom: 5%;
  /* background-color: #ac2bac; */
}
</style>
