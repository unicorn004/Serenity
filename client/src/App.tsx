import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/navbar";
import Footer from "./components/footer";
import Home from "./pages/home/page";
import CrisisPage from "./pages/crisis/page";
import BookingPage from "./pages/booking/page";
import DashboardPage from "./pages/dashboard/page";
import ChatPage from "./pages/chat/page";
import EmotionsPage from "./pages/emotions/page";
import GroupsPage from "./pages/groups/page";
import LoginPage from "./pages/login/page";
import SignupPage from "./pages/signup/page";
import MindfulnessPage from "./pages/mindfulness/page";
import ProtectRoute from "./ProtectedRoute.tsx";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

export default function App() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      {/* Routes */}
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/" element={<Home />} />

        {/* Protected Routes */}
        <Route element={<ProtectRoute />}>
          <Route path="/crisis" element={<CrisisPage />} />
          <Route path="/booking" element={<BookingPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/emotions" element={<EmotionsPage />} />
          <Route path="/groups" element={<GroupsPage />} />
          <Route path="/mindfulness" element={<MindfulnessPage />} />
          <Route path="/logout" element={<Logout />} />
        </Route>
      </Routes>
      <Footer />
    </div>
  );
}