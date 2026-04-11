import type { MenuItem } from "primevue/menuitem"

export const sortMethodNames = [
  'Sort alphabetically A-Z',
  'Sort alphabetically Z-A',
  'Most recent',
  'Number of comments'
] as const

export type SortMethodNames = (typeof sortMethodNames)[number]

export interface SortMenuItem extends MenuItem {
  label: SortMethodNames
}
