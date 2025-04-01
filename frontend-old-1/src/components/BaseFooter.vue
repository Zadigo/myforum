<template>
  <footer class="text-center text-white" style="background-color: #0a4275;">
    <div class="container pt-4">
      <section class="mb-4">
        <a class="btn btn-link btn-floating btn-lg text-dark m-1" href="#!" role="button">
          <i class="fab fa-facebook-f"></i>
        </a>
      </section>
    </div>

    <!-- Copyright -->
    <div class="text-center text-light p-3" style="background-color: rgba(0, 0, 0, 0.2);">
      © 2020 Copyright:
      <router-link :to="{ name: 'forums_view' }" class="text-light">
        My forum
      </router-link>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'BaseFooter'
}
</script>
