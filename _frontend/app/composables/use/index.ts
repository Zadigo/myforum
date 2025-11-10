export * from './search'
export * from './thread'

export function useDialog() {
  const props = defineProps<{ modelValue: boolean}>()
  const emit = defineEmits<{ 'update:modelValue': [boolean] }>()

  const show = useVModel(props, 'modelValue', emit, { defaultValue: false })

  return {
    show
  }
}
