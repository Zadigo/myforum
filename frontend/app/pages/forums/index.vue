<template>
  <section id="forums">
    <div class="row mb-5">
      <forums-card title="Site rules / FAQ" text="See here for detailed specifics of Tennis Forum site rules, policy, FAQ" />

      <!-- Forums -->
      <div class="my-3">
        <suspense>
          <AsyncForumsIterationBlock />

          <template #fallback>
            <volt-skeleton height="4rem" />
          </template>
        </suspense>
      </div>

      <!-- Latest Comments -->
      <client-only>
        <div class="mt-30">
          <suspense>
            <template #efault>
              <async-forum-latest-comments-block />
            </template>

            <template #fallback>
              <div>
                <div class="flex justify-between">
                  <volt-skeleton class="h-8" />
                  <volt-skeleton class="h-8" />
                </div>
                
                <div class="space-y-3">
                  <volt-skeleton v-for="i in 4" :key="i" class="h-16" />
                </div>
              </div>
            </template>
          </suspense>
        </div>
      </client-only>
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
