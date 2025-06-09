<template>
  <aside>
    <VoltCard>
      <template #content>
        <h4 class="card-title mb-3">Tennis Forum</h4>

        <p class="card-text mb-3">
          A forum community dedicated to Tennis players and enthusiasts.
          Come join the discussion about players, gear, matches, scores,
          guidelines, and more!

        <div class="fw-bold mb-1">35 million posts</div>
        <div class="fw-bold mb-3">94.3k members</div>
        </p>

        <button class="btn btn-block btn-info btn-rounded" @click="authStore.openLoginModal=true">
          Join our community
        </button>
      </template>
    </VoltCard>

    <VoltCard class="mt-2">
      <template #content>
        <h4 class="card-title mb-3">Top contributors this month</h4>
      </template>
    </VoltCard>
  </aside>
</template>

<script>
// import BaseAccordionVue from '../../layouts/BaseAccordion.vue'

import { useAuthentication } from '@/stores//authentication'


export default {
  name: 'ForumsAside',
  setup() {
    var authStore = useAuthentication()
    return {
      authStore
    }
  },
  components: {
    // BaseAccordionVue
  }
}
</script>
