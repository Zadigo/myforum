<template>
  <header ref="page-header" class="page-header mb-5 bg-light border-bottom">
    <div class="container">
      <!-- <div class="row p-4 pb-0 pe-lg-0 pt-lg-5 align-items-center border"> -->
      <div class="row p-4 align-items-center">
        <!-- p-lg-5 pt-lg-3 -->
        <div class="col-11 p-3 offset-1">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item">
                <router-link :to="{ name: 'forums_view' }">
                  Forums
                </router-link>
              </li>
              <!-- <li class="breadcrumb-item"><a href="#">Library</a></li>
              <li class="breadcrumb-item active" aria-current="page">Data</li> -->
              <slot name="breadcrumbs" />
            </ol>
          </nav>
  
          <h1 class="display-6 fw-normal lh-1 my-4">
            <slot name="title" />
          </h1>
          <!-- <p class="lead">Quickly design and customize responsive mobile-first sites with Bootstrap, the world’s most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.</p>
          <div class="d-grid gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3">
            <button type="button" class="btn btn-primary btn-lg px-4 me-md-2 fw-bold">Primary</button>
            <button type="button" class="btn btn-outline-secondary btn-lg px-4">Default</button>
          </div> -->
          <div class="mt-4">
            <slot name="actions" />
          </div>
        </div>
  
        <!-- <div class="col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg">
          <img class="rounded-lg-3" src="bootstrap-docs.png" alt="" width="720">
        </div> -->
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'BasePageHeader',
  computed: {
    breadcrumbs() {
      var items = [
        {
          text: 'Home',
          to: 'home'
        },
        {
          text: 'Forums',
          to: 'forums'
        }
      ]
      return items
    }
  }
}
</script>

<style scoped>
/* .page-header {
  padding: 1rem;
  min-height: 100px;
  box-shadow: 0px 3px 1px -2px rgba(0, 0, 0, 0.2), 0px 2px 2px 0px rgba(0, 0, 0, 0.14), 0px 1px 5px 0px rgba(0, 0, 0, 0.12);
} */
</style>
