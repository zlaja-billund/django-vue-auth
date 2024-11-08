<script setup>
    import { ref } from 'vue';
    import { toTypedSchema } from '@vee-validate/yup';
    import { useRouter } from 'vue-router';
    import { useForm } from 'vee-validate';
    import * as yup from 'yup';
    import { useToast } from "vue-toastification";


    import GuestLayout from '../../layouts/GuestLayout.vue';
    import { useAuthStore } from '../../stores';

    const router = useRouter();

    const { errors, defineField} = useForm({
        validationSchema: toTypedSchema(
            yup.object({
                email: yup.string().email().required().label("E-mail"),
            }),
        ),
    });

    const [email, emailAttrs] = defineField('email', {
        validateOnModelUpdate: false,
    });

    const isLoading = ref(false);

    const onSubmit = async () => {
        isLoading.value = true;
                
        const authStore = useAuthStore();
        const toast = useToast();

        await authStore.requestResetPassword(email.value)
        .then((response) => {
            toast.success("The email has now been sent to you.");
            isLoading.value = false;
        })
        .catch((error) => {
            toast.error(error.error);
            isLoading.value = false;
        });
    };
</script>

<template>
    <GuestLayout>
        <header class="text-center w-100">
            <h1>Forgot password</h1>
        </header>

        <div class="form-container">

            <form @submit.prevent="onSubmit" class="p-0 mt-5">
                <section>
                    <label for="emailInput" class="form-label">Write your e-mail</label>
                    <input type="email" v-model="email" v-bind="emailAttrs" class="form-control" id="emailInput">
                </section>

                <section class="mt-5">
                    <button v-if="!isLoading" type="submit">Reset password</button>
                    <button v-else class="submit" type="button" disabled>
                        <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                        Under process...
                    </button>
                </section>
            </form>
            
        </div>

        <footer>
            <div class="row">
                <div class="col text-center">
                    <router-link :to="{name: 'Login'}">Back to log in</router-link>
                </div>
            </div>
        </footer>
        
    </GuestLayout>
</template>

<style scoped lang="scss">
@use '../../assets/auth';

</style>