<template>
    <div class="container-fluid min-vh-100 d-flex flex-column ">
        <div class="row flex-grow-1">
            <div class="col-4 bg-col-left position-relative">
                <main class="align-items-center">
                    <slot />
                </main>                
            </div>
            <div class="col-8 p-0 m-0 background-image">
            </div>
        </div>
    </div>
</template>


<style scoped lang="scss">
@use '../assets/scss' as c;

.background-image {
    background-image:url('/images/background-image.jpg');
    background-repeat:no-repeat;
    background-size:cover;
    background-position:center;
}

.bg-col-left {
    background: transparent linear-gradient(180deg, c.$auth-bg-dark 0%, c.$auth-bg-darker 0%, c.$auth-bg-blue-light 100%) 0% 0% no-repeat padding-box;
    opacity: 1;
    padding-left: 5%;
    padding-right: 5%;
}

main {
    margin: 0;
    position: relative;
    top: 50%;
    -ms-transform: translateY(-50%);
    transform: translateY(-50%);
}

</style>