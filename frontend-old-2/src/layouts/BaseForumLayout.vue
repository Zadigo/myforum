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
import { scrollToTop, useUtilities } from '@/composables/utils'

export default {
  name: 'BaseForumLayout',
  setup () {
    const { darkMode } = inject('darkMode', false)
    const { getVerticalScrollPercentage } = useUtilities()
    return {
      scrollToTop,
      darkMode,
      getVerticalScrollPercentage
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
      const el = document.querySelector('body')
      const percentage = this.getVerticalScrollPercentage(el)

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
