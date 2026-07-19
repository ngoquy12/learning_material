import { Routes, Route } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import DashboardPage from "../modules/dashboard/pages/DashboardPage";
import CourseListPage from "../modules/courses/pages/CourseListPage";
import CourseDetailPage from "../modules/courses/pages/CourseDetailPage";
import ProgramListPage from "../modules/programs/pages/ProgramListPage";
import MajorListPage from "../modules/majors/pages/MajorListPage";
import SemesterListPage from "../modules/semesters/pages/SemesterListPage";
import PipelineMonitorPage from "../modules/pipeline/pages/PipelineMonitorPage";
import LessonArtifactViewerPage from "../modules/lessons/pages/LessonArtifactViewerPage";
import SessionArtifactViewerPage from "../modules/sessions/pages/SessionArtifactViewerPage";
import SettingsPage from "../modules/settings/pages/SettingsPage";
import Login from "../modules/auth/Login";
import ResetPassword from "../modules/auth/ResetPassword";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/reset" element={<ResetPassword />} />

      <Route path="/" element={<MainLayout />}>
        <Route index element={<DashboardPage />} />
        <Route path="programs" element={<ProgramListPage />} />
        <Route path="majors" element={<MajorListPage />} />
        <Route path="semesters" element={<SemesterListPage />} />
        <Route path="courses" element={<CourseListPage />} />
        <Route path="courses/:courseId" element={<CourseDetailPage />} />
        <Route path="courses/:courseId/lessons/:lessonId/viewer" element={<LessonArtifactViewerPage />} />
        <Route path="courses/:courseId/sessions/:sessionId/viewer" element={<SessionArtifactViewerPage />} />
        <Route path="pipeline" element={<PipelineMonitorPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>

      {/* Route lỗi Not Found */}
      <Route
        path="*"
        element={
          <div className="flex flex-col items-center justify-center min-h-screen">
            <h1 className="text-4xl font-bold text-gray-800">404</h1>
            <p className="text-gray-500 mt-2">Trang không tồn tại</p>
          </div>
        }
      />
    </Routes>
  );
}

