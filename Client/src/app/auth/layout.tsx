import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Вход в личный кабинет",
  description:
    "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
};

export default function AuthLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
