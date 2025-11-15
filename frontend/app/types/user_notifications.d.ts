import type { Profile } from './accounts'

export interface UserNotification {
  id: number
  user: Pick<Profile, 'id' | 'username'>
  message: number
  read: string
  created_on: string
}
