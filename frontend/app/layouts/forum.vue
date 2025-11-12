<template>
  <section id="forum">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <headers-forum />
    
    <div class="grid grid-cols-12 px-10 max-w-7xl mx-auto gap-4 my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <div class="col-span-4">
        <forums-aside />
      </div>
    </div>

    <!-- Footer -->
    <base-footer />
    
    <!-- Modals -->
    <ClientOnly>
      <ModalsLogin />
      <ModalsSearch />
    </ClientOnly>
  </section>
</template>

<script setup lang="ts">
import type { CustomRouteMeta } from '~/types'

const routeMeta = useRoute().meta as CustomRouteMeta
</script>
