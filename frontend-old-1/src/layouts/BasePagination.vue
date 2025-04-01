<template>
  <nav aria-label="...">
    <ul class="pagination pagination-md">
      <li :class="{ disabled: currentPage <= 1 }" class="page-item">
        <a class="page-link" href @click.prevent="getPreviousPage">
          Previous
        </a>
      </li>

      <template v-if="pages <= 3">
        <li v-for="page in pages" :key="page" :class="{ active: currentPage == page }" :aria-current="currentPage === page ? 'page' : null" class="page-item">
          <a class="page-link" href :aria-labelledby="`Page ${page}`" @click.prevent="getPage(page)">
            {{ page }}
          </a>
        </li>
      </template>
      
      <template v-else>
        <li v-for="page in 3" :key="page" :class="{ active: currentPage == page }" :aria-current="currentPage === page ? 'page' : null" class="page-item">
          <a class="page-link" href :aria-labelledby="`Page ${page}`" @click.prevent="getPage(page)">
            {{ page }}
          </a>
        </li>

        <li class="page-item">
          <a class="page-link" href @click.prevent>
            ...
          </a>
        </li>

        <li :class="{ active: currentPage == pages }" :aria-current="currentPage === pages ? 'page' : null" class="page-item">
          <a class="page-link" href :aria-labelledby="`Page ${pages}`" @click.prevent="getPage(pages)">
            {{ pages }}
          </a>
        </li>
      </template>
      
      <li :class="{ disabled: currentPage == pages }" class="page-item">
        <a class="page-link" href @click.prevent="getNextPage">
          Next
        </a>
      </li>
    </ul>
  </nav>
</template>

<script>
import { scrollToTop } from '../utils'

export default {
  name: 'BasePagination',
  emits: ['get-page'],
  props: {
    pages: {
      type: Number,
      default: 1
    },
    // Allows for multiple pagination instances
    // to sync the current page that is seen
    syncCurrentPage: {
      type: Number,
      default: 1
    }
  },
  data: () => ({
    currentPage: 1
  }),
  watch: {
    syncCurrentPage(newValue) {
      if (newValue !== this.currentPage) {
        this.currentPage = this.syncCurrentPage
      }
    }
  },
  beforeMount() {
    var existingCurrentPage = this.$session.retrieve('currentPage')

    this.currentPage = existingCurrentPage ? existingCurrentPage : 1
  },
  methods: {
    getPage(page) {
      this.currentPage = page
      scrollToTop()

      // Remember the current page anything
      // the user is currently viewing so that
      // on refresh we can get it back
      this.$session.create('currentPage', page)

      this.$emit('get-page', page)
    },
    getPreviousPage() {
      var result = this.currentPage - 1
      result = result <= 1 ? 1 : result

      this.currentPage = result
      scrollToTop()
      this.$emit('get-page', result)
    },
    getNextPage() {
      var result = this.currentPage + 1
      result = result == this.pages ? 1 : result

      this.currentPage = result
      scrollToTop()
      this.$emit('get-page', result)
    }
  }
}
</script>
