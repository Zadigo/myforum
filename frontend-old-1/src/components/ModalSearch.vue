<template>
  <base-modal-vue :show="store.openSearchModal" @modal-close="store.openSearchModal=false">
    <template #default>
      <input v-model="search" type="search" class="form-control p-3" placeholder="Search website" @keypress.enter="goToSearch">

      <div class="row my-3">
        <div class="col-12">
          <p class="fw-bold">Recent</p>

          <ul class="list-group">
            <a v-for="(item, i) in searchHistory" :key="i" href class="list-group-item list-group-item-action p-3 fw-normal d-flex justify-content-between" @click.prevent>
              <router-link :to="{ name: 'search_view', query: { q: item } }" class="text-dark">
                <span class="mdi mdi-history me-2"></span>
                <span>{{ item }}</span>
              </router-link>

              <div>
                <button class="btn btn-sm btn-primary btn-rounded me-2" @click="saveSearch(i)">
                  <span class="mdi mdi-star"></span>
                </button>

                <button class="btn btn-sm btn-primary btn-rounded" @click="deleteSearch(i)">
                  <span class="mdi mdi-close"></span>
                </button>
              </div>
            </a>
          </ul>
        </div>
      </div>
    </template>
  </base-modal-vue>
</template>

<script>
// import { storeToRefs } from 'pinia'
import { useForum } from '../store/forum'
import _ from 'lodash'

import BaseModalVue from '../layouts/BaseModal.vue'

export default {
  name: 'ModalSearch',
  setup() {
    var store = useForum()
    return {
      store
    }
  },
  components: {
    BaseModalVue
  },
  data: () => ({
    search: '',
    searchHistory: []
  }),
  beforeMount() {
    this.searchHistory = _.uniq(this.$session.retrieve('query'))
  },
  methods: {
    saveSearch() {
      console.log('saveSearch')
    },
    deleteSearch(index) {
      index
      // var history = this.$session.retrieve('query')
      // history.splice()
      // this.$session.create('query', history)
    },
    goToSearch() {
      this.$session.listPush('query', this.search)
      this.$router.push({ name: 'search_view', query: { q: this.search } })
      this.search = null
      this.store.openSearchModal = false
    }
  }
}
</script>
