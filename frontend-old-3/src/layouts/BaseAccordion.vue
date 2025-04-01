<template>
  <div :id="'accordionExample'" :class="{'border-dark': darkMode}" class="accordion">
    <div v-for="(item, i) in computedItems" :key="i" class="accordion-item">
      <h2 id="headingOne" class="accordion-header">
        <button :class="{ collapsed: !item.show, 'bg-dark text-light': darkMode}" :aria-expanded="item.show" :aria-controls="'collapseOne'" class="accordion-button" type="button" @click="expandItem(item)">
          {{ item.title }}
        </button>
      </h2>

      <div v-if="item.show" :id="'collapseOne'" :class="{show: item.show, 'bg-dark text-light': darkMode}" class="accordion-collapse collapse" aria-labelledby="headingOne">
        <div class="accordion-body">
          {{ item.content }}
        </div>
      </div>
      <!-- <transition name="slide" mode="in-out">
      </transition> -->
    </div>
  </div>
</template>

<script>
import { inject } from 'vue'

export default {
  name: 'BaseAccordion',
  props: {
    items: {
      type: Array
    }
  },
  emits: {
    click () {
      return true
    }
  },
  setup () {
    const darkMode = inject('darkMode')
    return {
      darkMode
    }
  },
  data () {
    return {
      computedItems: []
    }
  },
  beforeMount () {
    this.computedItems = this.items.map((item) => {
      item.show = false
      return item
    })
  },
  methods: {
    expandItem (item) {
      item.show = !item.show
      this.$emit('click', item)
    }
  }
}
</script>

<style scoped>
/* .slide-enter-active,
.slide-leave-active {
  transition: all .3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(0%);
  transform: translate3d(0, -10%, 0);
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  transform: translateY(10%);
  transform: translate3d(0, 0, 0);
} */
.border-dark {
  border-color: #373b3e;
}
</style>
