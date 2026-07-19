import { useState, useEffect } from "react";
import { Button, Form, Input, Card, message } from "antd";
import { Lock, Phone, KeyRound } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

export default function ResetPassword() {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [isResetPassword, setIsResetPassword] = useState(true);
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingSendOtp, setIsLoadingSendOtp] = useState(false);
  const [isHaveOtp, setIsHaveOtp] = useState(false);
  const [otpRequest, setOtpRequest] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [time, setTime] = useState(60);
  const [isNumber, setIsNumber] = useState(1);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval>;
    if (time > 0 && isHaveOtp) {
      interval = setInterval(() => {
        setTime((prev) => Math.max(0, prev - 1));
      }, 1000);
    } else if (time === 0 && isHaveOtp) {
      setIsHaveOtp(false);
      setOtpRequest("");
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [time, isHaveOtp]);

  const formatTime = (s: number) => {
    const m = Math.floor(s / 60);
    const sec = s % 60;
    return `${m}:${sec.toString().padStart(2, "0")}`;
  };

  const handleSendOtp = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (!phoneNumber) {
      message.error("Vui lòng nhập số điện thoại hoặc email trước");
      return;
    }
    setIsLoadingSendOtp(true);
    setTimeout(() => {
      setIsLoadingSendOtp(false);
      setIsHaveOtp(true);
      setTime(120);
      setIsNumber(isNumber + 1);
      message.success("Mã OTP đã được gửi đến số điện thoại / email của bạn!");
    }, 800);
  };

  const handleVerifyOtp = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      message.success("Mã OTP chính xác! Vui lòng tạo mật khẩu mới.");
      setIsResetPassword(false); // Move to password creation step
    }, 800);
  };

  const handleResetPassword = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      message.success("Đổi mật khẩu thành công!");
      navigate("/login");
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
                e.currentTarget.style.display = "none";
              }}
            />
          </div>
          <h3 className="text-2xl font-bold text-center text-slate-800 dark:text-white m-0">
            {isResetPassword ? "Quên mật khẩu" : "Tạo mật khẩu mới"}
          </h3>
          <p className="text-slate-400 dark:text-slate-300 text-sm mt-2 text-center">
            {isResetPassword
              ? "Xác nhận danh tính để khôi phục mật khẩu"
              : "Vui lòng nhập mật khẩu mới và xác nhận"}
          </p>
        </div>

        {isResetPassword ? (
          <Form
            form={form}
            layout="vertical"
            onFinish={handleVerifyOtp}
            requiredMark="optional"
            className="space-y-4"
          >
            <Form.Item
              name="phoneNumber"
              label={
                <span className="text-slate-600 dark:text-slate-200 font-medium">
                  Số điện thoại / Email
                  <span className="text-red-500 ml-1">*</span>
                </span>
              }
              rules={[{ required: true, message: "Vui lòng số điện thoại hoặc email" }]}
            >
              <Input
                prefix={<Phone size={18} className="text-slate-400 mr-2" />}
                placeholder="Nhập số điện thoại hoặc email"
                className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 rounded-lg h-11 flex items-center"
                onChange={(e) => setPhoneNumber(e.target.value)}
              />
            </Form.Item>

            <Form.Item
              name="otp"
              label={
                <span className="text-slate-600 dark:text-slate-200 font-medium">
                  Xác nhận mã OTP
                  <span className="text-red-500 ml-1">*</span>
                </span>
              }
              rules={[{ required: true, message: "Vui lòng nhập mã OTP" }]}
            >
              <Input
                prefix={<KeyRound size={18} className="text-slate-400 mr-2" />}
                placeholder="Nhập mã OTP 6 số"
                maxLength={6}
                disabled={!isHaveOtp}
                className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 rounded-lg h-11 flex items-center"
                onChange={(e) => setOtpRequest(e.target.value)}
                suffix={
                  <span
                    onClick={handleSendOtp}
                    className={`font-semibold text-xs cursor-pointer select-none transition-colors ${
                      phoneNumber
                        ? "text-[#1DBFAF] hover:text-[#1DBFAF]/80"
                        : "text-slate-400 cursor-not-allowed"
                    }`}
                  >
                    {isLoadingSendOtp ? (
                      <span className="animate-pulse">Đang gửi...</span>
                    ) : isHaveOtp ? (
                      `Gửi lại (${formatTime(time)})`
                    ) : isNumber === 1 ? (
                      "Gửi mã"
                    ) : (
                      "Gửi lại mã"
                    )}
                  </span>
                }
              />
            </Form.Item>

            <Form.Item className="pt-2">
              <Button
                loading={isLoading}
                disabled={!otpRequest || otpRequest.length < 4}
                htmlType="submit"
                type="primary"
                className="w-full rounded-lg h-11 text-base font-semibold shadow-md shadow-[#1DBFAF]/20"
                style={{
                  backgroundColor: "#1DBFAF",
                  borderColor: "#1DBFAF",
                  color: "#FFFFFF",
                  opacity: !otpRequest || otpRequest.length < 4 ? 0.6 : 1,
                }}
              >
                Xác nhận OTP
              </Button>
            </Form.Item>

            <div className="text-center pt-2">
              <Link
                to="/login"
                className="text-slate-500 dark:text-slate-400 hover:text-[#1DBFAF] transition-colors text-sm font-medium"
              >
                Quay lại Đăng nhập
              </Link>
            </div>
          </Form>
        ) : (
          <Form
            layout="vertical"
            onFinish={handleResetPassword}
            requiredMark="optional"
            className="space-y-4"
          >
            <Form.Item
              name="newPassword"
              label={
                <span className="text-slate-600 dark:text-slate-200 font-medium">
                  Mật khẩu mới
                  <span className="text-red-500 ml-1">*</span>
                </span>
              }
              rules={[
                { required: true, message: "Vui lòng nhập mật khẩu mới" },
                { min: 6, message: "Mật khẩu tối thiểu 6 ký tự" },
              ]}
            >
              <Input.Password
                prefix={<Lock size={18} className="text-slate-400 mr-2" />}
                placeholder="Nhập mật khẩu mới"
                className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 rounded-lg h-11"
              />
            </Form.Item>

            <Form.Item
              name="confirmPassword"
              label={
                <span className="text-slate-600 dark:text-slate-200 font-medium">
                  Xác thực mật khẩu mới
                  <span className="text-red-500 ml-1">*</span>
                </span>
              }
              dependencies={["newPassword"]}
              rules={[
                { required: true, message: "Vui lòng xác nhận mật khẩu mới" },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue("newPassword") === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject(new Error("Mật khẩu xác thực không trùng khớp!"));
                  },
                }),
              ]}
            >
              <Input.Password
                prefix={<Lock size={18} className="text-slate-400 mr-2" />}
                placeholder="Nhập lại mật khẩu mới"
                className="bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-700 rounded-lg h-11"
              />
            </Form.Item>

            <Form.Item className="pt-2">
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
                Cập nhật mật khẩu
              </Button>
            </Form.Item>
          </Form>
        )}
      </Card>
    </div>
  );
}
