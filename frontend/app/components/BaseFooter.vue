<template>
  <footer class="text-center bg-primary-600 dark:bg-primary-900 dark:text-primary-300">
    <div class="flex justify-center pt-4">
      <section class="mb-4 flex justify-center space-x-4">
        <volt-link>
          <icon name="i-fa7-brands:facebook" />
        </volt-link>

        <volt-link>
          <icon name="i-fa7-brands:instagram" />
        </volt-link>
        
        <volt-link>
          <icon name="i-fa7-brands:twitter" />
        </volt-link>
      </section>
    </div>

    <!-- Copyright -->
    <div class="text-center text-light p-3 bg-primary-700 dark:bg-primary-800">
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
