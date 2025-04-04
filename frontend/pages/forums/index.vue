<template>
  <section id="forums">
    <div class="row mb-5">
        <div class="col-12">
          <ForumsCard title="Site rules / FAQ" text="See here for detailed specifics of Tennis Forum site rules, policy, FAQ" />
        </div>

        <!-- Forums -->
        <div class="col-12 my-3">
          <Suspense>
            <template #default>
              <AsyncIterationBlock />
            </template>

            <template #fallback>
              Loading...
            </template>
          </Suspense>
        </div>

        <!-- Latest Comments -->
        <div class="col-12">
          <Suspense>
            <template #default>
              <AsyncForumLatestBlock />
            </template>

            <template #fallback>
              Loading...
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

const AsyncIterationBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/IterationBlock.vue'),
  timeout: 10000
})

const AsyncForumLatestBlock = defineAsyncComponent({
  loader: async () => import('~/components/forums/LatestBlock.vue'),
  timeout: 10000
})
</script>
