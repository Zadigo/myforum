<template>
<div class="dropdown">
  <button ref="link" :id="buttonName.toLowerCase()" :aria-expanded="expanded" class="btn btn-light text-dark shadow-none btn-md dropdown-toggle" type="button">
    <span v-if="icon" :class="`mdi-${icon}`" class="mdi me-2"></span>
    {{ buttonName }}
  </button>

  <transition name="scale">
    <ul ref="dropdown" v-if="expanded" :class="{ show: expanded }" :aria-labelledby="buttonName" class="dropdown-menu">
      <li v-for="item in items" :key="item.name">
        <a class="dropdown-item" href @click.prevent="$emit('dropdown-click', item)">
          {{ item.name }}
        </a>
      </li>
    </ul>
  </transition>
</div>
</template>

<script>
// import { indexElements } from '../utils'

export default {
  name: 'DropdownButton',
  emits: ['dropdown-click'],
  props: {
    buttonName: {
      type: String
    },
    icon: {
      type: String,
      default: null
    },
    items: {
      // { name, disabled, to }
      type: Array
    }
  },
  data: () => ({
    expanded: false
  }),
  beforeMount() {
    // var items = indexElements(this.items)
    
    // Allows for closing the dropdown
    // menu when clicking outside
    // var self = this
    // window.onclick = function (e) {
    //   if (!e.target.matches('.dropdown-menu')) {
    //     self.expanded = false
    //   }
    // }
  },
  mounted() {
    this.$refs.link.addEventListener('click', this.toggle, { passive: true })
  },
  beforeUnmount() {
    this.$refs.link.removeEventListener('click', this.toggle)
  },
  methods: {
    toggle() {
      var dropdown = this.$refs.dropdown

      this.expanded = !this.expanded
      
      // if (this.expanded) {
      //   dropdown.style.position = 'absolute'
      //   dropdown.style.inset = '0px auto auto auto 0px'
      //   dropdown.style.margin = '0px'
      // }
    }
  }
}
</script>

<style scoped>
.dropdown-menu {
  /* position: absolute; */
  /* display: inline-block; */
  /* max-width: 80%; */
  overflow-y: auto;
  overflow-x: hidden;
  contain: content;
  box-shadow: 0 5px 5px -3px rgb(0 0 0 / 20%), 0 8px 10px 1px rgb(0 0 0 / 14%), 0 3px 14px 2px rgb(0 0 0 / 12%);
  /* border-radius: 4px; */
  font-size: 1rem;
}
.dropdown-menu.show {
  display: block;
}
.fade-enter-active,
.fade-leave-active {
  transition: all .2s ease-in;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translate(10px, 20px);
}
.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translate(0px, 0px);
}

.scale-enter-active,
.scale-leave-active {
  transition: all .2s linear;
}
.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9, 0.9);
}
.scale-enter-to,
.scale-leave-from {
  opacity: 1;
  transform: scale(1, 1);
}
</style>
