<template>
  <section id="forum">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <headers-thread />

    <div class="grid grid-cols-12 px-10 max-w-7xl mx-auto" role="main">
      <div class="col-span-8">
        <slot />
      </div>
      
      <div class="col-span-4">
        <threads-aside />
      </div>
    </div>

    <!-- Footer -->
    <base-footer />
    
    <ClientOnly>
      <!-- Modals -->
      <ModalsLogin />
      <ModalsSearch />
    </ClientOnly>
  </section>
</template>

<script setup lang="ts">
</script>
