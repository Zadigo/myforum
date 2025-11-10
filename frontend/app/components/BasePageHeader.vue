<template>
  <header ref="pageHeaderEl" class="mb-5 max-w-7xl px-10 rounded-md mx-auto">
    <div class="p-20">
      <slot name="breadcrumbs" />

      <h1 class="font-title font-bold text-5xl mt-2 mb-5">
        <slot name="title" />
      </h1>

      <div class="mt-5">
        <slot name="actions" />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
const pageHeaderEl = useTemplateRef<HTMLElement>('pageHeaderEl')
</script>
