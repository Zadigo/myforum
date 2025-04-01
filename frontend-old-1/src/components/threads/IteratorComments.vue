<template>
  <div id="comments">
    <article v-for="(comment, i) in comments" :key="comment.id" :id="`post-${comment.id}`" class="card mb-2">
      <!-- <div class="card-toolbar shadow-none">
        <div class="card-toolbar-content">
          {{ comment.title }}

          <button class="btn btn-rounded btn-icon">
            <span class="mdi mdi-dots-vertical" />
          </button>
        </div>
      </div> -->

      <div class="card-body">
        <div class="mb-4">
          <span class="fw-bold text-muted">#{{ comment.id }}</span> <span class="mx-2">-</span> <span
            class="text-muted">{{ formatDate(comment.created_on) }}</span>
        </div>
        {{ comment.content }}
      </div>

      <div v-if="showActions" class="card-actions ms-auto ">
        <div v-if="isAuthenticated" class="btn-group">
          <button class="btn btn-md btn-outline-primary" @click="$emit('reply', comment)">Reply</button>
          <button class="btn btn-md btn-outline-primary" @click="quoteFrom">Quote from</button>
          <button class="btn btn-md btn-outline-primary" @click="bookmark">Bookmark</button>
          <button class="btn btn-md btn-outline-primary" @click="share">Share</button>
        </div>

        <div v-else class="btn-group">
          <button class="btn btn-md btn-dark" @click="authStore.openLoginModal = true">Reply</button>
          <button class="btn btn-md btn-dark" @click="authStore.openLoginModal = true">Quote from</button>
          <button class="btn btn-md btn-dark" @click="authStore.openLoginModal = true">Bookmark</button>
          <button class="btn btn-md btn-dark" @click="authStore.openLoginModal = true">Share</button>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
import { mapState } from 'pinia'
import dayjs from '../../plugins/dayjs'
import { useAuthentication } from '@/stores//authentication'

export default {
  name: 'IteratorComments',
  emits: ['reply'],
  setup() {
    var authStore = useAuthentication()
    return {
      authStore,
      dayjs
    }
  },
  props: {
    comments: {
      type: Array,
      required: true
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    ...mapState(useAuthentication, ['isAuthenticated'])
  }, 
  methods: {
    formatDate(d) {
      return this.dayjs(d).format('ddd, MMM YYYY')
    },
    quoteFrom() {
      // pass
    },
    bookmark() {
      // pass
    },
    share() {
      // pass
    }
  }
}
</script>

<style scoped>
.card-toolbar {
  contain: layout;
  display: block;
  flex: 1 1 auto;
  max-width: 100%;
  transition: transform .2s cubic-bezier(.4,0,.2,1),background-color .2s cubic-bezier(.4,0,.2,1),left .2s cubic-bezier(.4,0,.2,1),right .2s cubic-bezier(.4,0,.2,1),box-shadow .28s cubic-bezier(.4,0,.2,1),max-width .25s cubic-bezier(.4,0,.2,1),width .25s cubic-bezier(.4,0,.2,1);
  position: relative;
  background-color: #fff;
  border-top-left-radius: .5rem;
  border-top-right-radius: .5rem;
  box-shadow: 0 10px 15px -3px rgb(0 0 0 / 7%), 0 4px 6px -2px rgb(0 0 0 / 5%);
}
.card-toolbar .card-toolbar-content {
  padding: 4px 16px;
  height: 64px;
}
.btn-icon {
  color: rgba(0,0,0,.54);
  min-height: 0;
  min-width: 0;
  padding: 0;
  /* box-shadow: none; */
  height: 48px;
  width: 48px;
}
/* .card-actions {
  align-items: center;
  display: flex;
  padding: 8px;
}
.card-actions > .btn {
  padding: 0 8px;
} */
</style>
