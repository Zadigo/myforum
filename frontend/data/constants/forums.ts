export const sortMethodNames = [
  'Sort alphabetically A-Z',
  'Sort alphabetically Z-A',
  'Most recent',
  'Number of comments'
] as const

export type SortMethodNames = (typeof sortMethodNames)[number]

export const sortMethods: { label: SortMethodNames }[] = [
  {
    label: 'Sort alphabetically A-Z'
  },
  {
    label: 'Sort alphabetically Z-A'
  },
  {
    label: 'Most recent'
  },
  {
    label: 'Number of comments'
  }
]
