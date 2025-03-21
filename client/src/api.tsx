// import axios, { AxiosRequestConfig } from "axios";
// import { ACCESS_TOKEN } from "./constants";

// const api = axios.create({
//   baseURL: import.meta.env.VITE_API_URL as string,  // Ensure type safety
// });

// api.interceptors.request.use(
//   (config: AxiosRequestConfig) => {
//     const token = localStorage.getItem(ACCESS_TOKEN);
//     if (token) {
//       config.headers = config.headers || {};  // Ensure headers exist
//       config.headers.Authorization = `Bearer ${token}`;
//     }
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// export default api;


import axios from "axios"

import { ACCESS_TOKEN } from "./constants.tsx"

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api'
 });

api.interceptors.request.use(
   (config)=>{
       const token = localStorage.getItem(ACCESS_TOKEN);
       if(token){
           config.headers.Authorization = `Bearer ${token}`
       }
       return config
   } , 
   (error)=>{
       return Promise.reject(error)
   }
)

export default api