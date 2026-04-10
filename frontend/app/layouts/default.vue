<template>
  <section id="forum" class="my-30">
    <!-- Navbar -->
    <base-navbar />

    <div class="grid grid-cols-12 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <lazy-forums-aside class="col-span-4" hydrate-on-idle />
    </div>

    <!-- Footer -->
    <lazy-base-footer hydrate-on-visible />
    
    <!-- Modals -->
    <client-only>
      <template #default>
        <lazy-modals-login hydrate-on-idle />
      </template>
    </client-only>

    <client-only>
      <template #default>
        <lazy-modals-search hydrate-on-idle />
      </template>
    </client-only>
  </section>
</template>

<script setup lang="ts">
</script>
