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

      <div class="p-5 bg-secondary">
        google
      </div>

      <!-- Latest Comments -->
      <ClientOnly>
        <div class="mt-30">
          <Suspense>
            <AsyncForumLatestCommentsBlock />

            <template #fallback>
              <div class="flex justify-between">
                <VoltSkeleton class="h-[2rem]" />
                <VoltSkeleton class="h-[2rem]" />
              </div>
              
              <div class="space-y-3">
                <VoltSkeleton v-for="i in 4" :key="i" class="h-[4rem]" />
              </div>
            </template>
          </Suspense>
        </div>
      </ClientOnly>
    </div>
  </section>
</template>

<script setup lang="ts">
const AsyncForumsIterationBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/IterationBlock.vue')
})

const AsyncForumLatestCommentsBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/LatestBlock.vue')
})

/**
 * SEO
 */

useHead({
  title: 'Forums',
  meta: [
    {
      name: 'description',
      content: 'Join the Tennis Forum community to discuss tennis news, matches, players, and more with fellow tennis enthusiasts.'
    }
  ]
})
</script>
