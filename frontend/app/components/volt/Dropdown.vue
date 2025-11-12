<template>
  <div class="card flex justify-center">
    <slot :attrs="{ toggle }" />

    <volt-menu :id="id" ref="menuEl" :model="items" :popup="true" />
  </div>
</template>

<script setup lang="ts">
interface MenuItem {
  label: string
  icon?: string
  command?: () => void
}

defineProps<{ id: string, items: MenuItem[] }>()

const menuEl = useTemplateRef('menuEl')

function toggle(event: Event) {
  if (isDefined(menuEl)) {
    menuEl.value.toggle(event)
  }
}
</script>
