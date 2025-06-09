<template>
  <section id="forum">
    <!-- Navbar -->
    <BaseNavbar />

    <!-- Header -->
    <HeadersThread />

    <div class="grid grid-cols-2 px-10 max-w-7xl mx-auto" role="main">
      <slot />
      <ThreadsAside />
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
