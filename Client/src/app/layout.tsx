import type { Metadata } from "next";
import "./globals.css";
import "primeicons/primeicons.css";
import {
  Rubik_Doodle_Shadow,
  Zen_Maru_Gothic,
  Arsenal,
} from "next/font/google";
const rubik = Rubik_Doodle_Shadow({
  weight: "400",
  subsets: ["cyrillic"],
  variable: "--rubik",
});

const jost = Zen_Maru_Gothic({
  weight: "400",
  subsets: ["cyrillic"],
  variable: "--jost",
});

const huninn = Arsenal({
  weight: "400",
  subsets: ["cyrillic"],
  variable: "--Arsenal",
});

export const metadata: Metadata = {
  title: "Онлайн-платформа для подготовки к ЕГЭ",
  description:
    "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000"
  ),
  openGraph: {
    title: "Онлайн-платформа для подготовки к ЕГЭ",
    description:
      "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 600,
        alt: "Подготовка к ЕГЭ",
      },
    ],
    type: "website",
    locale: "ru_RU",
    siteName: "Онлайн-платформа для подготовки к ЕГЭ",
    url: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000",
  },
  twitter: {
    card: "summary_large_image",
    title: "Онлайн-платформа для подготовки к ЕГЭ",
    description:
      "Онлайн-платформа для подготовки к ЕГЭ — твой личный репетитор 24/7!",
    images: ["/og-image.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <head>
        <link rel="icon" href="/favicon.ico" />
 
      </head>
      <body
        className={`${rubik.variable} ${jost.variable} ${huninn.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
