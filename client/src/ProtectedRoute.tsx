import React, { useState, useEffect } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants.tsx";
import { Navigate, Outlet } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "./api.tsx";

function ProtectRoute() {
    const [isAuth, setIsAuth] = useState(null);

    const getAccessbyRefreshToken = async () => {
        const refresh_token = localStorage.getItem(REFRESH_TOKEN);
        try {
            const res = await api.post("/api/user/token/refresh/", { refresh: refresh_token });
            if (res.status === 200) {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                setIsAuth(true);
            } else {
                setIsAuth(false);
            }
        } catch (error) {
            setIsAuth(false);
        }
    };

    useEffect(() => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (!token) {
            setIsAuth(false);
        } else {
            const decode = jwtDecode(token);
            if (decode.exp < Date.now() / 1000) {
                getAccessbyRefreshToken();
            } else {
                setIsAuth(true);
            }
        }
    }, []);

    if (isAuth === null) return <>Loading...</>;
    if (isAuth === false) return <Navigate to="/login" />;
    
    return <Outlet />; // Renders child routes
}

export default ProtectRoute;
