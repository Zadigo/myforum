<template>
  <section id="forum">
    <!-- Navbar -->
    <BaseNavbar />

    <div class="grid grid-cols-12 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <ForumsAside class="col-span-4" />
    </div>

    <!-- Footer -->
    <BaseFooter />
    
    <!-- Modals -->
    <client-only>
      <ModalsLogin />
      <ModalsSearch />
    </client-only>
  </section>
</template>

<script setup lang="ts">
</script>
