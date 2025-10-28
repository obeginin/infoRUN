import { Rubik_Doodle_Shadow, Zen_Maru_Gothic, Arsenal } from "next/font/google";

export const rubik = Rubik_Doodle_Shadow({
  weight: "400",
  subsets: ["latin"],
  variable: "--rubik",
  display: "swap",
});

export const zen = Zen_Maru_Gothic({
  weight: "400",
  subsets: ["latin"], // при необходимости 'japanese'
  variable: "--jost",
  display: "swap",
});

export const arsenal = Arsenal({
  weight: "400",
  subsets: ["cyrillic", "latin"],
  variable: "--Arsenal",
  display: "swap",
});

export const fontVariables = `${rubik.variable} ${zen.variable} ${arsenal.variable}`;