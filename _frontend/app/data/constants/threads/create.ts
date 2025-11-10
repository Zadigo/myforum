export const threadTypes = [
  'General discussion',
  'Result',
  'WWW',
  'Bombshell',
  'Draw',
  'Poll'
] as const

export type ThreadTypes = (typeof threadTypes)[number]

export const roundTypes = [
  'QF1',
  'QF2',
  '1st',
  '2nd',
  '3rd',
  '4th',
  'QF',
  'SF',
  'F'
] as const

export type RoundTypes = (typeof roundTypes)[number]
