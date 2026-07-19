import { useState } from "react";
import { Button, Form, Input, Card, message } from "antd";
import { Eye, EyeOff, Lock, User } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  const handleLogin = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      localStorage.setItem(
        "userLogined",
        JSON.stringify({
          firstName: "Admin",
          lastName: "User",
          role: { roleName: "Quản trị viên" },
          position: { positionName: "Giảng viên công nghệ" },
        })
      );
      message.success("Đăng nhập thành công!");
      navigate("/", { replace: true });
    }, 800);
  };

  return (
    <div className="w-full min-h-screen bg-slate-50 dark:bg-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Decorative gradient backgrounds */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-[#1DBFAF]/10 rounded-full blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-[#2edcc7]/10 rounded-full blur-[120px]" />

      <Card className="w-full max-w-[480px] shadow-xl border-none rounded-2xl p-4 sm:p-6 transition-all duration-300 relative z-10 bg-white/90 dark:bg-slate-800/90 backdrop-blur-sm">
        <div className="flex flex-col items-center mb-8">
          <div className="flex justify-center mb-4">
            <img
              loading="lazy"
              alt="Logo Rikkei Education"
              className="h-16 w-auto object-contain"
              src="/logo-main.png"
              onError={(e) => {
                // Fallback text if logo fails to render
                e.currentTarget.style.display = "none";
              }}
            />
          </div>
          <h3 className="text-2xl sm:text-3xl font-bold text-center text-slate-800 dark:text-white m-0">
            Elearning Factory
          </h3>
          <p className="text-slate-400 dark:text-slate-300 text-sm mt-2 text-center">
            Đăng nhập hệ thống quản lý học liệu tự động
          </p>
        </div>

        <Form
          layout="vertical"
          onFinish={handleLogin}
          requiredMark="optional"
          className="space-y-4"
        >
          <Form.Item
            name="username"
            label={
              <span className="text-slate-600 dark:text-slate-200 font-medium">
                Tên đăng nhập / Email
                <span className="text-red-500 ml-1">*</span>
              </span>
            }
            rules={[{ required: true, message: "Vui lòng nhập tên đăng nhập" }]}
          >
            <Input
              prefix={<User size={18} className="text-slate-400 mr-2" />}
              placeholder="Nhập username hoặc email"
              className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 rounded-lg h-11 flex items-center"
              autoFocus
            />
          </Form.Item>

          <Form.Item
            name="password"
            label={
              <span className="text-slate-600 dark:text-slate-200 font-medium">
                Mật khẩu
                <span className="text-red-500 ml-1">*</span>
              </span>
            }
            rules={[{ required: true, message: "Vui lòng nhập mật khẩu" }]}
          >
            <Input.Password
              prefix={<Lock size={18} className="text-slate-400 mr-2" />}
              placeholder="Nhập mật khẩu"
              className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 rounded-lg h-11"
              iconRender={(visible) =>
                visible ? (
                  <Eye size={20} className="text-slate-400 cursor-pointer" />
                ) : (
                  <EyeOff size={20} className="text-slate-400 cursor-pointer" />
                )
              }
            />
          </Form.Item>

          <div className="flex justify-end items-center py-2">
            <Link
              className="text-[#1DBFAF] hover:text-[#1DBFAF]/80 transition-colors text-sm font-medium"
              to="/reset"
            >
              Quên mật khẩu?
            </Link>
          </div>

          <Form.Item>
            <Button
              loading={isLoading}
              htmlType="submit"
              type="primary"
              className="w-full rounded-lg h-11 text-base font-semibold shadow-md shadow-[#1DBFAF]/20"
              style={{
                backgroundColor: "#1DBFAF",
                borderColor: "#1DBFAF",
                color: "#FFFFFF",
              }}
            >
              Đăng nhập
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
