<template>
  <footer class="text-center text-white" style="background-color: #0a4275;">
    <div class="container pt-4">
      <section class="mb-4">
        <a class="btn btn-link btn-floating btn-lg text-dark m-1" href="#" role="button">
          <font-awesome :icon="['fab', 'facebook-f']" />
        </a>
      </section>
    </div>

    <!-- Copyright -->
    <div class="text-center text-light p-3" style="background-color: rgba(0, 0, 0, 0.2);">
      © {{ $dayjs().year() }} Copyright:
      <NuxtLink to="/" class="text-light">
        My forum
      </NuxtLink>
    </div>
  </footer>
</template>

<script setup lang="ts">
const { $dayjs } = useNuxtApp()
</script>
