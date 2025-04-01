<template>
  <transition name="modal">
    <div ref="link" class="modal" tabindex="-1" role="dialog">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title d-none">Modal title</h5>
            <button type="button" class="btn-close" aria-label="Close" @click="$emit('modal-close')"/>
          </div>

          <div class="modal-body">
            <slot />
          </div>
          
          <div class="modal-footer d-none">
            <button type="button" class="btn btn-secondary">Close</button>
            <button type="button" class="btn btn-primary">Save changes</button>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { useBackdrop } from '../composables/backdrop'

export default {
  name: 'BaseModal',
  emits: ['modal-close'],
  setup() {
    var { removeBackdrop, createBackdrop } = useBackdrop()
    return {
      removeBackdrop,
      createBackdrop
    }
  },
  props: {
    show: {
      type: Boolean
    }
  },
  mounted() {
    if (this.show) {
      this.diplayModal()
      this.createBackdrop()
    }
  },
  watch: {
    show(newValue) {
      if (newValue) {
        this.diplayModal()
      } else {
        this.hideModal()
      }
    }
  },
  computed: {
    modalClasses() {
      return [
        this.show ? 'show' : null,
        'fade'
      ]
    }
  },
  methods: {
    diplayModal() {
      this.$refs.link.classList.add('show')
      
      var html = document.querySelector('html')
      html.style.overflow = 'hidden'

      this.createBackdrop()
    },
    hideModal() {
      this.$refs.link.classList.remove('show')
      
      var html = document.querySelector('html')
      html.style.overflow = 'scroll'
      
      this.removeBackdrop()
    }
  }
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: .3s ease-in-out;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
  transform: scale(0.9, 0.9);
}
.modal-enter-to,
.modal-leave-from {
  opacity: 1;
  transform: scale(1, 1);
}
.modal {
  transition: all .3s ease;
}
.modal.show {
  display: block;
  animation: 0.3s cubic-bezier(0.165, 0.84, 0.44, 1) scale;
}
@keyframes scale {
  0% {
    opacity: 0;
    transform: scale(0.9, 0.9);
  }
  50% {
    transform: scale(1.1, 1.1);
  }
  100% {
    opacity: 1;
    transform: scale(1, 1);
  }
}
.dropdown-backdrop {
  transition: all .3s ease;
  animation: opacity .3s ease;
  z-index: 1052;
}
@keyframes opacity {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.5;
  }
  100% {
    opacity: 1;
  }
}
</style>
