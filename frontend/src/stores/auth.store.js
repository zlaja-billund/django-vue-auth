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
        async login(username, password) {

            const data = {
                username: username,
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
        async create(email, firstName, surname, password){

            if(!email && !firstName && !surname && !password)
            {
                return false;
            }

            const data = {
                email: email,
                firstName: firstName,
                surname: surname,
                password: password
            };
            
            return await fetchWrapper.post(baseUrl + '/register', data);
        },
        async requestResetPassword(email) {
            
            if(email === null)
            {
                return "Missing email param";
            }

            const data = {
                email: email
            };

            return await fetchWrapper.post(baseUrl + '/forgot-password', data);

        },
        async resetPassword(userid, token, password)
        {
            if(userid === 'undefined' || token === 'undefined' || password === 'undefined')
            {
                return 'Params missing';
            }

            const data = {
                userId: userid,
                password: password,
                token: token
            };

            return await fetchWrapper.post(baseUrl + '/reset-password', data );
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