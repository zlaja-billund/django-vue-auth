<script setup>
    import { ref } from 'vue';
    import { toTypedSchema } from '@vee-validate/yup';
    import { useRouter } from 'vue-router';
    import { useForm } from 'vee-validate';
    import * as yup from 'yup';
    import { useToast } from "vue-toastification";

    import GuestLayout from '../../layouts/GuestLayout.vue';
    import { useAuthStore } from '../../stores';
import { errorMessages } from 'vue/compiler-sfc';

    const router = useRouter();


    const { errors, defineField} = useForm({
        validationSchema: toTypedSchema(
            yup.object({
                email: yup.string().email().required().label("E-mail"),
                firstName: yup.string().required().label('Firstname'),
                lastname: yup.string().required().label('lastname'),
                password: yup.string().length(8).required().label('password'),
                passwordConfirmation: yup.string().required().label('confirm password').oneOf([yup.ref('password')], 'Passwords do not match')
            }),
        ),
    });


    const [email, emailAttrs] = defineField('email', {
        validateOnModelUpdate: false,
    });

    const [firstName, firstNameAttrs] = defineField('firstName', {
        validateOnModelUpdate: false,
    });

    const [lastname, lastnameAttrs] = defineField('lastname', {
        validateOnModelUpdate: false,
    });

    const [password, passwordAttrs] = defineField('password', {
        validateOnModelUpdate: false,
    });

    const [passwordConfirmation, passwordConfirmationAttrs] = defineField('passwordConfirmation',{
        validateOnModelUpdate: false,
    });

    const isLoading = ref(false);

    const onSubmit = () => {
        isLoading.value = true;

        const authStore = useAuthStore();
        const toast = useToast();

        setTimeout(() => {
            
            authStore.create(email.value, firstName.value, lastname.value, password.value, passwordConfirmation.value)
            .then((response) => {
                toast.success("Your account is created successfully");

                setTimeout(() => { router.push({name: 'Login'});}, 5000);
                
            }).catch((errors) => {

                let errorsMessages = []

                for(const errorKey of Object.keys(errors)) {
                    const errorType = errors[errorKey]
                    errorType.forEach(item => errorsMessages.push(errorKey + ": " + item));
                }

                toast.error(errorsMessages.join('\n'));
            });

            isLoading.value = false;

        }, 3000);

        
    };



</script>

<template>
    <GuestLayout>
        <header class="text-center w-100">
            <h1>Join us today</h1>
        </header>

        <div class="form-container">
            <form @submit.prevent="onSubmit" class="p-0 mt-5">
                <section>
                    <label for="emailInput" class="form-label">What is your email</label>
                    <input type="email" v-model="email" v-bind="emailAttrs" class="form-control" id="emailInput" required>
                    <div class="validation-errors">
                        {{ errors.email }}
                    </div>
                </section>
                
                <section class="mt-4">
                    <label for="firstNameInput" class="form-label">Your firstname</label>
                    <input type="text" v-model="firstName" v-bind="firstNameAttrs" class="form-control" id="firstNameInput" required>
                    <div class="validation-errors">
                        {{ errors.firstName }}
                    </div>
                </section>

                <section class="mt-4">
                    <label for="lastnameInput" class="form-label">Your lastname</label>
                    <input type="text" v-model="lastname" v-bind="lastnameAttrs" class="form-control" id="lastnameInput" required>
                    <div class="validation-errors">
                        {{ errors.lastname }}
                    </div>
                </section>
                
                <section class="mt-4">
                   <label for="passwordInput" class="form-label">Enter your password</label>
                    <input type="password" v-model="password" v-bind="passwordAttrs" class="form-control" id="passwordInput" required>
                    <div id="passwordHelp" class="form-text helper-text">Your password must be at least 8 characters long and include at least uppercase letter, lowercase letter, number and special character.</div>
                    <div class="validation-errors">
                        {{ errors.password }}
                    </div>
                </section>
                
                <section class="mt-4">
                   <label for="passwordConfirmationInput" class="form-label">Confirm password</label>
                    <input type="password" v-model="passwordConfirmation" v-bind="passwordConfirmationAttrs"  class="form-control" id="passwordConfirmationInput" required>
                    <div class="validation-errors">
                        {{ errors.passwordConfirmation }}
                    </div>
                </section>

                <section class="mt-5">
                    <button v-if="!isLoading" type="submit">Create free account</button>
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
                    <router-link :to="{ name: 'Login' }">I already have an account</router-link>
                </div>
            </div>
        </footer>
        
    </GuestLayout>
</template>

<style scoped lang="scss">
@use '../../assets/auth';

</style>