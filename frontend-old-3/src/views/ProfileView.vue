<template>
  <section id="profile" class="my-5">
    <div class="container">
      <div class="row">
        <div class="col-4">
          <div class="card">
            <img src="https://via.placeholder.com/600x600" class="img-card-top">
            <!-- <div class="card-body">
            </div> -->
          </div>
        </div>

        <div class="col-8">
          <div class="card">
            <div class="card-body">
              <h3 class="card-title">
                {{ user.username }}
              </h3>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapState } from 'pinia';
import { useAuthentication } from '../store/authentication';

export default {
  name: 'ProfileView',
  computed: {
    ...mapState(useAuthentication, ['user'])
  }
}
</script>
