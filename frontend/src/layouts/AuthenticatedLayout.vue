<script setup>
  import { storeToRefs } from 'pinia';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

</script>


<template>
    <main class="main-container">
        <slot />             
    </main>
        
    
</template>

<style scoped lang="scss">
@use '../assets/main.scss'
    
</style>