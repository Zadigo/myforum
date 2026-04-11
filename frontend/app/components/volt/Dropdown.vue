<template>
  <div class="card flex justify-center">
    <slot :attrs="{ toggle }" />

    <volt-popover v-if="isPopover" :id="id" ref="menuEl">
      <slot name="popover-content" />
    </volt-popover>

    <volt-menu v-else :id="id" ref="menuEl" :model="items" :popup="true" />
  </div>
</template>

<script setup lang="ts">
import type { MenuItemCommandEvent } from 'primevue/menuitem';

interface MenuItem {
  label: string
  icon?: string
  command?: (event: MenuItemCommandEvent) => void
}

const { id, isPopover = false, items = [] } = defineProps<{ id: string, isPopover?: boolean, items?: MenuItem[] }>()

const menuEl = useTemplateRef('menuEl')

function toggle(event: Event) {
  if (isDefined(menuEl)) {
    menuEl.value.toggle(event, event.target as HTMLElement)
  }
}
</script>
