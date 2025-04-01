<template>
  <base-page-header-vue>
    <template #title>
      {{ currentThread.title }}
    </template>

    <template #breadcrumbs>
      <li class="breadcrumb-item">
        <router-link :to="{ name: 'forum_view', params: { id: currentForum.id } }">
          {{ currentForum.title }}
        </router-link>
      </li>
      <li class="breadcrumb-item active" aria-current="page">
        {{ currentThread.title }}
      </li>
    </template>

    <template #actions>
      <div class="btn-group">
        <button class="btn btn-lg btn-info" @click="$emit('jump-to-latest')">
          Jump to latest
        </button>

        <button class="btn btn-lg btn-info" @click="$emit('follow')">
          Follow thread
        </button>
        
        <button class="btn btn-lg btn-danger" @click="$emit('delete')">
          Delete
        </button>
        
        <button class="btn btn-lg btn-primary" @click="$emit('new-comment')">
          New comment
        </button>
      </div>
    </template>
  </base-page-header-vue>
</template>

<script>
import BasePageHeaderVue from '../../layouts/BasePageHeader.vue'
import { mapState } from 'pinia'
import { useForum } from '@/stores//forum'
import { useAuthentication } from '@/stores//authentication'

export default {
  name: 'ThreadHeader',
  emits: ['jump-to-latest', 'follow', 'delete', 'new-comment'],
  components: {
    BasePageHeaderVue
  },
  computed: {
    ...mapState(useForum, ['currentThread', 'currentForum']),
    ...mapState(useAuthentication, ['user']),
    userCreatedThread() {
      if (!this.user) {
        return false
      }
      return this.currentThread.user.id == this.user.id
    }
  }
}
</script>
