<template>
  <div>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title mb-3">
          About this Discussion
        </h5>
  
        <p class="card-text mb-1"><span class="fw-bold h4">{{ numberOfComments }}</span> replies</p>
        <p class="card-text mb-0"><span class="fw-bold h4">29</span> participants</p>

        <hr>

        <!-- TODO: Create a different aside for WhatsNew -->
        <!-- <p class="card-text">
          Last post from <router-link :to="{ name: 'forums_view'}" class="text-decoration">{{ currentThread.latest_comment.user__username }}</router-link> {{ formatDuration(currentThread.latest_comment.created_on) }}  
        </p> -->
      </div>
    </div>    

    <div class="card mt-2">
      <div class="card-body">

        <div class="card-title">
          Tennis Forum
        </div>
  
        <div class="card-text">
          A forum community dedicated to Tennis players and enthusiasts. Come join the discussion 
          about players, gear, matches, scores, guidelines, and more!
  
          <hr>
  
          <router-link :to="{ name: 'forums_view' }">Other threads</router-link>

  
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

    <base-accordion-vue :items="[{'title': 'First forum', 'content': 'Some content'}, {'title': 'Second forum', 'content': 'Some content'}]" />
  </div>
</template>

<script>
import dayjs from '../../plugins/dayjs'
import { storeToRefs } from 'pinia'
import BaseAccordionVue from '../../layouts/BaseAccordion.vue'
import { useForum } from '@/stores//forum'

export default {
  name: 'ThreadAside',
  setup() {
    const store = useForum()
    const { currentThread } = storeToRefs(store)
    return {
      currentThread
    }
  },
  props: {
    numberOfComments: {
      type: Number,
      default: 0
    }
  },
  components: {
    BaseAccordionVue
  },
  methods: {
    formatDuration(d) {
      const d = dayjs(d)
      const currentDate = dayjs()
      return dayjs.duration(d.diff(currentDate), 'days').humanize(true)
    }
  }
}
</script>
