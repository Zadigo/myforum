<template>
  <div class="accordion" id="forums">
    <div v-for="item in computedItems" :key="item.id"  class="accordion-item">
      <h2 :id="`heading-${item.id}`" class="accordion-header">
        <button :aria-expanded="item.show" :aria-controls="`panel-${item.id}`" class="accordion-button" type="button" @click="closeItem(item)">
          {{ item.title }}
        </button>
      </h2>

      <transition name="slide-transition">
        <!-- :class="{ show: item.show }" -->
        <div v-if="item.show" :id="`panel-${item.id}`" :aria-labelledby="`heading-${item.id}`" class="accordion-collapse collapse show">
          <div class="accordion-body">
            {{ item.content }}
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import _ from 'lodash'

export default {
  name: 'BaseAccordion',
  props: {
    id: {
      type: String,
      default: 'accordion'
    },
    items: {
      type: Array,
      required: true
    }
  },
  data: () => ({
    computedItems: []
  }),
  methods: {
    closeItem(item) {
      // _.forEach(this.computedItems, (item) => {
      //   item.show = false
      // })
      item.show = !item.show
    }
  },
  beforeMount() {
    this.computedItems = _.map(this.items, (item, i) => {
      item['id'] = i
      item['show'] = false
      return item
    })
  }
}
</script>

<style scoped>
.slide-transition-enter-active,
.slide-transition-leave-active {
  transition: all .3s ease-in;
}
.slide-transition-enter-from,
.slide-transition-leave-to {
  opacity: 0;
  transform: translateY(-50px);
}
.slide-transition-enter-to,
.slide-transition-leave-from {
  opacity:1;
  transform: translateY(0px);
}
</style>
