<template>
  <div class=" container-fluid products">
    <Sell />

    <div class="row pt-5 mt-5" v-if="loadingAdverts">
        <div class="col-12 text-center">
            <h2>...loading wishlist items</h2>
        </div>
    </div>
    <div
      v-if="!noAdverts && !loadingAdverts"
      class="row  pt-5 mt-5 categories  px-3 mt-0 mb-2 text-center d-flex"
    >
      <div class="col-md-3 col-12" v-for="advert in adverts" :key="advert.id">
        <AdvertMinified
          :advert_object="advert"
          @remove="removeFromWishList(advert.slug, advert)"
        />
      </div>
    </div>

    <div
      class="row p-5  mt-5 mb-2 text-center d-flex justify-content-center"
      v-if="noAdverts && !loadingAdverts"
    >
      <div class="col-12 text-center">
        <h4 class="sub-heading mt-4 mb-2 text-danger">
          <strong> You haven't saved any item yet !!</strong>
        </h4>

        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import { apiService } from "@/common/api.service.js";

import { store } from "@/store/store";

import AdvertMinified from "@/components/Adverts/AdvertMinified.vue";

import Sell from "@/components/Others/Sell.vue";

export default {
  name: "wishlist",

  components: {
    AdvertMinified,
    Sell
  },

  data() {
    return {
      adverts: [],
      next: null,
      loadingAdverts: false,
      requestUser: null
    };
  },

  computed: {
    noAdverts() {
      if (this.adverts.length === 0) {
        return true;
      }
    }
  },

  methods: {
      
    getAdverts() {
      this.loadingAdverts = true;
      let get_adverts_url = "api/v1/user/wishlist/";

      if (this.next) {
        get_adverts_url = this.next.slice(22);
      }

      apiService(get_adverts_url, "GET").then(data => {
        this.adverts.push(...data.results);
        this.loadingAdverts = false; 

        if (data.next) {
          this.next = data.next;
        } else {
          this.next = null;
        }
      });
    },

    removeFromWishList(slug, advert) {
      let endpoint = `api/v1/user/wishlist/advert/${slug}/`;
      apiService(endpoint, "DELETE");

      let index = this.adverts.indexOf(advert);
      this.adverts.splice(index, 1);
    },

    setRequestUser() {
      this.requestUser = window.localStorage.getItem("username");
    }
  },

  mounted: function() {
    this.setRequestUser();
    this.getAdverts();
    document.title = "Wishlist";
  },

  async beforeRouteEnter(to, from, next) {
    let isAuth = store.state.isAuthenticated;
    if (isAuth === true) {
      next();
    } else {
      next({
        name: "continue" // back to safety route //
      });
    }
  }
};
</script>

<style scoped></style>
