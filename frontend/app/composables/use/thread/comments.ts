import type { Delta } from '@vueup/vue-quill'
import type { Arrayable, EditorData, LatestComments, RouteIdParamsGeneric, Undefineable } from '~/types'

export interface NewComment {
  thread: string | number
  title: string
  content: string
  content_delta: Undefineable<string | Delta>
  content_html: string
  quotes: Arrayable<number>
}

/**
 * Composable for creating a new comment
 */
export function useCreateCommentComposable() {
  const { id } = useRoute().params as RouteIdParamsGeneric
  const newComment = ref<NewComment>({
    thread: id,
    title: '',
    content: '',
    content_delta: undefined,
    content_html: '',
    quotes: [],
  })

  // const { customHandleError } = useErrorHandler()
  const { $nuxtAuthentication } = useNuxtApp()

  async function _create(callable?: () => void) {
    try {
      await $nuxtAuthentication('/v1/comments/create', { method: 'POST', body: newComment.value })
      callable?.()
    } catch (e) {
      // customHandleError(e)
      console.error(e)
    }
  }

  async function _saveDraft(callable?: () => void) {
    try {
      await $nuxtAuthentication('/v1/comments/create', { method: 'POST', body: newComment.value })
      callable?.()
    } catch (e) {
      // customHandleError(e)
      console.error(e)
    }
  }

  const create = useThrottleFn(_create, 5000)
  const saveDraft = useThrottleFn(_saveDraft, 5000)

  //
  function writeEditorContent(data: EditorData) {
    newComment.value.content = data.text
    newComment.value.content_html = data.html
    newComment.value.content_delta = data.delta
  }

  return {
    /**
     * New comment being created
     */
    newComment,
    /**
     * Create the new comment
     */
    create,
    /**
     * Save the new comment as a draft
     */
    saveDraft,
    /**
     * Write editor content to new comment
     */
    writeEditorContent
  }
}

export const useLatestCommentsComposable = createGlobalState(async <T extends LatestComments>() => {
  const requestComplete = ref<boolean>(false)
  
  const comments = await $fetch<T>('/api/comments/latest', {
    method: 'GET',
    onResponse() {
      requestComplete.value = true
    }
  })


  return {
    comments,
    requestComplete
  }
})
