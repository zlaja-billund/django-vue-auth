import { defineStore } from 'pinia';
import { fetchWrapper } from '@/helpers';

const baseUrl = import.meta.env.VITE_API_URL + "/User";

export const useUserStore = defineStore({
    id: "user",
    state: () => ({
        user: {}
    }),
    actions: {
        async getCurrentUser(){

            const response = await fetchWrapper.get(baseUrl +'/current');

            this.user = { };
        }
    }
});