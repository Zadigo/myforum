<template>
  <aside>
    <volt-card class="bg-blue-300 shadow-sm">
      <template #content>
        <h5 class="font-bold text-primary-600 mb-3">
          About this Discussion
        </h5>
  
        <p class="mb-10">
          <span class="font-bold text-2xl">6,677</span> replies
        </p>
        
        <p>
          <span class="fw-bold h4">{{ currentThread?.participants.length || 0 }}</span> participants
        </p>

        <VoltDivider />

        <p>
          Last post from <NuxtLinkLocale to="/" class="text-decoration">{{ currentThread?.latest_comment.user__username }}</NuxtLinkLocale> 
          formatDuration(currentThread.latest_comment.created_on)
        </p>
      </template>
    </volt-card>    

    <volt-card class="bg-primary-300 shadow-sm my-2">
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
          <VoltSecondaryButton size="small" rounded>
            <nuxt-link to="/">
              <icon name="i-lucide:link" />
              Other threads
            </nuxt-link>
          </VoltSecondaryButton>
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

    <volt-card class="bg-primary-100 shadow-sm">
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

const forumStore = useForums()
const { currentThread } = storeToRefs(forumStore)
</script>>
