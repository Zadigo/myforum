import type { MenuItem } from 'primevue/menuitem'

export const sortMethodNames = [
  'Sort alphabetically A-Z',
  'Sort alphabetically Z-A',
  'Most recent',
  'Number of comments'
] as const

export enum SortMethods {
  AlphabeticalAZ = 'Sort alphabetically A-Z',
  AlphabeticalZA = 'Sort alphabetically Z-A',
  MostRecent = 'Most recent',
  NumberOfComments = 'Number of comments'
}

export type SortMethodNames = `${SortMethods}`

export interface SortMenuItem extends MenuItem {
  label: SortMethodNames
}
