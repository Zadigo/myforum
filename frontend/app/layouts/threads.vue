<template>
  <section id="forum" class="my-30">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <headers-thread />

    <div class="grid grid-cols-12 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <div class="col-span-4">
        <threads-aside />
      </div>
    </div>

    <!-- Footer -->
    <base-footer />

    <client-only>
      <!-- Modals -->
      <modals-login />
      <modals-search />
      <modals-comments-create />
    </client-only>
  </section>
</template>

<script setup lang="ts">
</script>
