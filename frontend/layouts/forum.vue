<template>
  <section id="forum">
    <!-- Navbar -->
    <BaseNavbar />

    <!-- Header -->
    <HeadersForum />
    
    <div class="grid grid-cols-2" role="main">
      <slot />

      <ForumsAside />
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
