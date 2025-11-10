<template>
  <aside>
    <VoltCard class="bg-blue-300 shadow-sm">
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
    </VoltCard>    

    <VoltCard class="bg-primary-300 shadow-sm my-2">
      <template #title>
        Tennis Forum
      </template>

      <template #content>
        <p class="font-light">
          A forum community dedicated to Tennis players and enthusiasts. Come join the discussion 
          about players, gear, matches, scores, guidelines, and more!
        </p>

        <VoltDivider />

        <div class="flex justify-end">
          <VoltSecondaryButton size="small" rounded>
            <NuxtLink to="/">
              <Icon name="fa-solid:link" />
              Other threads
            </NuxtLink>
          </VoltSecondaryButton>
        </div>

        <VoltAccordion :value="0" class="mt-5">
          <VoltAccordionPanel v-for="(item, i) in items" :key="item.title" :value="i">
            <VoltAccordionHeader>
              {{ i }}
            </VoltAccordionHeader>

            <VoltAccordionContent>
              {{ i }}
            </VoltAccordionContent>
          </VoltAccordionPanel>
        </VoltAccordion>
      </template>
    </VoltCard>

    <VoltCard class="bg-primary-100 shadow-sm">
      <template #content>
        <VoltAccordion :value="0">
          <VoltAccordionPanel v-for="(item, i) in items" :key="item.title" :value="i">
            <VoltAccordionHeader>
              {{ item.title }}
            </VoltAccordionHeader>

            <VoltAccordionContent>
              {{ item.title }}
            </VoltAccordionContent>
          </VoltAccordionPanel>
        </VoltAccordion>
      </template>
    </VoltCard>
  </aside>
</template>

<script setup lang="ts">
const items = [{'title': 'First forum', 'content': 'Some content'}, {'title': 'Second forum', 'content': 'Some content'}]

const forumStore = useForums()
const { currentThread } = storeToRefs(forumStore)
</script>>
