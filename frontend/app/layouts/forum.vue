<template>
  <section id="forum" class="my-30">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <headers-forum />

    <div class="grid grid-cols-12 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <div class="col-span-4">
        <suspense>
          <async-forums-aside />
        </suspense>
      </div>
    </div>

    <!-- Footer -->
    <lazy-base-footer hydrate-on-visible />

    <!-- Modals -->
    <client-only>
      <lazy-modals-login hydrate-on-idle />
    </client-only>

    <client-only>
      <lazy-modals-search hydrate-on-idle />
    </client-only>
  </section>
</template>

<script setup lang="ts">
const AsyncForumsAside = defineAsyncComponent(() => import('~/components/forums/Aside.vue'))
</script>
