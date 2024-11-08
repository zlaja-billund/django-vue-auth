import { defineStore } from "pinia";
import router from '../router';
import { fetchWrapper } from "../helpers";

const baseUrl = import.meta.env.VITE_API_URL + "/api";

export const useAuthStore = defineStore({
    id: 'auth',
    state: () => ({
        accessKey: JSON.parse(localStorage.getItem('access_key')),
        returnUrl: null,
    }),
    actions: {
        async login(email, password) {

            const data = {
                email: email,
                password: password
            };
        
            //Get login token from 
            const responseData = await fetchWrapper.post(baseUrl + '/token/', data);
            
            if(responseData)
            {
                let accessKey = responseData.access;
                let refreshKey = responseData.refresh;

                this.accessKey = accessKey;

                // Store user details and JWT in localstorage to keep user logged in between page refreshes
                localStorage.setItem('access_key', JSON.stringify(accessKey));
                localStorage.setItem('refresh_key', JSON.stringify(refreshKey))

                // Redirect to previous url or default to home page
                return router.push('/');
            }

            return router.push('/login');
        },
        async create(email, firstName, lastname, password, password2){

            if(!email && !firstName && !lastname && !password && !password2)
            {
                return false;
            }

            const data = {
                email: email,
                first_name: firstName,
                last_name: lastname,
                password: password,
                password2: password2
            };
            
            return await fetchWrapper.post(baseUrl + '/user/register', data);
        },
        async requestResetPassword(email) {
            
            if(email === null)
            {
                return "Missing email param";
            }

            const data = {
                email: email
            };

            return await fetchWrapper.post(baseUrl + '/user/request-reset-password', data);

        },
        async resetPassword(token, newPassword, confirmPassword)
        {
            if(token === 'undefined' || newPassword === 'undefined' || confirmPassword === 'undefined')
            {
                return 'Params missing';
            }

            const data = {
                new_password: newPassword,
                confirm_password: confirmPassword,
                token: token
            };

            return await fetchWrapper.post(baseUrl + '/user/reset-password', data );
        },
        async confirmEmail(userId, token){

            const data = {
                UserId: userId,
                ConfirmToken: token,
            };

            const response = await fetchWrapper.post(baseUrl + '/email/confirm', data).then((response) => {
                return true;
            }).catch((error) => {
                return false;
            });
            
            return response;
        },
        async resendConfirmEmail(userId){
            const data = {
                userId: userId,
            };
            
            const response = await fetchWrapper.post(baseUrl + '/email/resend', data).then((response) => {
                return true;
            }).catch((error) => {
                return false;
            });

            return response;
            
        },
        logout() {
            localStorage.removeItem('access_key');
            localStorage.removeItem('refresh_key');
            location.reload();
        }
    }
});