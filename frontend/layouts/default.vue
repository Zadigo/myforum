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
const HeadersForum = resolveComponent('HeadersForum')
const HeadersThread = resolveComponent('HeadersThread')

const route = useRoute()

const pageHeader = computed(() => {
  if (route.name === 'forums-id') {
    return HeadersForum
  } else if (route.name === 'threads-id') {
    return HeadersThread
  } else {
    return null
  }
})

const aside = computed(() => {
  return null
})
</script>
