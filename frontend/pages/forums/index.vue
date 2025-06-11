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
      <ClientOnly>
        <div class="mt-30">
          <Suspense>
            <AsyncForumLatestCommentsBlock />

            <template #fallback>
              <div class="flex justify-between">
                <VoltSkeleton height="2rem" />
                <VoltSkeleton height="2rem" />
              </div>
              
              <div class="space-y-3">
                <VoltSkeleton v-for="i in 4" :key="i" height="4rem" />
              </div>
            </template>
          </Suspense>
        </div>
      </ClientOnly>
    </div>
  </section>
</template>

<script setup lang="ts">
useHead({
  title: 'Forums'
})

const AsyncForumsIterationBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/IterationBlock.vue')
})

const AsyncForumLatestCommentsBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/LatestBlock.vue')
})
</script>
