<template>
  <section id="forum">
    <!-- Navbar -->
    <BaseNavbar />

    <!-- Header -->
    <HeadersThread />

    <div class="grid grid-cols-12 px-10 max-w-7xl mx-auto" role="main">
      <div class="col-span-8">
        <slot />
      </div>
      
      <div class="col-span-4">
        <ThreadsAside />
      </div>
    </div>

    <!-- Footer -->
    <BaseFooter />
    
    <ClientOnly>
      <!-- Modals -->
      <ModalsLogin />
      <ModalsSearch />
    </ClientOnly>
  </section>
</template>

<script setup lang="ts">
</script>
