<template>
  <div id="forums">
    <article v-for="category in forumCategories" :key="category" class="mb-5">
      <div class="mb-2">
        <h3 class="font-bold text-2xl">
          {{ category }}
        </h3>
      </div>
      
      <template v-if="forumsByCategory && forumsByCategory[category]">
        <article v-for="(forum, i) in forumsByCategory[category]" :key="forum.id">
          <volt-card :class="{ 'mt-1': i > 0 }"  class="shadow-sm" role="article">
            <template #content>
              <nuxt-link-locale :to="`/forums/${forum.id}`">
                <h4 class="font-bold">
                  {{ forum.title }}
                </h4>
    
                <p class="font-light my-2">
                  {{ forum.description }}
                </p>
    
                <div id="infos" class="space-x-3 mt-5">
                  <volt-tag>
                    {{ forum.numberOfThreads }} <icon name="i-lucide:users" />
                  </volt-tag>
    
                  <volt-tag>
                    200000 <icon name="i-lucide:eye" />
                  </volt-tag>
    
                  <volt-tag>
                    {{ $dayjs(forum.createdOn).fromNow() }}
                  </volt-tag>
                </div>
              </nuxt-link-locale>
            </template>
          </volt-card>
        </article>
      </template>
    </article>

    <dev-only>
      <dev-container>
        <pre vocab="json" class="overflow-scroll h-70 w-full p-2 rounded-lg inset-shadow-2xs bg-slate-50/60 backdrop-blur-3xl">
          {{ forumsByCategory }}
        </pre>

        <pre class="overflow-scroll h-70 w-full p-2 rounded-lg inset-shadow-2xs bg-slate-50/60 backdrop-blur-3xl">
          {{ forumCategories }}
        </pre>
      </dev-container>
    </dev-only>
  </div>
</template>

<script setup lang="ts">
const { forumCategories, forumsByCategory } = await useForumsComposable()
</script>
