<template>
  <!-- dropdown-center dropup dropend dropstart -->
  <div ref="drop" class="dropdown">
    <button :id="id" :class="buttonClasses" :aria-expanded="show" class="btn dropdown-toggle" type="button" @click="toggle">
      <!-- <span v-if="icon" :class="{ [`mdi-${icon}`]: true }" class="mdi me-2"></span> -->
      <font-awesome-icon :icon="`fa-solid fa-${icon}`" class="mdi me-2" />
      {{ buttonName }}
    </button>

    <!-- :name="animation" -->
    <transition :name="animation" mode="in-out">
      <!-- dropdown-menu-end -->
      <ul v-if="show" :class="{show, 'dropdown-menu-dark': darkMode}" :aria-labelledby="id" class="dropdown-menu">
        <!-- <li><h6 class="dropdown-header">Dropdown header</h6></li> -->
        <li v-for="(item, i) in items" :key="item.name">
          <a class="dropdown-item" href @click.prevent="dropdownClick(i, item)">
            <!-- <span v-if="item.icon" :class="{ [`mdi-${item.icon}`]: true }" class="mdi me-2"></span> -->
            <font-awesome-icon v-if="item.icon" :icon="`fa-solid fa-${item.icon}`" class="mdi me-2" />
            {{ item.name }}
          </a>
        </li>
        <!-- <li><hr class="dropdown-divider"></li> -->
      </ul>
    </transition>
  </div>
</template>

<script>
// import { onClickOutside } from '@vueuse/core'
import { ref, inject } from 'vue'

export default {
  name: 'BaseDropdownButton',
  props: {
    animation: {
      type: String,
      default: 'slideup'
    },
    buttonName: {
      type: String
    },
    color: {
      type: String,
      default: 'primary'
    },
    icon: {
      type: String
    },
    id: {
      type: String,
      required: true
    },
    items: {
      type: Array,
      required: true
    },
    size: {
      type: String,
      default: 'md'
    }
  },
  emits: {
    'dropdown-click' () {
      return true
    },
    'dropdown-closed' () {
      return true
    },
    'dropdown-opened' () {
      return true
    }
  },
  setup () {
    const target = ref(null)
    const show = ref(false)
    const darkMode = inject('darkMode')
    // onClickOutside(target, () => {
    //   show.value = false
    // })
    return {
      darkMode,
      show,
      target
    }
  },
  computed: {
    buttonClasses () {
      return [
        this.show ? 'show' : null,
        {
          [`btn-${this.color}`]: true,
          [`btn-${this.size}`]: true
        }
      ]
    }
  },
  watch: {
    show (current) {
      if (!current) {
        this.$emit('dropdown-closed')
      } else {
        this.$emit('dropdown-opened')
      }
    }
  },
  mounted () {
    const dropdown = this.$refs.drop
    const button = dropdown.querySelector('button')
    const buttonWidth = button.offsetWidth
    console.log(buttonWidth)
    //   this.$refs.link.style.animation = `${this.animation} .3s ease`
    //   var body = document.querySelector('body')
    //   body.addEventListener('click', (e) => {
    //       // console.log(e)
    //       if (!e.target.classList.contains('dropdown')) {
    //           this.show = !this.show
    //       }
    //   })
  },
  methods: {
    toggle () {
      this.show = !this.show
    },
    dropdownClick (index, item) {
      this.toggle()
      this.$emit('dropdown-click', [index, item])
    }
  }
}  
</script>

<style scoped>
.scale-enter-active,
.scale-leave-active {
  position: absolute;
  transition: all .3s ease;
  margin: 0px;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(.9, .9);
}

.scale-enter-to,
.scale-leave-from {
  opacity: 1;
  transform: scale(1, 1);
}

.slide-enter-active,
.slide-leave-active {
  position: absolute;
  transition: all .3s ease;
  margin: 0px;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(-15px);
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  transform: translateX(0px);
}

.slideup-enter-active,
.slideup-leave-active {
  position: absolute;
  transition: all .3s ease;
  margin: 0px;
}

.slideup-enter-from,
.slideup-leave-to {
  opacity: 0;
  transform: translateY(15px);
}

.slideup-enter-to,
.slideup-leave-from {
  opacity: 1;
  transform: translateY(0px);
}
</style>
