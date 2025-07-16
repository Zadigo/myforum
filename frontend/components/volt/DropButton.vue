<template>
  <div class="card flex justify-center">
    <slot name="button" :toggle="handleToggle">
      <VoltButton :aria-controls="id" :aria-haspopup="isOpen ? 'true' : 'false'" type="button" plain @click="handleToggle">
        <slot />
      </VoltButton>
    </slot>

    <VoltMenu :id="id" ref="menuEl" :model="items" :popup="true" />
</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import type { VoltMenu } from '#components';

defineEmits<{ items: { label: [] }}>()
defineProps<{ id?: string, items: { label: string }[] }>()

const menuEl = useTemplateRef<typeof VoltMenu>('menuEl')

const isOpen = ref<boolean>(false)

/**
 * 
 * @param e 
 */
function handleToggle(e: Event) {
  menuEl.value?.toggle(e)
}
</script>
