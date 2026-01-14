<template>
  <aside>
    <volt-card id="statistics" class="bg-blue-300 shadow-sm">
      <template #content>
        <h5 class="font-bold text-primary-600 mb-3">
          About this Discussion
        </h5>
  
        <p class="mb-10">
          <span class="font-bold text-2xl">{{ statistics.total_comments || 0 }}</span> replies
        </p>
        
        <p>
          <span class="fw-bold h4">{{ statistics.total_participants || 0 }}</span> participants
        </p>

        <volt-divider />

        <p>
          Last post from <nuxt-link-locale to="/" class="underline font-semibold underline-offset-3">username</nuxt-link-locale> 
          16 years ago
        </p>
      </template>
    </volt-card>    

    <!-- Other Threads -->
    <volt-card id="other-threads" class="bg-primary-300 shadow-sm my-2">
      <template #title>
        Tennis Forum
      </template>

      <template #content>
        <p class="font-light">
          A forum community dedicated to Tennis players and enthusiasts. Come join the discussion 
          about players, gear, matches, scores, guidelines, and more!
        </p>

        <volt-divider />

        <div class="flex justify-end">
          <volt-secondary-button size="small" rounded>
            <nuxt-link to="/">
              <icon name="i-lucide:link" />
              Other threads
            </nuxt-link>
          </volt-secondary-button>
        </div>

        <volt-accordion :value="0" class="mt-5">
          <volt-accordion-panel v-for="(item, i) in items" :key="item.title" :value="i">
            <volt-accordion-header>
              {{ i }}
            </volt-accordion-header>

            <volt-accordion-content>
              {{ i }}
            </volt-accordion-content>
          </volt-accordion-panel>
        </volt-accordion>
      </template>
    </volt-card>

    <volt-card id="other-forums" class="bg-primary-100 shadow-sm">
      <template #content>
        <volt-accordion :value="0">
          <volt-accordion-panel v-for="(item, i) in items" :key="item.title" :value="i">
            <volt-accordion-header>
              {{ item.title }}
            </volt-accordion-header>

            <volt-accordion-content>
              {{ item.title }}
            </volt-accordion-content>
          </volt-accordion-panel>
        </volt-accordion>
      </template>
    </volt-card>
  </aside>
</template>

<script setup lang="ts">
const items = [{'title': 'First forum', 'content': 'Some content'}, {'title': 'Second forum', 'content': 'Some content'}]

const { statistics } = await useForumStatisticsComposable()
</script>>
