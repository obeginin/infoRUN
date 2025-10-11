import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Все задания",
  description:
    "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
};

export default function ProfileLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return <>{children}</>;
}
