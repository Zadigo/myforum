<template>
  <section id="forums">
    <div class="row mb-5">
        <div class="col-12">
          <ForumsCard title="Site rules / FAQ" text="See here for detailed specifics of Tennis Forum site rules, policy, FAQ" />
        </div>

        <!-- Forums -->
        <div class="col-12 my-3">
          <Suspense>
            <AsyncForumsDetailCard />

            <template #fallback>
              Loading...
            </template>
          </Suspense>
        </div>

        <!-- Latest Comments -->
        <div class="col-12">
          <Suspense>
            <AsyncForumLatest />

            <template #fallback>
              Loading...
            </template>
          </Suspense>
        </div>
      </div>
  </section>
</template>

<script setup lang="ts">
const AsyncForumsDetailCard = defineAsyncComponent({
  loader: async () => import('~/components/forums/DetailCard.vue')
})

const AsyncForumLatest = defineAsyncComponent({
  loader: async () => import('~/components/forums/Latest.vue')
})
</script>
