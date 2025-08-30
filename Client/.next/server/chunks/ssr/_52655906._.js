module.exports = {

"[project]/public/assets/burger-menu.svg (static in ecmascript)": ((__turbopack_context__) => {

__turbopack_context__.v("/_next/static/media/burger-menu.3b071f24.svg");}),
"[project]/public/assets/burger-menu.svg.mjs { IMAGE => \"[project]/public/assets/burger-menu.svg (static in ecmascript)\" } [app-ssr] (structured image object, ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "default": ()=>__TURBOPACK__default__export__
});
var __TURBOPACK__imported__module__$5b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg__$28$static__in__ecmascript$29$__ = __turbopack_context__.i("[project]/public/assets/burger-menu.svg (static in ecmascript)");
;
const __TURBOPACK__default__export__ = {
    src: __TURBOPACK__imported__module__$5b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg__$28$static__in__ecmascript$29$__["default"],
    width: 40,
    height: 40,
    blurWidth: 0,
    blurHeight: 0
};
}),
"[project]/src/src/ui/buttonDeafault/Button.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "active": "Button-module-scss-module__-Y2A9a__active",
  "button": "Button-module-scss-module__-Y2A9a__button",
  "disabled": "Button-module-scss-module__-Y2A9a__disabled",
  "pulseSpin": "Button-module-scss-module__-Y2A9a__pulseSpin",
  "spinner": "Button-module-scss-module__-Y2A9a__spinner",
});
}),
"[project]/src/src/ui/buttonDeafault/Button.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "Button": ()=>Button
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.module.scss.module.css [app-ssr] (css module)");
;
;
const Button = ({ children, disabled = false, onClick, radius = "32px", filled = false, border, outlined = false, color = "text", style, type, width = "auto", loading = false, size = "base", fontSize = "base" })=>{
    const baseStyles = {
        zIndex: 10,
        width: width === "full" ? "100%" : "auto",
        fontSize: `var(--${fontSize})`,
        borderRadius: radius,
        padding: size === "base" ? "10px 25px" : "5px 10px",
        backgroundColor: filled ? "var(--primary)" : "transparent",
        color: color ? `var(--${color})` : filled ? "var(--bg)" : "var(--text)",
        border: border ? `1px solid var(--${border})` : outlined ? "1px solid var(--primary)" : "none"
    };
    const finalStyles = style ? style : baseStyles;
    if (loading) {
        disabled = true;
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        type: type,
        style: finalStyles,
        className: `${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].button} ${disabled ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].disabled : __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].active} ${outlined ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].outlined : ""}`,
        disabled: disabled,
        onClick: onClick,
        children: loading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
            style: {
                fontSize: "1.2rem"
            },
            className: `${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].spinner} `
        }, void 0, false, {
            fileName: "[project]/src/src/ui/buttonDeafault/Button.tsx",
            lineNumber: 68,
            columnNumber: 9
        }, ("TURBOPACK compile-time value", void 0)) : children
    }, void 0, false, {
        fileName: "[project]/src/src/ui/buttonDeafault/Button.tsx",
        lineNumber: 58,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/Widgets/Header/Header.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "burger": "Header-module-scss-module__-ePQmq__burger",
  "content__right": "Header-module-scss-module__-ePQmq__content__right",
  "dark": "Header-module-scss-module__-ePQmq__dark",
  "header": "Header-module-scss-module__-ePQmq__header",
  "light": "Header-module-scss-module__-ePQmq__light",
  "list": "Header-module-scss-module__-ePQmq__list",
  "scrolled": "Header-module-scss-module__-ePQmq__scrolled",
  "theme_switcher": "Header-module-scss-module__-ePQmq__theme_switcher",
});
}),
"[project]/src/src/ui/AnimationLink/AnimationLink.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "link": "AnimationLink-module-scss-module__NOd99G__link",
});
}),
"[project]/src/src/ui/AnimationLink/AnimationLink.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "AnimationLink": ()=>AnimationLink
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/AnimationLink/AnimationLink.module.scss.module.css [app-ssr] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-ssr] (ecmascript)");
;
;
;
const AnimationLink = ({ children, href, size = 'base', ...props })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
            ...props,
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].link,
            style: {
                fontSize: `var(--${size})`
            },
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                href: href ? href : "/",
                children: children
            }, void 0, false, {
                fileName: "[project]/src/src/ui/AnimationLink/AnimationLink.tsx",
                lineNumber: 18,
                columnNumber: 9
            }, ("TURBOPACK compile-time value", void 0))
        }, void 0, false, {
            fileName: "[project]/src/src/ui/AnimationLink/AnimationLink.tsx",
            lineNumber: 17,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false);
};
}),
"[project]/src/src/Widgets/Header/Header.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "Header": ()=>Header
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg__$28$static__in__ecmascript$2922$__$7d$__$5b$app$2d$ssr$5d$__$28$structured__image__object$2c$__ecmascript$29$__ = __turbopack_context__.i('[project]/public/assets/burger-menu.svg.mjs { IMAGE => "[project]/public/assets/burger-menu.svg (static in ecmascript)" } [app-ssr] (structured image object, ecmascript)');
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/Widgets/Header/Header.module.scss.module.css [app-ssr] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/store/userStore.ts [app-ssr] (ecmascript)");
// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/image.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/AnimationLink/AnimationLink.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
"use client";
;
;
;
;
;
;
;
;
;
const Header = ()=>{
    // const nav = useNavigate();
    const useUserLogout = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useUserStore"])((state)=>state.logout);
    const user = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useUserStore"])((state)=>state.user);
    const [isScrolled, setIsScrolled] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        const handleScroll = ()=>{
            const scrollThreshold = 100;
            if (window.scrollY > scrollThreshold) {
                setIsScrolled(true);
            } else {
                setIsScrolled(false);
            }
        };
        window.addEventListener("scroll", handleScroll);
        handleScroll();
        return ()=>window.removeEventListener("scroll", handleScroll);
    }, []);
    // const theme = localStorage.getItem("theme");
    // const [isDark, setIsDart] = useState(theme === "dark" ? true : false);
    // const handleClick = () => {
    //   setIsDart(!isDark);
    //   localStorage.setItem("theme", isDark ? "light" : "dark");
    // };
    // useEffect(() => {
    //   const theme = localStorage.getItem("theme");
    //   document.documentElement.setAttribute("data-theme", theme as string);
    // }, [isDark]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: `${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].header} ${isScrolled ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].scrolled : ""}`,
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].content__right,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                        src: __TURBOPACK__imported__module__$5b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg__$28$static__in__ecmascript$2922$__$7d$__$5b$app$2d$ssr$5d$__$28$structured__image__object$2c$__ecmascript$29$__["default"],
                        alt: "",
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].burger
                    }, void 0, false, {
                        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                        lineNumber: 60,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    user?.RoleName === "Админ" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                        href: "/admin",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                            color: "white",
                            filled: true,
                            children: "admin"
                        }, void 0, false, {
                            fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                            lineNumber: 63,
                            columnNumber: 17
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                        lineNumber: 62,
                        columnNumber: 15
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].list,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AnimationLink"], {
                                href: "/profile",
                                size: "base",
                                children: "Профиль"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                                lineNumber: 69,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AnimationLink"], {
                                href: "/profile/all-tasks",
                                size: "base",
                                children: "Мои задачи"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                                lineNumber: 72,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["AnimationLink"], {
                                href: "/",
                                size: "base",
                                children: "Категории заданий"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                                lineNumber: 75,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                        lineNumber: 68,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    !user ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                        href: "/auth",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                            color: "white",
                            filled: true,
                            children: "Войти"
                        }, void 0, false, {
                            fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                            lineNumber: 88,
                            columnNumber: 17
                        }, ("TURBOPACK compile-time value", void 0))
                    }, void 0, false, {
                        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                        lineNumber: 87,
                        columnNumber: 15
                    }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                        outlined: true,
                        onClick: useUserLogout,
                        children: "Выйти"
                    }, void 0, false, {
                        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                        lineNumber: 93,
                        columnNumber: 15
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                lineNumber: 59,
                columnNumber: 11
            }, ("TURBOPACK compile-time value", void 0))
        }, void 0, false, {
            fileName: "[project]/src/src/Widgets/Header/Header.tsx",
            lineNumber: 50,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
        lineNumber: 49,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/API/filters.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "default": ()=>FiltersAPI
});
class FiltersAPI {
    static async getSubjects(token) {
        const response = await fetch(`${("TURBOPACK compile-time value", "https://info-run.ru")}/api/subjects`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            }
        });
        return response.json();
    }
    static async getTaskNumber(token, subject_id) {
        const response = await fetch(`${("TURBOPACK compile-time value", "https://info-run.ru")}/api/tasks?subject_id=${subject_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            }
        });
        return response.json();
    }
    static async getVariants(token) {
        const response = await fetch(`${("TURBOPACK compile-time value", "https://info-run.ru")}/api/tasks/variants`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            }
        });
        return response.json();
    }
}
}),
"[project]/src/src/API/constructor.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "default": ()=>ConstructorAPI
});
class ConstructorAPI {
    static async create(token, data) {
        const response = await fetch(`${("TURBOPACK compile-time value", "https://info-run.ru")}/api/subtasks/create`, {
            method: "POST",
            headers: {
                Authorization: `Bearer ${token}`
            },
            body: data
        });
        return response.json();
    }
}
}),
"[project]/src/src/store/useConstructorStore.ts [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "useConstructorStore": ()=>useConstructorStore
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/zustand/esm/react.mjs [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/zustand/esm/middleware.mjs [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/API/filters.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$constructor$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/API/constructor.ts [app-ssr] (ecmascript)");
;
;
;
;
const useConstructorStore = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["create"])()((0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["persist"])((set, get)=>({
        loading: false,
        error: null,
        success: null,
        subject: null,
        subjects: [],
        task: null,
        variants: [],
        variant: null,
        answer: "",
        image: null,
        tasks: [],
        elements: [],
        getSubjects: async ()=>{
            set({
                loading: true
            });
            const token = localStorage.getItem("token") || "";
            try {
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].getSubjects(token);
                set({
                    subjects: response.subjects,
                    loading: false
                });
            } catch (error) {
                set({
                    error: "Ошибка получения данных" + error,
                    loading: false
                });
            }
        },
        setSubject: (subject)=>{
            set({
                subject
            });
        },
        getTaskNumber: async (task_id)=>{
            set({
                loading: true
            });
            const token = localStorage.getItem("token") || "";
            try {
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].getTaskNumber(token, task_id);
                set({
                    tasks: response.tasks,
                    loading: false
                });
            } catch (error) {
                set({
                    error: "Ошибка получения данных" + error,
                    loading: false
                });
            }
        },
        setTask: (task)=>{
            set({
                task
            });
        },
        getVarinants: async ()=>{
            set({
                loading: true
            });
            const token = localStorage.getItem("token") || "";
            try {
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].getVariants(token);
                set({
                    variants: response,
                    loading: false
                });
            } catch (error) {
                set({
                    error: "Ошибка получения данных" + error,
                    loading: false
                });
            }
        },
        setVariant: (variant)=>{
            set({
                variant
            });
        },
        setAnswer: (answer)=>{
            set({
                answer
            });
        },
        setImage: (image)=>{
            set({
                image
            });
        },
        moveElement: (id, direction)=>{
            set((state)=>({
                    elements: state.elements.map((element)=>{
                        if (element.id === id) {
                            const index = state.elements.indexOf(element);
                            if (direction === "up" && index > 0) {
                                return state.elements[index - 1];
                            } else if (direction === "down" && index < state.elements.length - 1) {
                                return state.elements[index + 1];
                            }
                        }
                        return element;
                    })
                }));
        },
        addElement: (type)=>{
            const newElement = {
                id: Date.now().toString(),
                type: type,
                content: type === "text" ? "" : undefined,
                file: type === "image" ? null : undefined
            };
            set((state)=>({
                    elements: [
                        ...state.elements,
                        newElement
                    ]
                }));
        },
        updateElement: (id, updates)=>{
            set((state)=>({
                    elements: state.elements.map((element)=>element.id === id ? {
                            ...element,
                            ...updates
                        } : element)
                }));
        },
        removeElement: (id)=>{
            set((state)=>({
                    elements: state.elements.filter((element)=>element.id !== id)
                }));
        },
        handleSave: async ()=>{
            set({
                loading: true,
                success: null,
                error: null
            });
            const token = localStorage.getItem("token") || "";
            const constructorStorage = localStorage.getItem("constructor-storage");
            const data = JSON.parse(constructorStorage || "");
            const task = data.state.task.TaskID;
            try {
                // Создаем FormData
                const data = new FormData();
                // Добавляем task_id
                if (get().task?.TaskID) {
                    data.append("task_id", task);
                }
                // Собираем blocks и файлы
                const blocks = [];
                get().elements.forEach((element, index)=>{
                    if (element.type === "text") {
                        blocks.push({
                            type: "text",
                            content: element.content || ""
                        });
                    } else if (element.type === "image" && element.file) {
                        // Добавляем файл в FormData
                        data.append(`file_${index}`, element.file);
                        blocks.push({
                            type: "image",
                            file_index: index,
                            content: element.content || ""
                        });
                    }
                });
                // Добавляем blocks как JSON строку
                data.append("blocks", JSON.stringify(blocks));
                // Вызываем API - передаем FormData напрямую
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$constructor$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"].create(token, data);
                set({
                    success: response.message,
                    loading: false
                });
            } catch (e) {
                set({
                    error: "Ошибка в создании задачи: " + e,
                    loading: false
                });
            }
        },
        clearMessages: ()=>{
            set({
                error: null,
                success: null
            });
        }
    }), {
    name: "constructor-storage",
    storage: (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["createJSONStorage"])(()=>localStorage),
    partialize: (state)=>({
            subject: state.subject,
            task: state.task,
            variant: state.variant,
            answer: state.answer
        })
}));
}),
"[project]/src/src/ui/LoadingSpinner/LoadingSpinner.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "ball1": "LoadingSpinner-module-scss-module__sjzvuG__ball1",
  "ball2": "LoadingSpinner-module-scss-module__sjzvuG__ball2",
  "loader": "LoadingSpinner-module-scss-module__sjzvuG__loader",
  "rotate": "LoadingSpinner-module-scss-module__sjzvuG__rotate",
  "spinner": "LoadingSpinner-module-scss-module__sjzvuG__spinner",
});
}),
"[project]/src/src/ui/LoadingSpinner/LoadingSpinner.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "Spinner": ()=>Spinner
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/LoadingSpinner/LoadingSpinner.module.scss.module.css [app-ssr] (css module)");
;
;
const Spinner = ()=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].spinner,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].loader
        }, void 0, false, {
            fileName: "[project]/src/src/ui/LoadingSpinner/LoadingSpinner.tsx",
            lineNumber: 5,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/src/src/ui/LoadingSpinner/LoadingSpinner.tsx",
        lineNumber: 4,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/ui/textArea/TextArea.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "textarea": "TextArea-module-scss-module__lFND1W__textarea",
});
}),
"[project]/src/src/ui/textArea/TextArea.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "TextArea": ()=>TextArea
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/textArea/TextArea.module.scss.module.css [app-ssr] (css module)");
;
;
const TextArea = ({ value, onChange, placeholder = "Введите текст..." })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].textarea,
        value: value,
        onChange: onChange,
        placeholder: placeholder,
        rows: 4
    }, void 0, false, {
        fileName: "[project]/src/src/ui/textArea/TextArea.tsx",
        lineNumber: 15,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "btn__container": "CreateForm-module-scss-module__k3wdca__btn__container",
  "container": "CreateForm-module-scss-module__k3wdca__container",
  "form": "CreateForm-module-scss-module__k3wdca__form",
  "icon": "CreateForm-module-scss-module__k3wdca__icon",
  "option": "CreateForm-module-scss-module__k3wdca__option",
  "select": "CreateForm-module-scss-module__k3wdca__select",
  "select__container": "CreateForm-module-scss-module__k3wdca__select__container",
});
}),
"[project]/src/src/Features/ProfileContentContainer/ProfileContentContainer.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "content": "ProfileContentContainer-module-scss-module__FvsfIG__content",
  "outside__content": "ProfileContentContainer-module-scss-module__FvsfIG__outside__content",
});
}),
"[project]/src/src/Features/ProfileContentContainer/ProfileContentContainer.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "ProfileContentContainer": ()=>ProfileContentContainer
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Features$2f$ProfileContentContainer$2f$ProfileContentContainer$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/Features/ProfileContentContainer/ProfileContentContainer.module.scss.module.css [app-ssr] (css module)");
;
;
const ProfileContentContainer = ({ children, width, color, borderColor })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Features$2f$ProfileContentContainer$2f$ProfileContentContainer$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].outside__content,
        style: {
            maxWidth: width
        },
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Features$2f$ProfileContentContainer$2f$ProfileContentContainer$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].content,
            style: {
                backgroundColor: color ? `var(--${color})` : "",
                border: borderColor ? `1px solid var(--${color})` : `1px solid var(--primary)`,
                transition: "all 0.2s ease-in-out"
            },
            children: children
        }, void 0, false, {
            fileName: "[project]/src/src/Features/ProfileContentContainer/ProfileContentContainer.tsx",
            lineNumber: 24,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/src/src/Features/ProfileContentContainer/ProfileContentContainer.tsx",
        lineNumber: 23,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/ui/InputImage/InputImage.module.scss.module.css [app-ssr] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "input__container": "InputImage-module-scss-module__0SD4ga__input__container",
  "label": "InputImage-module-scss-module__0SD4ga__label",
  "preview": "InputImage-module-scss-module__0SD4ga__preview",
  "preview__image": "InputImage-module-scss-module__0SD4ga__preview__image",
});
}),
"[project]/src/src/ui/InputImage/InputImage.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "InputImage": ()=>InputImage
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/InputImage/InputImage.module.scss.module.css [app-ssr] (css module)");
;
;
;
const InputImage = ({ file, onChange })=>{
    const [preview, setPreview] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isDragging, setIsDragging] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useState"])(false);
    const fileInputRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useRef"])(null);
    const handleFile = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useCallback"])((selectedFile)=>{
        if (selectedFile && selectedFile.type.startsWith("image/")) {
            onChange(selectedFile);
            const reader = new FileReader();
            reader.onload = (e)=>setPreview(e.target?.result);
            reader.readAsDataURL(selectedFile);
        }
    }, [
        onChange
    ]);
    const handleFileChange = (event)=>{
        const selectedFile = event.target.files?.[0];
        if (selectedFile) {
            handleFile(selectedFile);
        }
    };
    const handleDragOver = (e)=>{
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(true);
    };
    const handleDragLeave = (e)=>{
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
    };
    const handleDrop = (e)=>{
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            handleFile(droppedFile);
        }
    };
    const handleRemove = ()=>{
        onChange(null);
        setPreview(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };
    const handleClick = ()=>{
        fileInputRef.current?.click();
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: `${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].input__container} ${isDragging ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].dragging : ""}`,
        onDragOver: handleDragOver,
        onDragLeave: handleDragLeave,
        onDrop: handleDrop,
        onClick: handleClick,
        children: preview ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].preview,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                    src: preview,
                    alt: "Preview",
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].preview__image
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 81,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                    className: "pi pi-times",
                    onClick: handleRemove
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 82,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
            lineNumber: 80,
            columnNumber: 9
        }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Fragment"], {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].label,
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                            ref: fileInputRef,
                            type: "file",
                            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].input,
                            onChange: handleFileChange,
                            accept: "image/*"
                        }, void 0, false, {
                            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                            lineNumber: 87,
                            columnNumber: 13
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            children: isDragging ? "Отпустите файл" : "Загрузить файл"
                        }, void 0, false, {
                            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                            lineNumber: 94,
                            columnNumber: 13
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 86,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].hint,
                    children: "PNG, JPG, GIF до 10MB"
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 96,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].hint,
                    children: "Или перетащите файл сюда"
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 97,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true)
    }, void 0, false, {
        fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
        lineNumber: 70,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/ui/p/Paragraph.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "Paragraph": ()=>Paragraph
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
;
const Paragraph = ({ children, size = "base", f_weight = "light", color })=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        style: {
            fontSize: `var(--${size})`,
            fontWeight: `var(--fw_${f_weight})`,
            color: `var(--${color})`
        },
        children: children
    }, void 0, false, {
        fileName: "[project]/src/src/ui/p/Paragraph.tsx",
        lineNumber: 15,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),
"[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx [app-ssr] (ecmascript)": ((__turbopack_context__) => {
"use strict";

__turbopack_context__.s({
    "CreateForm": ()=>CreateForm
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react-jsx-dev-runtime.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$useConstructorStore$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/store/useConstructorStore.ts [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/LoadingSpinner/LoadingSpinner.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/textArea/TextArea.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/server/route-modules/app-page/vendored/ssr/react.js [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.module.scss.module.css [app-ssr] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Features$2f$ProfileContentContainer$2f$ProfileContentContainer$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/Features/ProfileContentContainer/ProfileContentContainer.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/InputImage/InputImage.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/p/Paragraph.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.tsx [app-ssr] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-ssr] (ecmascript)");
"use client";
;
;
;
;
;
;
;
;
;
;
;
const CreateForm = ()=>{
    const { subjects, getSubjects, setSubject, getTaskNumber, subject, loading, error, tasks, task, setTask, getVarinants, variants, variant, setVariant, answer, setAnswer, image, setImage } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$useConstructorStore$2e$ts__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useConstructorStore"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        getSubjects();
        getVarinants();
    }, []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["useEffect"])(()=>{
        if (subject) {
            getTaskNumber(subject.ID);
        }
    }, [
        subject
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Features$2f$ProfileContentContainer$2f$ProfileContentContainer$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["ProfileContentContainer"], {
            children: loading && (!subjects || subjects.length === 0) && (!tasks || tasks.length === 0) ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Spinner"], {}, void 0, false, {
                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                lineNumber: 53,
                columnNumber: 11
            }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].form,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].select__container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                className: `pi pi-chevron-down ${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].icon}`
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 57,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].select,
                                value: subject?.Name || "",
                                onChange: (e)=>{
                                    const selectedSubject = subjects?.find((s)=>s.Name === e.target.value);
                                    if (selectedSubject) setSubject(selectedSubject);
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "",
                                        children: "Выберите предмет"
                                    }, void 0, false, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 68,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    subjects?.map((subject)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: subject.Name,
                                            children: subject.Name
                                        }, subject.ID, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 70,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0)))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 58,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 56,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].select__container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                className: `pi pi-chevron-down ${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].icon}`
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 77,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].select,
                                value: task?.TaskTitle || "",
                                onChange: (e)=>{
                                    const selectedTask = tasks?.find((t)=>t.TaskTitle === e.target.value);
                                    if (selectedTask) setTask(selectedTask);
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "",
                                        children: "Выберите категорию"
                                    }, void 0, false, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 88,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    tasks?.map((task)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: task.TaskTitle,
                                            children: task.TaskTitle
                                        }, task.TaskID, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 90,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0)))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 78,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 76,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].select__container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                className: `pi pi-chevron-down ${__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].icon}`
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 97,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].select,
                                value: variant?.VariantName || "",
                                onChange: (e)=>{
                                    const selectedVariant = variants?.find((v)=>v.VariantName === e.target.value);
                                    if (selectedVariant) setVariant(selectedVariant);
                                },
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                        value: "",
                                        children: "Выберите вариант"
                                    }, void 0, false, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 108,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    variants?.map((variant)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                            value: variant.VariantName,
                                            children: variant.VariantName
                                        }, variant.VariantID, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 110,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0)))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 98,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 96,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["TextArea"], {
                        onChange: (e)=>setAnswer(e.target.value),
                        value: answer,
                        placeholder: "Введите ответ"
                    }, void 0, false, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 116,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Paragraph"], {
                                size: "small",
                                children: "Изображение с решением"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 122,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["InputImage"], {
                                file: image,
                                onChange: setImage
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 123,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 121,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$ssr$5d$__$28$css__module$29$__["default"].btn__container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                                outlined: true,
                                children: "Вернуться назад"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 126,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["default"], {
                                href: "/profile/create-task/constructor",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$server$2f$route$2d$modules$2f$app$2d$page$2f$vendored$2f$ssr$2f$react$2d$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$ssr$5d$__$28$ecmascript$29$__["Button"], {
                                    color: "white",
                                    filled: true,
                                    children: "Перейти в конструктор"
                                }, void 0, false, {
                                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                    lineNumber: 128,
                                    columnNumber: 17
                                }, ("TURBOPACK compile-time value", void 0))
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 127,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 125,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0))
                ]
            }, void 0, true, {
                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                lineNumber: 55,
                columnNumber: 11
            }, ("TURBOPACK compile-time value", void 0))
        }, void 0, false, {
            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
            lineNumber: 49,
            columnNumber: 7
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
        lineNumber: 48,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
}),

};

//# sourceMappingURL=_52655906._.js.map