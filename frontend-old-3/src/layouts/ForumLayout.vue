<template>
  <section id="forum">
    <!-- Header -->
    <router-view name="header" /> 

    <div class="container">
      <div class="row my-5">
        <!-- Main -->
        <div class="col-sm-12 col-md-8 offset-md-1" role="main">
          <router-view v-slot="{ Component }">
            <transition :key="$route.name">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>

        <!-- Aside -->
        <aside class="col-sm-12 col-md-3">
          <router-view name="aside" />  
        </aside>

        <a ref="totop" href class="btn btn-primary btn-lg btn-floating" role="button" @click.prevent="scrollToTop">
          <span class="mdi mdi-arrow-up" />
        </a>
      </div>
    </div>
  </section>
</template>

<script>
import { scrollToTop, useUtilities } from '@/composables/utils'

export default {
  name: 'ForumLayout',
  setup() {
    const { getVerticalScrollPercentage } = useUtilities()
    return {
      getVerticalScrollPercentage,
      scrollToTop
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
