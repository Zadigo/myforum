<template>
  <section id="forum">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <HeadersForum />
    
    <div class="grid grid-cols-12 px-10 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <div class="col-span-4">
        <ForumsAside />
      </div>
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
