import { useState, useMemo } from "react";
import { Layout, Menu, Dropdown, Avatar, message, theme } from "antd";
import { Link, Outlet, useLocation, useNavigate } from "react-router-dom";
import {
  BookOpen,
  LayoutDashboard,
  Settings,
  Layers,
  FolderTree,
  BookMarked,
  Activity,
  ChevronLeft,
  ChevronRight,
  User,
  LogOut,
  ChevronDown,
} from "lucide-react";

const { Header, Content, Footer, Sider } = Layout;

export default function MainLayout() {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);

  // Retrieve user mock login info or fallback to default
  const userLogined = useMemo(() => {
    const raw = localStorage.getItem("userLogined");
    if (raw) {
      try {
        const parsed = JSON.parse(raw);
        if (parsed) return parsed;
      } catch (e) {
        console.log(e);
      }
    }
    return {
      firstName: "Giảng viên",
      lastName: "Rikkei",
      role: "Quản trị viên",
      position: "Giảng viên công nghệ",
    };
  }, [location.pathname]);

  const handleLogout = () => {
    localStorage.removeItem("userLogined");
    message.success("Đăng xuất thành công!");
    navigate("/login");
  };

  const menuItems = [
    {
      key: "/",
      icon: <LayoutDashboard size={18} />,
      label: <Link to="/">Dashboard</Link>,
    },
    {
      key: "/programs",
      icon: <Layers size={18} />,
      label: <Link to="/programs">Hệ đào tạo</Link>,
    },
    {
      key: "/majors",
      icon: <FolderTree size={18} />,
      label: <Link to="/majors">Chuyên ngành</Link>,
    },
    {
      key: "/semesters",
      icon: <BookMarked size={18} />,
      label: <Link to="/semesters">Kỳ học</Link>,
    },
    {
      key: "/courses",
      icon: <BookOpen size={18} />,
      label: <Link to="/courses">Môn học</Link>,
    },
    {
      key: "/pipeline",
      icon: <Activity size={18} />,
      label: <Link to="/pipeline">Pipeline Monitor</Link>,
    },
    {
      key: "/settings",
      icon: <Settings size={18} />,
      label: <Link to="/settings">Cài đặt hệ thống</Link>,
    },
  ];

  const userDropdownItems = [
    {
      key: "profile",
      label: (
        <span className="flex items-center gap-2 px-1">
          <User size={16} />
          <span>Thông tin cá nhân</span>
        </span>
      ),
    },
    {
      key: "settings",
      label: (
        <span className="flex items-center gap-2 px-1">
          <Settings size={16} />
          <span>Cài đặt cá nhân</span>
        </span>
      ),
      onClick: () => navigate("/settings"),
    },
    { type: "divider" as const },
    {
      key: "logout",
      label: (
        <span className="flex items-center gap-2 px-1 text-red-500 hover:text-red-600">
          <LogOut size={16} />
          <span>Đăng xuất</span>
        </span>
      ),
      onClick: handleLogout,
    },
  ];

  return (
    <Layout style={{ height: "100vh", overflow: "hidden" }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
        theme="light"
        width={256}
        collapsedWidth={80}
        className="shadow-sm border-r border-slate-200/80"
      >
        <div className="h-16 flex items-center justify-center border-b border-slate-100 px-4">
          <Link to="/" className="flex items-center justify-center">
            <img
              src="/logo-main.png"
              alt="Rikkei Logo"
              className="h-10 w-auto object-contain transition-all"
            />
          </Link>
        </div>
        <Menu
          theme="light"
          mode="inline"
          selectedKeys={[
            location.pathname === "/"
              ? "/"
              : menuItems.find(
                  (item) =>
                    item.key !== "/" && location.pathname.startsWith(item.key),
                )?.key || location.pathname,
          ]}
          items={menuItems}
          className="border-r-0 mt-4 px-2"
          style={{
            // Custom premium selection highlights
            fontSize: "14px",
            fontWeight: 500,
          }}
        />
      </Sider>

      <Layout
        style={{
          height: "100vh",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Header
          style={{ padding: "0 24px", background: colorBgContainer }}
          className="shadow-sm border-b border-slate-100 flex items-center justify-between sticky top-0 z-30 h-16"
        >
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <button
                onClick={() => navigate(-1)}
                className="cursor-pointer text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 bg-slate-50 hover:bg-slate-100 rounded-full p-2 transition-all"
                title="Quay lại"
              >
                <ChevronLeft size={18} />
              </button>
              <button
                onClick={() => navigate(1)}
                className="cursor-pointer text-slate-400 hover:text-slate-700 dark:hover:text-slate-300 bg-slate-50 hover:bg-slate-100 rounded-full p-2 transition-all"
                title="Chuyển tiếp"
              >
                <ChevronRight size={18} />
              </button>
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* User Profile Info Dropdown */}
            <Dropdown menu={{ items: userDropdownItems }} trigger={["click"]}>
              <div className="flex items-center gap-3 cursor-pointer p-1.5 hover:bg-slate-50 rounded-lg transition-colors">
                <Avatar
                  size={36}
                  style={{ backgroundColor: "#1DBFAF" }}
                  icon={<User size={18} />}
                />
                <div className="hidden sm:flex flex-col items-start leading-tight">
                  <span className="text-sm font-semibold text-slate-700 dark:text-slate-200">
                    {userLogined?.name ||
                      `${userLogined?.firstName || ""} ${userLogined?.lastName || ""}`.trim() ||
                      "Giảng viên Rikkei"}
                  </span>
                  <span className="text-[11px] text-slate-400 font-medium">
                    {userLogined?.position?.positionName ||
                      userLogined?.position ||
                      userLogined?.role?.roleName ||
                      userLogined?.role ||
                      "Quản trị viên"}
                  </span>
                </div>
                <ChevronDown size={14} className="text-slate-400" />
              </div>
            </Dropdown>
          </div>
        </Header>

        <Content
          style={{
            flex: 1,
            overflowY: "auto",
            background: colorBgContainer,
          }}
        >
          <div
            style={{
              padding: 24,
              minHeight: "calc(100vh - 128px)",
            }}
            className="border-t border-slate-100"
          >
            <Outlet />
          </div>
          <Footer
            style={{
              textAlign: "center",
              color: "#94a3b8",
              padding: "16px 24px",
            }}
          >
            Elearning Content Factory ©{new Date().getFullYear()} Created by
            Rikkei Education
          </Footer>
        </Content>
      </Layout>
    </Layout>
  );
}
