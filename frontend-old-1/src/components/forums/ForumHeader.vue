<template>
  <base-page-header-vue>
    <template #title>
      {{ currentForum.title }}
    </template>

    <template #breadcrumbs>
      <li class="breadcrumb-item active" aria-current="page">
        {{ currentForum.title }}
      </li>
    </template>

    <template #actions>
      <div class="btn-group">
        <button class="btn btn-lg btn-info" @click="$emit('follow')">
          Follow forum
        </button>

        <router-link :to="{ name: 'create_thread_view' }" class="btn btn-lg btn-primary">
          New thread
        </router-link>
      </div>
    </template>
  </base-page-header-vue>
</template>

<script>
import { mapState } from 'pinia'
import { useForum } from '@/stores//forum'

import BasePageHeaderVue from '../../layouts/BasePageHeader.vue'

export default {
  name: 'ForumHeader',
  emits: ['follow', 'new-thread'],
  components: {
    BasePageHeaderVue
  },
  computed: {
    ...mapState(useForum, ['currentForum'])
  }
}
</script>
