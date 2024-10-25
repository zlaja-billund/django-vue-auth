<script setup>
    import { ref, onMounted } from 'vue';
    import { toTypedSchema } from '@vee-validate/yup';
    import { useForm } from 'vee-validate';
    import * as yup from 'yup';
    import { useToast } from "vue-toastification";
  
    import GuestLayout from '@/layouts/GuestLayout.vue';
    import { useAuthStore } from '../../stores';

    const { errors, defineField } = useForm({
        validationSchema: toTypedSchema(
            yup.object({
            email: yup.string().email().required(),
            password: yup.string().min(6).required(),
            }),
        ),
        });

    const [email, emailAttrs] = defineField('email', {
        validateOnModelUpdate: false,
    });

    const [password, passwordAttrs] = defineField('password', {
        validateOnModelUpdate: false,
    });

    const isHidden = ref(false)

    const onSubmit = () => {
        isHidden.value = true;

        const authStore = useAuthStore();
        const toast = useToast();
        
        setTimeout(() => {
            isHidden.value = false;
            authStore.login(email.value, password.value).catch((error) => {
                toast.error("Authentication failed: " + error.detail);
            });
        },1000);              
    }
</script>

<template>    
    <GuestLayout>

        <header class="text-center w-100">
            <h1>Log in</h1>
        </header>

        <div class="form-container">

            <form @submit.prevent="onSubmit" class="p-0 mt-5">
                <section>
                    <label for="emailInput" class="form-label">Write your email</label>
                    <input type="text" v-model="email" v-bind="emailAttrs" class="form-control" id="emailInput" required>
                    <div class="validation-errors">
                        {{ errors.email }}
                    </div>
                </section>

                <section class="mt-4">
                    <label for="passwordInput" class="form-label">Write your password</label>
                    <input type="password" v-model="password" v-bind="passwordAttrs" class="form-control" id="passwordInput">
                    <div class="validation-errors">
                        {{ errors.password }}
                    </div>
                </section>

                <section class="mt-5">
                    <button v-if="!isHidden" type="submit">Log in</button>
                    <button v-else class="submit" type="button" disabled>
                        <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                        Indlæser...
                    </button>
                </section>
            </form>
        </div>

        <footer>
            <div class="row">
                <div class="col text-end me-3">
                    <!--<router-link :to="{ name: 'ForgotPassword' }">Forgot your password ?</router-link>-->
                </div>
                <div class="col text-start ms-3">
                    <!--<router-link :to="{ name: 'CreateNewUser'}">Create new account</router-link>-->
                </div>
            </div>
        </footer>        
    </GuestLayout>
</template>

<style scoped lang="scss">
@use '../../assets/auth.scss';

</style>