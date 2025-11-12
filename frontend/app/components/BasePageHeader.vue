<template>
  <header ref="pageHeaderEl" class="mb-5 max-w-7xl px-10 rounded-md mx-auto">
    <div class="p-20">
      <client-only>
        <template #default>
          <slot name="breadcrumbs" />
        </template>

        <template #fallback>
          <volt-skeleton height="1.5rem" width="20rem" />
        </template>
      </client-only>

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
