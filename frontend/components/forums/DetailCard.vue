<template>
  <article v-for="category in forumCategories" :key="category" :aria-label="category" class="row mb-5">
    <div class="col-12">
      <h3>{{ category }}</h3>
    </div>

    <div class="col-12">
      <div v-for="(forum, i) in forumsByCategory[category]" :key="forum.id" :class="{ 'mt-1': i > 0 }" :aria-label="forum.title" class="card shadow-sm" role="article">
        <div class="card-body">
          <NuxtLink :to="`/forums/${forum.id}`" class="text-dark">
            <div class="card-body">
              <h3 class="card-title">
                {{ forum.title }}
              </h3>

              <p class="card-text fw-light">{{ forum.description }}</p>

              <div class="card-info">
                <span class="badge bg-info p-2">{{ forum.number_of_threads }} <font-awesome icon="users" /></span>
                <span class="badge bg-info p-2 ms-2">200000 <font-awesome icon="eye" /></span>
                <span class="badge bg-info p-2 ms-2">{{ forum.created_on }}</span>
              </div>
            </div>
          </NuxtLink>
        </div>
      </div>
    </div>
  </article>
</template>

<script setup lang="ts">
// const { getForums } = useForumsComposable()
// const { forumCategories, forumsByCategory } = storeToRefs(useForums())

// onBeforeMount(getForums)

const { forumsList, forumCategories, forumsByCategory } = storeToRefs(useForums())

useFetch('/api/forums', {
  transform(data: Forum) {
    forumsList.value = data
    return data
  }
})
</script>
