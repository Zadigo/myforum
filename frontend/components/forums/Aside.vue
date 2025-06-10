<template>
  <aside>
    <VoltCard class="bg-blue-300 shadow-sm">
      <template #content>
        <h5 class="card-title mb-3">
          About this Discussion
        </h5>
  
        <!-- <p class="card-text mb-1">
          <span class="fw-bold h4">{{ numberOfComments }}</span> replies
        </p>
        
        <p class="card-text mb-0">
          <span class="fw-bold h4">{{ currentThread?.participants.length || 0 }}</span> participants
        </p> -->

        <VoltDivider />

        <!-- TODO: Create a different aside for WhatsNew -->
        <!-- <p class="card-text">
          Last post from <NuxtLink to="/" class="text-decoration">{{ currentThread.latest_comment.user__username }}</NuxtLink> 
          {{ formatDuration(currentThread.latest_comment.created_on) }}  
        </p> -->
      </template>
    </VoltCard>    

    <VoltCard class="bg-blue-300 shadow-sm my-2">
      <template #title>
        Tennis Forum
      </template>

      <template #content>
        A forum community dedicated to Tennis players and enthusiasts. Come join the discussion 
        about players, gear, matches, scores, guidelines, and more!

        <VoltDivider />

        <VoltButton>
          <NuxtLink to="/">
            Other threads
          </NuxtLink>
        </VoltButton>


        <!-- <v-expansion-panels>
          <v-expansion-panel v-for="(item, i) in 4" :key="i" accordion>
            <v-expansion-panel-header>
              Thread {{ i }}
            </v-expansion-panel-header>
            
            <v-expansion-panel-content>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt.
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels> -->
      </template>
    </VoltCard>

    <VoltCard class="bg-blue-300 shadow-sm">
      <template #content>
        <!-- <base-accordion-vue :items="[{'title': 'First forum', 'content': 'Some content'}, {'title': 'Second forum', 'content': 'Some content'}]" /> -->
      </template>
    </VoltCard>
  </aside>
</template>
