import { useState } from "react";
import { Layout, Menu, Dropdown, Avatar, message, theme, Badge, Popover, Tag } from "antd";
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
  Bell,
  Search,
  Sparkles,
  Cpu,
  CheckCircle2,
  Server,
} from "lucide-react";
import { AppBreadcrumb } from "../components/AppBreadcrumb";

const { Header, Content, Footer, Sider } = Layout;

export default function MainLayout() {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const location = useLocation();
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem("userLogined");
    message.success("Đăng xuất thành công!");
    navigate("/login");
  };

  const menuItems = [
    {
      key: "/",
      icon: <LayoutDashboard size={18} />,
      label: <Link to="/">Bảng điều khiển</Link>,
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
      label: <Link to="/courses">Môn học & Bài đọc</Link>,
    },
    {
      key: "/pipeline",
      icon: <Activity size={18} />,
      label: (
        <Link to="/pipeline" className="flex items-center justify-between">
          <span>Theo dõi tiến trình</span>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
        </Link>
      ),
    },
    {
      key: "/settings",
      icon: <Settings size={18} />,
      label: <Link to="/settings">Cài đặt hệ thống</Link>,
    },
  ];

  const notifications = [
    { id: 1, title: "Tiến trình HTML/GSAP", time: "2 phút trước", status: "success", text: "Bài đọc Lesson 06 đã render thành công HTML/GSAP." },
    { id: 2, title: "Kiểm tra bài trước", time: "15 phút trước", status: "warning", text: "Phát hiện 1 bài chưa đủ điều kiện tiên quyết trong Session 02." },
    { id: 3, title: "Bộ nhớ đệm", time: "1 giờ trước", status: "info", text: "Đã tối ưu hóa 320 KB cache vector embedding." },
  ];

  const notificationContent = (
    <div className="w-80 space-y-3 p-1">
      <div className="flex justify-between items-center pb-2 border-b border-slate-100">
        <span className="font-semibold text-slate-800 text-sm">Thông báo hệ thống</span>
        <Tag color="cyan" className="m-0 text-xs">Cập nhật tự động</Tag>
      </div>
      <div className="space-y-2">
        {notifications.map((n) => (
          <div key={n.id} className="p-2.5 rounded-lg bg-slate-50 hover:bg-slate-100/80 transition-colors text-xs space-y-1">
            <div className="flex justify-between items-center font-medium text-slate-700">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 size={13} className="text-teal-500" />
                {n.title}
              </span>
              <span className="text-[10px] text-slate-400">{n.time}</span>
            </div>
            <p className="text-slate-500 m-0 leading-relaxed">{n.text}</p>
          </div>
        ))}
      </div>
      <div className="pt-2 border-t border-slate-100 text-center">
        <button
          onClick={() => navigate("/pipeline")}
          className="text-xs text-teal-600 font-medium hover:underline cursor-pointer"
        >
          Xem tất cả trong Tiến trình →
        </button>
      </div>
    </div>
  );

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
    <Layout style={{ height: "100vh", overflow: "hidden" }} className="bg-slate-50">
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
        theme="light"
        width={260}
        collapsedWidth={80}
        className="shadow-sm border-r border-slate-200/80 flex flex-col justify-between"
      >
        <div>
          {/* Logo & Agent Badge Header */}
          <div className="h-16 flex items-center justify-between px-4 border-b border-slate-100">
            <Link to="/" className="flex items-center gap-2.5 overflow-hidden">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-teal-500 to-emerald-400 flex items-center justify-center text-white shadow-md shadow-teal-500/20 shrink-0">
                <Sparkles size={20} />
              </div>
              {!collapsed && (
                <div className="flex flex-col leading-tight">
                  <span className="font-bold text-slate-800 text-sm tracking-tight">Rikkei LMS Agent</span>
                  <span className="text-[10px] text-teal-600 font-semibold tracking-wider uppercase">Hệ Thống Tự Động</span>
                </div>
              )}
            </Link>
          </div>

          {/* Navigation Menu */}
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
            className="border-r-0 mt-3 px-2 text-slate-600 font-medium"
          />
        </div>

        {/* Sidebar Footer System Health Widget */}
        {!collapsed && (
          <div className="m-3 p-3 rounded-xl bg-gradient-to-br from-teal-50 to-emerald-50 border border-teal-200/80 text-slate-800 shadow-sm space-y-2.5">
            <div className="flex items-center justify-between text-xs">
              <span className="flex items-center gap-1.5 text-slate-700 font-semibold">
                <Cpu size={14} className="text-teal-600" /> Trạng thái Worker
              </span>
              <Tag color="emerald" className="m-0 text-[10px] px-1.5 py-0 border-none font-bold">SẴN SÀNG</Tag>
            </div>
            <div className="space-y-1">
              <div className="flex justify-between text-[11px] text-slate-600">
                <span>Bộ nhớ đệm (Cache)</span>
                <span className="text-teal-700 font-bold">94.8% Trùng khớp</span>
              </div>
              <div className="w-full h-1.5 bg-teal-200/60 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-teal-500 to-emerald-500 rounded-full w-[94.8%]"></div>
              </div>
            </div>
            <div className="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-teal-200/60">
              <span className="flex items-center gap-1"><Server size={11} className="text-teal-600" /> Mô hình AI</span>
              <span className="text-emerald-700 font-semibold">Đang kết nối</span>
            </div>
          </div>
        )}
      </Sider>

      <Layout
        style={{
          height: "100vh",
          overflow: "hidden",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* Modern Top Header */}
        <Header
          style={{ padding: "0 24px", background: colorBgContainer }}
          className="shadow-sm border-b border-slate-200/80 flex items-center justify-between sticky top-0 z-30 h-16"
        >
          {/* Left section: navigation arrows & live agent pills */}
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-1.5">
              <button
                onClick={() => navigate(-1)}
                className="cursor-pointer text-slate-500 hover:text-slate-800 bg-slate-100 hover:bg-slate-200/80 rounded-lg p-2 transition-all"
                title="Quay lại"
              >
                <ChevronLeft size={16} />
              </button>
              <button
                onClick={() => navigate(1)}
                className="cursor-pointer text-slate-500 hover:text-slate-800 bg-slate-100 hover:bg-slate-200/80 rounded-lg p-2 transition-all"
                title="Chuyển tiếp"
              >
                <ChevronRight size={16} />
              </button>
            </div>
          </div>

          {/* Right section: Search bar, Notifications, User profile */}
          <div className="flex items-center gap-3">
            {/* Quick Search Input */}
            <div className="relative hidden sm:block w-48 lg:w-64">
              <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                placeholder="Tìm kiếm môn học, pipeline..."
                className="w-full pl-9 pr-3 py-1.5 bg-slate-100 hover:bg-slate-200/60 focus:bg-white focus:ring-2 focus:ring-teal-500/30 focus:border-teal-500 border border-transparent rounded-xl text-xs transition-all outline-none"
              />
            </div>

            {/* Notifications Popover */}
            <Popover content={notificationContent} trigger="click" placement="bottomRight">
              <button className="relative cursor-pointer p-2 rounded-xl text-slate-600 hover:bg-slate-100 transition-colors">
                <Badge dot color="#1DBFAF">
                  <Bell size={18} />
                </Badge>
              </button>
            </Popover>

            {/* User Profile Dropdown */}
            <Dropdown menu={{ items: userDropdownItems }} trigger={["click"]}>
              <div className="flex items-center gap-2.5 cursor-pointer p-1.5 hover:bg-slate-100 rounded-xl transition-colors">
                <Avatar
                  size={36}
                  className="bg-gradient-to-tr from-teal-500 to-emerald-500 text-white font-bold shadow-sm"
                  icon={<User size={18} />}
                />
                <div className="hidden sm:flex flex-col items-start leading-tight">
                  <span className="text-xs font-bold text-slate-800">
                    Giảng viên Rikkei
                  </span>
                  <span className="text-[10px] text-teal-600 font-semibold">
                    Admin Content Lead
                  </span>
                </div>
                <ChevronDown size={14} className="text-slate-400" />
              </div>
            </Dropdown>
          </div>
        </Header>

        {/* Scrollable Page Content */}
        <Content
          style={{
            flex: 1,
            overflowY: "auto",
            background: "#f8fafc",
          }}
        >
          <div
            style={{
              padding: "24px 32px",
              minHeight: "calc(100vh - 120px)",
            }}
          >
            <AppBreadcrumb />
            <Outlet />
          </div>
          <Footer
            style={{
              textAlign: "center",
              color: "#94a3b8",
              padding: "16px 24px",
              fontSize: "12px",
              background: "#f8fafc",
              borderTop: "1 border-slate-200/60",
            }}
          >
            Elearning Content Factory Agent System ©{new Date().getFullYear()} • Developed for Rikkei Education
          </Footer>
        </Content>
      </Layout>
    </Layout>
  );
}

