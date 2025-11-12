<template>
  <section id="forum">
    <!-- Navbar -->
    <base-navbar />

    <div class="grid grid-cols-12 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <forums-aside class="col-span-4" />
    </div>

    <!-- Footer -->
    <base-footer />
    
    <!-- Modals -->
    <client-only>
      <template #default>
        <modals-login />
        <modals-search />
      </template>
    </client-only>
  </section>
</template>

<script setup lang="ts">
</script>
