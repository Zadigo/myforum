<template>
  <section id="forum" class="relative my-30">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <headers-thread />

    <div class="grid grid-cols-12 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <div class="col-span-4">
        <lazy-threads-aside hydrate-on-idle />
      </div>
    </div>

    <!-- Footer -->
    <lazy-base-footer hydrate-on-visible />

    <client-only>
      <lazy-modals-login hydrate-on-idle />
    </client-only>

    <client-only>
      <lazy-modals-search hydrate-on-idle />
    </client-only>

    <client-only>
      <lazy-modals-comments-create hydrate-on-idle />
    </client-only>
  </section>
</template>

<script setup lang="ts">
</script>
