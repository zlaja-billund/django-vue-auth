<script setup>
    import { ref } from 'vue';
    import { toTypedSchema } from '@vee-validate/yup';
    import { useRouter, useRoute } from 'vue-router';
    import { useForm } from 'vee-validate';
    import * as yup from 'yup';
    import { useToast } from "vue-toastification";

    import GuestLayout from '../../layouts/GuestLayout.vue';
    import { useAuthStore } from '../../stores';

    const router = useRouter();
    const route = useRoute();

    const token = route.params.token;

    // Custom regex for password validation
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    const { errors, defineField} = useForm({
        validationSchema: toTypedSchema(
            yup.object({
                newPassword: yup.string().matches(passwordRegex, 'Your password does not meet the requirements').required().label('password'),
                confirmPassword: yup.string().label('Password confirmation').required().oneOf([yup.ref('password')], 'Your password does not match')
            }),
        ),
    });

    const [newPassword, newPasswordAttrs] = defineField('newPassword', {
        validateOnModelUpdate: false,
    });

    const [confirmPassword, confirmPasswordAttrs] = defineField('confirmPassword',{
        validateOnModelUpdate: false,
    });

    const isLoading = ref(false);

    const onSubmit = () => {
        isLoading.value = true;

        const authStore = useAuthStore();
        const toast = useToast();

        setTimeout(() => {
            
            authStore.resetPassword(token, newPassword.value, confirmPassword.value)
            .then((response) => {
                toast.success("Your password has now been changed. You will be redirected shortly.");

                setTimeout(() => { router.push({name: 'Login'});}, 3000);
                
            }).catch((error) => {
                toast.error(error.error);
            });

            isLoading.value = false;

        }, 3000);

        
    };



</script>

<template>
    <GuestLayout>
        <header class="text-center w-100">
            <h1>Reset your password</h1>
        </header>

        <div class="form-container">
            <form @submit.prevent="onSubmit" class="p-0 mt-5">
                
                <section class="mt-4">
                   <label for="newPasswordInput" class="form-label">Write a new password</label>
                    <input type="password" v-model="newPassword" v-bind="newPasswordAttrs" class="form-control" id="newPasswordInput" required>
                    <div id="passwordHelp" class="form-text helper-text">Your password must be at least 8 characters long and include at least uppercase letter, lowercase letter, number and special character.</div>
                    <div class="validation-errors">
                        {{ errors.newPassword }}
                    </div>
                </section>
                
                <section class="mt-4">
                   <label for="confirmPasswordInput" class="form-label">Confirm password</label>
                    <input type="password" v-model="confirmPassword" v-bind="confirmPasswordAttrs"  class="form-control" id="confirmPasswordInput" required>
                    <div class="validation-errors">
                        {{ errors.confirmPassword }}
                    </div>
                </section>

                <section class="mt-5">
                    <button v-if="!isLoading" type="submit">Save</button>
                    <button v-else class="submit" type="button" disabled>
                        <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                        Processing ...
                    </button>
                </section>
            </form>
            
        </div>

        <footer>
            <div class="row">
                <div class="col text-center me-3">
                    <router-link :to="{ name: 'Login' }">I already have an account</router-link>
                </div>
            </div>
        </footer>
        
    </GuestLayout>
</template>

<style scoped lang="scss">
@use '../../assets/auth';

</style>