import { Breadcrumb } from "antd";
import { Link, useLocation, useParams } from "react-router-dom";
import {
  Home,
  Layers,
  FolderTree,
  BookMarked,
  BookOpen,
  Activity,
  Settings as SettingsIcon,
  FileText,
} from "lucide-react";
import React from "react";

export const AppBreadcrumb: React.FC = () => {
  const location = useLocation();
  const params = useParams();

  const pathname = location.pathname;

  // Don't render breadcrumbs on dashboard home page
  if (pathname === "/") {
    return null;
  }

  const renderBreadcrumbTitle = (
    icon: React.ReactNode,
    text: string,
    to?: string,
    isActive?: boolean
  ) => {
    const iconElement = React.cloneElement(icon as React.ReactElement, {
      size: 14,
      style: {
        display: "inline-block",
        flexShrink: 0,
        verticalAlign: "middle",
        margin: 0,
      },
    });

    const labelElement = (
      <span
        style={{
          lineHeight: "1.2",
          display: "inline-block",
          verticalAlign: "middle",
        }}
      >
        {text}
      </span>
    );

    const flexStyle: React.CSSProperties = {
      display: "inline-flex",
      flexDirection: "row",
      alignItems: "center",
      gap: "6px",
      lineHeight: "1",
      whiteSpace: "nowrap",
      verticalAlign: "middle",
    };

    if (to && !isActive) {
      return (
        <Link
          to={to}
          style={flexStyle}
          className="text-slate-600 hover:text-teal-600 transition-colors"
        >
          {iconElement}
          {labelElement}
        </Link>
      );
    }

    return (
      <span
        style={flexStyle}
        className={isActive ? "font-bold text-slate-800" : "text-slate-600"}
      >
        {iconElement}
        {labelElement}
      </span>
    );
  };

  const items: { key: string; title: React.ReactNode }[] = [
    {
      key: "home",
      title: renderBreadcrumbTitle(<Home />, "Trang chủ", "/"),
    },
  ];

  // Pattern matching for parent -> child -> grandchild paths
  if (pathname.startsWith("/programs")) {
    items.push({
      key: "programs",
      title: renderBreadcrumbTitle(<Layers />, "Hệ đào tạo", "/programs"),
    });
    if (params.programId) {
      items.push({
        key: "program-detail",
        title: renderBreadcrumbTitle(
          <Layers />,
          `Chi tiết Hệ đào tạo #${params.programId}`,
          undefined,
          true
        ),
      });
    }
  } else if (pathname.startsWith("/majors")) {
    items.push({
      key: "programs",
      title: renderBreadcrumbTitle(<Layers />, "Hệ đào tạo", "/programs"),
    });
    items.push({
      key: "majors",
      title: renderBreadcrumbTitle(<FolderTree />, "Chuyên ngành", "/majors"),
    });
    if (params.majorId) {
      items.push({
        key: "major-detail",
        title: renderBreadcrumbTitle(
          <FolderTree />,
          `Chi tiết Chuyên ngành #${params.majorId}`,
          undefined,
          true
        ),
      });
    }
  } else if (pathname.startsWith("/semesters")) {
    items.push({
      key: "majors",
      title: renderBreadcrumbTitle(<FolderTree />, "Chuyên ngành", "/majors"),
    });
    items.push({
      key: "semesters",
      title: renderBreadcrumbTitle(<BookMarked />, "Kỳ học", "/semesters"),
    });
    if (params.semesterId) {
      items.push({
        key: "semester-detail",
        title: renderBreadcrumbTitle(
          <BookMarked />,
          `Chi tiết Kỳ học #${params.semesterId}`,
          undefined,
          true
        ),
      });
    }
  } else if (pathname.startsWith("/courses")) {
    items.push({
      key: "semesters",
      title: renderBreadcrumbTitle(<BookMarked />, "Kỳ học", "/semesters"),
    });
    items.push({
      key: "courses",
      title: renderBreadcrumbTitle(<BookOpen />, "Môn học & Bài đọc", "/courses"),
    });
    if (params.courseId) {
      if (pathname.includes("/lessons/") && pathname.includes("/viewer")) {
        items.push({
          key: "course-detail",
          title: renderBreadcrumbTitle(
            <BookOpen />,
            `Chi tiết môn học #${params.courseId}`,
            `/courses/${params.courseId}`
          ),
        });
        items.push({
          key: "lesson-viewer",
          title: renderBreadcrumbTitle(
            <FileText />,
            `Nội dung bài học #${params.lessonId}`,
            undefined,
            true
          ),
        });
      } else if (pathname.includes("/sessions/") && pathname.includes("/viewer")) {
        items.push({
          key: "course-detail",
          title: renderBreadcrumbTitle(
            <BookOpen />,
            `Chi tiết môn học #${params.courseId}`,
            `/courses/${params.courseId}`
          ),
        });
        items.push({
          key: "session-viewer",
          title: renderBreadcrumbTitle(
            <FileText />,
            `Nội dung phiên học #${params.sessionId}`,
            undefined,
            true
          ),
        });
      } else {
        items.push({
          key: "course-detail",
          title: renderBreadcrumbTitle(
            <BookOpen />,
            `Chi tiết môn học #${params.courseId}`,
            undefined,
            true
          ),
        });
      }
    }
  } else if (pathname.startsWith("/pipeline")) {
    items.push({
      key: "pipeline",
      title: renderBreadcrumbTitle(
        <Activity className="text-teal-600" />,
        "Theo dõi tiến trình",
        undefined,
        true
      ),
    });
  } else if (pathname.startsWith("/settings")) {
    items.push({
      key: "settings",
      title: renderBreadcrumbTitle(
        <SettingsIcon className="text-teal-600" />,
        "Cài đặt hệ thống",
        undefined,
        true
      ),
    });
  }

  return (
    <div className="bg-white px-4 py-2.5 rounded-xl border border-slate-200/80 shadow-sm mb-4">
      <Breadcrumb
        items={items}
        className="text-xs font-medium text-slate-600 [&_ol]:!flex [&_ol]:!items-center [&_ol]:!flex-row [&_li]:!inline-flex [&_li]:!items-center [&_.ant-breadcrumb-link]:!inline-flex [&_.ant-breadcrumb-link]:!items-center [&_.ant-breadcrumb-separator]:!inline-flex [&_.ant-breadcrumb-separator]:!items-center"
      />
    </div>
  );
};
