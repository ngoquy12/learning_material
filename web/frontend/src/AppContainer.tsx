import { BrowserRouter } from "react-router-dom";
import { ConfigProvider, message } from "antd";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import AppRoutes from "./routes/AppRoutes";

message.config({
  top: 75,
  maxCount: 3,
});

const queryClient = new QueryClient();

export default function AppContainer() {
  return (
    <QueryClientProvider client={queryClient}>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: "#1DBFAF",
            fontFamily: "Roboto, sans-serif",
            controlHeight: 40,
          },
        }}
      >
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </ConfigProvider>
    </QueryClientProvider>
  );
}
