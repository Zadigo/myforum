<template>
  <section id="forums">
    <div class="row mb-5">
        <ForumsCard title="Site rules / FAQ" text="See here for detailed specifics of Tennis Forum site rules, policy, FAQ" />

        <!-- Forums -->
        <div class="my-3">
          <Suspense>
            <AsyncForumsIterationBlock />

            <template #fallback>
              <VoltSkeleton height="4rem" />
            </template>
          </Suspense>
        </div>

        <!-- Latest Comments -->
        <div class="mt-30">
          <Suspense>
            <AsyncForumLatestCommentsBlock />

            <template #fallback>
              <VoltSkeleton height="4rem" />
            </template>
          </Suspense>
        </div>
      </div>
  </section>
</template>

<script setup lang="ts">
useHead({
  title: 'Forums'
})

const AsyncForumsIterationBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/IterationBlock.vue'),
  timeout: 10000
})

const AsyncForumLatestCommentsBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/LatestBlock.vue'),
  timeout: 10000
})
</script>
