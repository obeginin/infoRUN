import type { Metadata } from "next";
import "./globals.css";
import 'primeicons/primeicons.css';
import { Rubik_Doodle_Shadow, Zen_Maru_Gothic, Arsenal } from "next/font/google";
const rubik = Rubik_Doodle_Shadow({
  weight: "400",
  subsets: ["cyrillic"],
  variable: "--rubik",
});

const jost = Zen_Maru_Gothic({
  weight: "400",
  subsets: ["cyrillic"],
  variable: "--jost",
})

const huninn = Arsenal({
  weight: "400",
  subsets: ["cyrillic"],
  variable: "--Arsenal",
})

export const metadata: Metadata = {
  title: "Онлайн-платформа для подготовки к ЕГЭ",
  description:
    "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body className={`${rubik.variable} ${jost.variable} ${huninn.variable} antialiased`}>{children}</body>
    </html>
  );
}
