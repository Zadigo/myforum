<template>
  <section id="forum">
    <!-- Navbar -->
    <BaseNavbar />

    <div class="grid grid-cols-12 px-10 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <ForumsAside class="col-span-4" />
    </div>

    <!-- Footer -->
    <BaseFooter />
    
    <!-- Modals -->
    <ClientOnly>
      <ModalsLogin />
      <ModalsSearch />
    </ClientOnly>
  </section>
</template>

<script setup lang="ts">
</script>
