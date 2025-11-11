import { doc, addDoc, collection } from 'firebase/firestore'
import type { Arrayable, Nullable } from '~/types'

export interface UserSession {
  accessToken: string
  lastVisited: Nullable<number>
  visited: Arrayable<number>
}

export async function useSession<S extends UserSession>() {
  if (import.meta.server) {
    return {
      sessionId: ref(null),
      session: ref<UserSession | null>(null),
    }
  }

  const sessionId = useCookie('forum-session-id')
  const fireStore = useFirestore()

  if (!isDefined(sessionId)) {
    const collectionRef = collection(fireStore, 'sessions')
    const data: UserSession = {
      accessToken: '',
      lastVisited: null,
      visited: [],

    }
    const newDoc = await addDoc(collectionRef, data)
    sessionId.value = newDoc.id
  }

  const docRef = doc(fireStore, 'sessions', sessionId.value || '')
  const session = useDocument<S>(docRef)

  return {
    sessionId,
    session
  }
}

export async function useSessionManager() {
  const { sessionId } = await useSession<UserSession>()

  function addVisited(id: string | number) {}

  function addLastVisited(id: string | number) {}

  return {
    addVisited,
    addLastVisited,
  }
}
