<template>
  <header ref="pageHeaderEl" class="page-header mb-5 bg-light border-bottom">
    <div class="container">
      <div class="row p-4 align-items-center">
        <div class="col-11 p-3 offset-1">
          <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
              <li class="breadcrumb-item">
                <NuxtLink to="/">
                  Forums
                </NuxtLink>
              </li>
              <slot name="breadcrumbs" />
            </ol>
          </nav>
  
          <h1 class="display-6 fw-normal lh-1 my-4">
            <slot name="title" />
          </h1>

          <div class="mt-4">
            <slot name="actions" />
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
</script>
