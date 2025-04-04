<template>
  <aside>
    <div class="card bg-blue-300 shadow-sm">
      <div class="card-body">
        <h5 class="card-title mb-3">
          About this Discussion
        </h5>
  
        <!-- <p class="card-text mb-1">
          <span class="fw-bold h4">{{ numberOfComments }}</span> replies
        </p>
        
        <p class="card-text mb-0">
          <span class="fw-bold h4">{{ currentThread?.participants.length || 0 }}</span> participants
        </p> -->

        <hr>

        <!-- TODO: Create a different aside for WhatsNew -->
        <!-- <p class="card-text">
          Last post from <NuxtLink to="/" class="text-decoration">{{ currentThread.latest_comment.user__username }}</NuxtLink> 
          {{ formatDuration(currentThread.latest_comment.created_on) }}  
        </p> -->
      </div>
    </div>    

    <div class="card bg-blue-300 shadow-sm my-2">
      <div class="card-body">

        <div class="card-title">
          Tennis Forum
        </div>
  
        <div class="card-text">
          A forum community dedicated to Tennis players and enthusiasts. Come join the discussion 
          about players, gear, matches, scores, guidelines, and more!
  
          <hr>
  
          <NuxtLink to="/">
            Other threads
          </NuxtLink>

  
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
        </div>
      </div>
    </div>

    <div class="card bg-blue-300 shadow-sm">
      <div class="card-body">
        <!-- <base-accordion-vue :items="[{'title': 'First forum', 'content': 'Some content'}, {'title': 'Second forum', 'content': 'Some content'}]" /> -->
      </div>
    </div>
  </aside>
</template>
