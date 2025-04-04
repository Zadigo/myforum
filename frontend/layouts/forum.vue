<template>
  <section id="forum">
    <!-- Navbar -->
    <BaseNavbar />

    <!-- Header -->
    <HeadersForum />
    
    <div class="container">
      <div class="row my-5">
        <div class="col-sm-12 col-md-8 offset-md-1" role="main">
          <slot />
        </div>

        <aside class="col-sm-12 col-md-3">
          <ForumsAside />
        </aside>
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
