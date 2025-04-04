<template>
  <section id="forum">
    <BaseNavbar />

    <!-- Header -->
    <component  :is="pageHeader" v-if="pageHeader" />
    
    <div class="container">
      <div class="row my-5">
        <div class="col-sm-12 col-md-8 offset-md-1" role="main">
          <slot />
        </div>

        <aside class="col-sm-12 col-md-3">
          <component :is="aside" />
        </aside>
      </div>
    </div>

    <BaseFooter />

    <ModalsLogin />
    <ModalsSearch />
  </section>
</template>

<script setup lang="ts">
import HeadersForum from '~/components/headers/Forum.vue'
import HeadersThread from '~/components/headers/Thread.vue'

const headersForum = markRaw(HeadersForum)
const headersThread = markRaw(HeadersThread)

const route = useRoute()

const pageHeader = computed(() => {
  if (route.name.includes('threads-id__fr')) {
    return headersThread
  } else if (route.name.includes('forums-id__')) {
    return headersForum
  } else {
    return null
  }
})

const aside = computed(() => {
  return null
})
</script>
