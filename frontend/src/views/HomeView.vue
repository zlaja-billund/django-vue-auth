<script setup>
  import { useLoading } from "vue-loading-overlay";
  
  import AuthLayout from '@/layouts/AuthenticatedLayout.vue';



  const $loading = useLoading({
    canCancel: false,
    color: '#0D2F41',
    height: 128,
    width: 128,
  });


</script>

<template>
  <AuthLayout>
    <h1>Hello world it works</h1>

    <router-link :to="{ name: 'Logout' }" >Logout here</router-link>

  </AuthLayout>
  
</template>

<style scoped lang="scss">
@use '../assets/main';

</style>