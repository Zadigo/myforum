<template>
  <footer class="text-center bg-primary-600 dark:bg-primary-800 dark:text-primary-300">
    <div class="container pt-4">
      <section class="mb-4">
        <a class="btn btn-link btn-floating btn-lg text-dark m-1" href="#" role="button">
          <icon name="i-fa6:facebook-f" />
        </a>
      </section>
    </div>

    <!-- Copyright -->
    <div class="text-center text-light p-3">
      © {{ currentYear }} Copyright:
      <NuxtLink to="/" class="text-light">
        My forum
      </NuxtLink>
    </div>
  </footer>
</template>

<script setup lang="ts">
const { $dayjs } = useNuxtApp()
const currentYear = ref<number>($dayjs().year())
</script>
