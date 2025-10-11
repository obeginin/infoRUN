import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Подтверждение электронной почты",
  description:
    "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
};

export default function ConfirmEmailLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
