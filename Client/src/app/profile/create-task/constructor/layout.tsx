import { ProtectedRoute } from "@/src/Processes/ProtectedRoute/ProtectedRoute";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Создание задания",
  description:
    "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
};

export default function TaskConstructorLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <ProtectedRoute>{children}</ProtectedRoute>;
}
