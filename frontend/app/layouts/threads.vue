<template>
  <section id="forum" class="my-30">
    <!-- Navbar -->
    <base-navbar />

    <!-- Header -->
    <headers-thread />

    <div class="grid grid-cols-12 px-10 max-w-7xl mx-auto my-20" role="main">
      <div class="col-span-8">
        <slot />
      </div>

      <div class="col-span-4">
        <threads-aside />
      </div>
    </div>

    <!-- Footer -->
    <base-footer />

    <client-only>
      <!-- Modals -->
      <modals-login />
      <modals-search />
      <modals-comments-create />
    </client-only>
  </section>
</template>

<script setup lang="ts">
import type { CustomRouteMeta } from '~/types'

const routeMeta = useRoute().meta as CustomRouteMeta
</script>
