(globalThis.TURBOPACK = globalThis.TURBOPACK || []).push([typeof document === "object" ? document.currentScript : undefined, {

"[project]/public/assets/burger-menu.svg (static in ecmascript)": ((__turbopack_context__) => {

__turbopack_context__.v("/_next/static/media/burger-menu.3b071f24.svg");}),
"[project]/public/assets/burger-menu.svg.mjs { IMAGE => \"[project]/public/assets/burger-menu.svg (static in ecmascript)\" } [app-client] (structured image object, ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
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
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/ui/buttonDeafault/Button.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "active": "Button-module-scss-module__-Y2A9a__active",
  "button": "Button-module-scss-module__-Y2A9a__button",
  "disabled": "Button-module-scss-module__-Y2A9a__disabled",
  "pulseSpin": "Button-module-scss-module__-Y2A9a__pulseSpin",
  "spinner": "Button-module-scss-module__-Y2A9a__spinner",
});
}),
"[project]/src/src/ui/buttonDeafault/Button.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "Button": ()=>Button
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.module.scss.module.css [app-client] (css module)");
;
;
const Button = (param)=>{
    let { children, disabled = false, onClick, radius = "32px", filled = false, border, outlined = false, color = "text", style, type, width = "auto", loading = false, size = "base", fontSize = "base" } = param;
    const baseStyles = {
        zIndex: 10,
        width: width === "full" ? "100%" : "auto",
        fontSize: "var(--".concat(fontSize, ")"),
        borderRadius: radius,
        padding: size === "base" ? "10px 25px" : "5px 10px",
        backgroundColor: filled ? "var(--primary)" : "transparent",
        color: color ? "var(--".concat(color, ")") : filled ? "var(--bg)" : "var(--text)",
        border: border ? "1px solid var(--".concat(border, ")") : outlined ? "1px solid var(--primary)" : "none"
    };
    const finalStyles = style ? style : baseStyles;
    if (loading) {
        disabled = true;
    }
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("button", {
        type: type,
        style: finalStyles,
        className: "".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].button, " ").concat(disabled ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].disabled : __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].active, " ").concat(outlined ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].outlined : ""),
        disabled: disabled,
        onClick: onClick,
        children: loading ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
            style: {
                fontSize: "1.2rem"
            },
            className: "".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].spinner, " ")
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
_c = Button;
var _c;
__turbopack_context__.k.register(_c, "Button");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/Widgets/Header/Header.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

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
"[project]/src/src/ui/AnimationLink/AnimationLink.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "container": "AnimationLink-module-scss-module__NOd99G__container",
  "link": "AnimationLink-module-scss-module__NOd99G__link",
});
}),
"[project]/src/src/ui/AnimationLink/AnimationLink.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "AnimationLink": ()=>AnimationLink
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/AnimationLink/AnimationLink.module.scss.module.css [app-client] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
;
;
;
const AnimationLink = (param)=>{
    let { children, href, size = 'base', ...props } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].container,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("li", {
            ...props,
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].link,
            style: {
                fontSize: "var(--".concat(size, ")")
            },
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
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
    }, void 0, false, {
        fileName: "[project]/src/src/ui/AnimationLink/AnimationLink.tsx",
        lineNumber: 16,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = AnimationLink;
var _c;
__turbopack_context__.k.register(_c, "AnimationLink");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/Widgets/Header/Header.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "Header": ()=>Header
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg__$28$static__in__ecmascript$2922$__$7d$__$5b$app$2d$client$5d$__$28$structured__image__object$2c$__ecmascript$29$__ = __turbopack_context__.i('[project]/public/assets/burger-menu.svg.mjs { IMAGE => "[project]/public/assets/burger-menu.svg (static in ecmascript)" } [app-client] (structured image object, ecmascript)');
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/Widgets/Header/Header.module.scss.module.css [app-client] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/store/userStore.ts [app-client] (ecmascript)");
// import { useNavigate } from "react-router-dom";
// import { useEffect, useState } from "react";
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/image.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/AnimationLink/AnimationLink.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
"use client";
;
;
;
;
;
;
;
;
const Header = ()=>{
    _s();
    // const nav = useNavigate();
    const useUserLogout = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useUserStore"])({
        "Header.useUserStore[useUserLogout]": (state)=>state.logout
    }["Header.useUserStore[useUserLogout]"]);
    const user = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useUserStore"])({
        "Header.useUserStore[user]": (state)=>state.user
    }["Header.useUserStore[user]"]);
    const [isScrolled, setIsScrolled] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "Header.useEffect": ()=>{
            const handleScroll = {
                "Header.useEffect.handleScroll": ()=>{
                    const scrollThreshold = 100;
                    if (window.scrollY > scrollThreshold) {
                        setIsScrolled(true);
                    } else {
                        setIsScrolled(false);
                    }
                }
            }["Header.useEffect.handleScroll"];
            window.addEventListener("scroll", handleScroll);
            handleScroll();
            return ({
                "Header.useEffect": ()=>window.removeEventListener("scroll", handleScroll)
            })["Header.useEffect"];
        }
    }["Header.useEffect"], []);
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
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("header", {
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].header, " ").concat(isScrolled ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].scrolled : ""),
            children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].content__right,
                children: [
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$image$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                        src: __TURBOPACK__imported__module__$5b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg$2e$mjs__$7b$__IMAGE__$3d3e$__$225b$project$5d2f$public$2f$assets$2f$burger$2d$menu$2e$svg__$28$static__in__ecmascript$2922$__$7d$__$5b$app$2d$client$5d$__$28$structured__image__object$2c$__ecmascript$29$__["default"],
                        alt: "",
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].burger
                    }, void 0, false, {
                        fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                        lineNumber: 60,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0)),
                    (user === null || user === void 0 ? void 0 : user.RoleName) === "Админ" && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                        href: "/admin",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
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
                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("ul", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Header$2f$Header$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].list,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnimationLink"], {
                                href: "/profile",
                                size: "base",
                                children: "Профиль"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                                lineNumber: 69,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnimationLink"], {
                                href: "/profile/all-tasks",
                                size: "base",
                                children: "Мои задачи"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Header/Header.tsx",
                                lineNumber: 72,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$AnimationLink$2f$AnimationLink$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnimationLink"], {
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
                    !user ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                        href: "/auth",
                        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
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
                    }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
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
_s(Header, "pRtGOwpQ60pVdjQVQQWP0bd/6L0=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useUserStore"],
        __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$userStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useUserStore"]
    ];
});
_c = Header;
var _c;
__turbopack_context__.k.register(_c, "Header");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/API/filters.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>FiltersAPI
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
class FiltersAPI {
    static async getSubjects(token) {
        const response = await fetch("".concat(("TURBOPACK compile-time value", "https://info-run.ru"), "/api/subjects"), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer ".concat(token)
            }
        });
        return response.json();
    }
    static async getTaskNumber(token, subject_id) {
        const response = await fetch("".concat(("TURBOPACK compile-time value", "https://info-run.ru"), "/api/tasks?subject_id=").concat(subject_id), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer ".concat(token)
            }
        });
        return response.json();
    }
    static async getVariants(token) {
        const response = await fetch("".concat(("TURBOPACK compile-time value", "https://info-run.ru"), "/api/variants"), {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer ".concat(token)
            }
        });
        return response.json();
    }
}
;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/API/constructor.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "default": ()=>ConstructorAPI
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$build$2f$polyfills$2f$process$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = /*#__PURE__*/ __turbopack_context__.i("[project]/node_modules/next/dist/build/polyfills/process.js [app-client] (ecmascript)");
class ConstructorAPI {
    static async create(token, data) {
        const response = await fetch("".concat(("TURBOPACK compile-time value", "https://info-run.ru"), "/api/subtasks/create/v2"), {
            method: "POST",
            headers: {
                Authorization: "Bearer ".concat(token)
            },
            body: data
        });
        return response.json();
    }
}
;
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/store/useConstructorStore.ts [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "useConstructorStore": ()=>useConstructorStore
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/zustand/esm/react.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/zustand/esm/middleware.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/API/filters.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$constructor$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/API/constructor.ts [app-client] (ecmascript)");
;
;
;
;
const useConstructorStore = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$react$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["create"])()((0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["persist"])((set, get)=>({
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
        initialAnswerFiles: [],
        initialDescriptionFiles: [],
        getSubjects: async ()=>{
            set({
                loading: true
            });
            const token = localStorage.getItem("token") || "";
            try {
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].getSubjects(token);
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
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].getTaskNumber(token, task_id);
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
                const response = await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$filters$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].getVariants(token);
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
            console.log(get().initialAnswerFiles, get().initialDescriptionFiles, get().elements);
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
        initialAnswerFilesAdd: ()=>{
            const newElement = {
                id: Date.now(),
                file: null
            };
            set((state)=>({
                    initialAnswerFiles: [
                        ...state.initialAnswerFiles,
                        newElement
                    ]
                }));
        },
        initialDescriptionFilesAdd: ()=>{
            const newElement = {
                id: Date.now(),
                file: null
            };
            set((state)=>({
                    initialDescriptionFiles: [
                        ...state.initialDescriptionFiles,
                        newElement
                    ]
                }));
        },
        initialDescriptionFilesRemove: (id)=>{
            set((state)=>({
                    initialDescriptionFiles: state.initialDescriptionFiles.filter((element)=>element.id !== id)
                }));
        },
        initialAnswerFilesRemove: (id)=>{
            set((state)=>({
                    initialAnswerFiles: state.initialAnswerFiles.filter((element)=>element.id !== id)
                }));
        },
        updateInitialAnswerFile: (id, file)=>{
            set((state)=>({
                    initialAnswerFiles: state.initialAnswerFiles.map((element)=>{
                        if (element.id === id) {
                            return {
                                ...element,
                                file
                            };
                        }
                        return element;
                    })
                }));
        },
        updateInitialDescriptionFile: (id, file)=>{
            set((state)=>({
                    initialDescriptionFiles: state.initialDescriptionFiles.map((element)=>{
                        if (element.id === id) {
                            return {
                                ...element,
                                file
                            };
                        }
                        return element;
                    })
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
            if (!data.state.subject || !data.state.task || !data.state.variant_id) {
                set({
                    error: "Заполните все поля",
                    loading: false
                });
                return;
            } else {
                const task = data.state.task.TaskID;
                const subject = data.state.subject.ID;
                const variant = data.state.variant.VariantID;
                try {
                    var _get_task, _get_variant, _get_subject;
                    const data = new FormData();
                    if ((_get_task = get().task) === null || _get_task === void 0 ? void 0 : _get_task.TaskID) {
                        data.append("subtask_number", subject);
                    }
                    if ((_get_variant = get().variant) === null || _get_variant === void 0 ? void 0 : _get_variant.VariantID) {
                        data.append("variant_id", variant);
                    }
                    if ((_get_subject = get().subject) === null || _get_subject === void 0 ? void 0 : _get_subject.ID) {
                        data.append("task_id", task);
                    }
                    if (get().answer) {
                        data.append("answer", get().answer);
                    }
                    if (get().initialAnswerFiles) {
                        get().initialAnswerFiles.forEach((file)=>{
                            if (file.file) {
                                data.append("files_solution", file.file);
                            }
                        });
                    }
                    if (get().initialDescriptionFiles) {
                        get().initialDescriptionFiles.forEach((file)=>{
                            if (file.file) {
                                data.append("files", file.file);
                            }
                        });
                    }
                    const blocks = [];
                    get().elements.forEach((element, index)=>{
                        if (element.type === "text") {
                            blocks.push({
                                type: "text",
                                content: element.content || ""
                            });
                        } else if (element.type === "image" && element.file) {
                            // Добавляем файл в FormData
                            data.append("file_".concat(index), element.file);
                            blocks.push({
                                type: "image",
                                file_index: index,
                                content: element.content || ""
                            });
                        }
                    });
                    // Добавляем blocks как JSON строку
                    data.append("blocks", JSON.stringify(blocks));
                    console.log(data);
                    if (get().task === null || get().subject === null || blocks.length === 0) {
                        set({
                            error: "Задание не было сохранено. Проверьте введенные данные",
                            loading: false
                        });
                    } else {
                        await __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$API$2f$constructor$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].create(token, data);
                        set({
                            success: "Задание успешно сохранено: ",
                            loading: false,
                            elements: [],
                            subject: null,
                            task: null,
                            variant: null,
                            answer: "",
                            initialAnswerFiles: [],
                            initialDescriptionFiles: []
                        });
                        localStorage.removeItem("constructor-storage");
                    }
                } catch (error) {
                    set({
                        error: "Failed to save task" + error,
                        loading: false
                    });
                }
            }
        },
        clearMessages: ()=>{
            set({
                error: null,
                success: null
            });
        },
        setError: (error)=>{
            set({
                error
            });
        }
    }), {
    name: "constructor-storage",
    storage: (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$zustand$2f$esm$2f$middleware$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["createJSONStorage"])(()=>localStorage),
    partialize: (state)=>({
            subject: state.subject,
            task: state.task,
            variant: state.variant,
            answer: state.answer
        })
}));
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/ui/LoadingSpinner/LoadingSpinner.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "ball1": "LoadingSpinner-module-scss-module__sjzvuG__ball1",
  "ball2": "LoadingSpinner-module-scss-module__sjzvuG__ball2",
  "loader": "LoadingSpinner-module-scss-module__sjzvuG__loader",
  "rotate": "LoadingSpinner-module-scss-module__sjzvuG__rotate",
  "spinner": "LoadingSpinner-module-scss-module__sjzvuG__spinner",
});
}),
"[project]/src/src/ui/LoadingSpinner/LoadingSpinner.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "Spinner": ()=>Spinner
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/LoadingSpinner/LoadingSpinner.module.scss.module.css [app-client] (css module)");
;
;
const Spinner = ()=>{
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].spinner,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].loader
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
_c = Spinner;
var _c;
__turbopack_context__.k.register(_c, "Spinner");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/ui/textArea/TextArea.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "textarea": "TextArea-module-scss-module__lFND1W__textarea",
});
}),
"[project]/src/src/ui/textArea/TextArea.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "TextArea": ()=>TextArea
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/textArea/TextArea.module.scss.module.css [app-client] (css module)");
;
;
const TextArea = (param)=>{
    let { value, onChange, placeholder = "Введите текст..." } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("textarea", {
        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].textarea,
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
_c = TextArea;
var _c;
__turbopack_context__.k.register(_c, "TextArea");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

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
"[project]/src/src/ui/InputImage/InputImage.module.scss.module.css [app-client] (css module)": ((__turbopack_context__) => {

__turbopack_context__.v({
  "input__container": "InputImage-module-scss-module__0SD4ga__input__container",
  "label": "InputImage-module-scss-module__0SD4ga__label",
  "preview": "InputImage-module-scss-module__0SD4ga__preview",
  "preview__image": "InputImage-module-scss-module__0SD4ga__preview__image",
});
}),
"[project]/src/src/ui/p/Paragraph.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "Paragraph": ()=>Paragraph
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
;
const Paragraph = (param)=>{
    let { children, size = "base", f_weight = "light", color } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("p", {
        style: {
            fontSize: "var(--".concat(size, ")"),
            fontWeight: "var(--fw_".concat(f_weight, ")"),
            color: "var(--".concat(color, ")")
        },
        children: children
    }, void 0, false, {
        fileName: "[project]/src/src/ui/p/Paragraph.tsx",
        lineNumber: 15,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_c = Paragraph;
var _c;
__turbopack_context__.k.register(_c, "Paragraph");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/ui/InputImage/InputImage.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "InputImage": ()=>InputImage
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/ui/InputImage/InputImage.module.scss.module.css [app-client] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/p/Paragraph.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
;
;
;
const InputImage = (param)=>{
    let { file, onChange } = param;
    _s();
    const [preview, setPreview] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [fileName, setFileName] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(null);
    const [isDragging, setIsDragging] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const fileInputRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    const handleFile = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useCallback"])({
        "InputImage.useCallback[handleFile]": (selectedFile)=>{
            if (selectedFile) {
                onChange(selectedFile);
                setFileName(selectedFile.name);
                // Создаем превью только для изображений
                if (selectedFile.type.startsWith("image/")) {
                    const reader = new FileReader();
                    reader.onload = ({
                        "InputImage.useCallback[handleFile]": (e)=>{
                            var _e_target;
                            return setPreview((_e_target = e.target) === null || _e_target === void 0 ? void 0 : _e_target.result);
                        }
                    })["InputImage.useCallback[handleFile]"];
                    reader.readAsDataURL(selectedFile);
                } else {
                    setPreview(null); // Сбрасываем превью для не-изображений
                }
            }
        }
    }["InputImage.useCallback[handleFile]"], [
        onChange
    ]);
    const handleFileChange = (event)=>{
        var _event_target_files;
        const selectedFile = (_event_target_files = event.target.files) === null || _event_target_files === void 0 ? void 0 : _event_target_files[0];
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
        setFileName(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = "";
        }
    };
    const handleClick = ()=>{
        var _fileInputRef_current;
        (_fileInputRef_current = fileInputRef.current) === null || _fileInputRef_current === void 0 ? void 0 : _fileInputRef_current.click();
    };
    // Функция для получения иконки файла по расширению
    const getFileIcon = (filename)=>{
        var _filename_split_pop;
        const extension = (_filename_split_pop = filename.split('.').pop()) === null || _filename_split_pop === void 0 ? void 0 : _filename_split_pop.toLowerCase();
        switch(extension){
            case 'pdf':
                return 'pi pi-file-pdf';
            case 'doc':
            case 'docx':
                return 'pi pi-file-word';
            case 'xls':
            case 'xlsx':
                return 'pi pi-file-excel';
            case 'jpg':
            case 'jpeg':
            case 'png':
            case 'gif':
                return 'pi pi-image';
            default:
                return 'pi pi-file';
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].input__container, " ").concat(isDragging ? __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].dragging : ""),
        onDragOver: handleDragOver,
        onDragLeave: handleDragLeave,
        onDrop: handleDrop,
        onClick: handleClick,
        children: preview ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].preview,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("img", {
                    src: preview,
                    alt: "Preview",
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].preview__image
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 113,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                    className: "pi pi-times",
                    onClick: handleRemove
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 114,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
            lineNumber: 112,
            columnNumber: 9
        }, ("TURBOPACK compile-time value", void 0)) : fileName ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].file__info,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                    className: getFileIcon(fileName)
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 118,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].file__name,
                    children: fileName
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 119,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                    className: "pi pi-times",
                    onClick: (e)=>{
                        e.stopPropagation();
                        handleRemove();
                    }
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 120,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
            lineNumber: 117,
            columnNumber: 9
        }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Fragment"], {
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("label", {
                    className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].label,
                    children: [
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("input", {
                            ref: fileInputRef,
                            type: "file",
                            className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].input,
                            onChange: handleFileChange,
                            accept: "pdf,doc,docx,xls,xlsx,jpg,jpeg,png"
                        }, void 0, false, {
                            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                            lineNumber: 131,
                            columnNumber: 13
                        }, ("TURBOPACK compile-time value", void 0)),
                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                            children: isDragging ? "Отпустите файл" : "Загрузить файл"
                        }, void 0, false, {
                            fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                            lineNumber: 138,
                            columnNumber: 13
                        }, ("TURBOPACK compile-time value", void 0))
                    ]
                }, void 0, true, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 130,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Paragraph"], {
                    size: "tiny",
                    color: "gray",
                    children: "PDF, DOC, DOCX, XLS, XLSX, JPG, JPEG, PNG до 10MB"
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 140,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Paragraph"], {
                    size: "tiny",
                    color: "gray",
                    children: "Или перетащите файл сюда"
                }, void 0, false, {
                    fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
                    lineNumber: 143,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true)
    }, void 0, false, {
        fileName: "[project]/src/src/ui/InputImage/InputImage.tsx",
        lineNumber: 102,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(InputImage, "8ZJZJLdFpsr9A5wsdfopv4VYjts=");
_c = InputImage;
var _c;
__turbopack_context__.k.register(_c, "InputImage");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/shared/Stepper/Stepper.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "Step": ()=>Step,
    "default": ()=>Stepper
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/framer-motion/dist/es/render/components/motion/proxy.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$components$2f$AnimatePresence$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/framer-motion/dist/es/components/AnimatePresence/index.mjs [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/client/app-dir/link.js [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature(), _s1 = __turbopack_context__.k.signature(), _s2 = __turbopack_context__.k.signature();
;
;
;
;
;
function Stepper(param) {
    let { children, initialStep = 1, onStepChange = ()=>{}, onFinalStepCompleted = ()=>{}, stepCircleContainerClassName = "", stepContainerClassName = "", contentClassName = "", footerClassName = "", // backButtonProps = {},
    // nextButtonProps = {},
    backButtonText = "Назад", nextButtonText = "Далее", disabledNextButton = false, disableStepIndicators = false, renderStepIndicator, endButtonChildren, linkEndButton, ...rest } = param;
    _s();
    const [currentStep, setCurrentStep] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(initialStep);
    const [direction, setDirection] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(0);
    const stepsArray = __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Children"].toArray(children);
    const totalSteps = stepsArray.length;
    const isCompleted = currentStep > totalSteps;
    const isLastStep = currentStep === totalSteps;
    const isNextButtonDisabled = typeof disabledNextButton === "function" ? disabledNextButton(currentStep) : disabledNextButton;
    const updateStep = (newStep)=>{
        setCurrentStep(newStep);
        if (newStep > totalSteps) {
            onFinalStepCompleted();
        } else {
            onStepChange(newStep);
        }
    };
    const handleBack = ()=>{
        if (currentStep > 1) {
            setDirection(-1);
            updateStep(currentStep - 1);
        }
    };
    const handleNext = ()=>{
        if (!isLastStep) {
            setDirection(1);
            updateStep(currentStep + 1);
        }
    };
    const handleComplete = ()=>{
        setDirection(1);
        updateStep(totalSteps + 1);
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "outer-container",
        ...rest,
        style: {},
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
            className: "step-circle-container ".concat(stepCircleContainerClassName),
            style: {
                border: "1px solid var(--primary)",
                backgroundColor: "var(--bg)"
            },
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "step-indicator-row ".concat(stepContainerClassName),
                    children: stepsArray.map((_, index)=>{
                        const stepNumber = index + 1;
                        const isNotLastStep = index < totalSteps - 1;
                        return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"].Fragment, {
                            children: [
                                renderStepIndicator ? renderStepIndicator({
                                    step: stepNumber,
                                    currentStep,
                                    onStepClick: (clicked)=>{
                                        setDirection(clicked > currentStep ? 1 : -1);
                                        updateStep(clicked);
                                    }
                                }) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(StepIndicator, {
                                    step: stepNumber,
                                    disableStepIndicators: disableStepIndicators,
                                    currentStep: currentStep,
                                    onClickStep: (clicked)=>{
                                        setDirection(clicked > currentStep ? 1 : -1);
                                        updateStep(clicked);
                                    }
                                }, void 0, false, {
                                    fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                                    lineNumber: 123,
                                    columnNumber: 19
                                }, this),
                                isNotLastStep && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(StepConnector, {
                                    isComplete: currentStep > stepNumber
                                }, void 0, false, {
                                    fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                                    lineNumber: 134,
                                    columnNumber: 19
                                }, this)
                            ]
                        }, stepNumber, true, {
                            fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                            lineNumber: 112,
                            columnNumber: 15
                        }, this);
                    })
                }, void 0, false, {
                    fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                    lineNumber: 107,
                    columnNumber: 9
                }, this),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(StepContentWrapper, {
                    isCompleted: isCompleted,
                    currentStep: currentStep,
                    direction: direction,
                    className: "step-content-default ".concat(contentClassName),
                    children: stepsArray[currentStep - 1]
                }, void 0, false, {
                    fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                    lineNumber: 141,
                    columnNumber: 9
                }, this),
                !isCompleted && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                    className: "footer-container ".concat(footerClassName),
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: "footer-nav ".concat(currentStep !== 1 ? "spread" : "end"),
                        children: [
                            currentStep !== 1 && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                size: "small",
                                fontSize: "small",
                                outlined: true,
                                color: "text",
                                onClick: handleBack,
                                children: backButtonText
                            }, void 0, false, {
                                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                                lineNumber: 156,
                                columnNumber: 17
                            }, this),
                            isLastStep ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$client$2f$app$2d$dir$2f$link$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
                                href: linkEndButton || "",
                                children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                    size: "small",
                                    fontSize: "small",
                                    filled: true,
                                    color: "white",
                                    onClick: handleComplete,
                                    children: endButtonChildren
                                }, void 0, false, {
                                    fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                                    lineNumber: 168,
                                    columnNumber: 19
                                }, this)
                            }, void 0, false, {
                                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                                lineNumber: 167,
                                columnNumber: 17
                            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                disabled: isNextButtonDisabled,
                                size: "small",
                                fontSize: "small",
                                filled: true,
                                color: "white",
                                onClick: handleNext,
                                children: nextButtonText
                            }, void 0, false, {
                                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                                lineNumber: 179,
                                columnNumber: 17
                            }, this)
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                        lineNumber: 152,
                        columnNumber: 13
                    }, this)
                }, void 0, false, {
                    fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                    lineNumber: 151,
                    columnNumber: 11
                }, this)
            ]
        }, void 0, true, {
            fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
            lineNumber: 103,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 102,
        columnNumber: 5
    }, this);
}
_s(Stepper, "u1gtuB8foRkyiUtDuJBTA7S/CTA=");
_c = Stepper;
function StepContentWrapper(param) {
    let { isCompleted, currentStep, direction, children, className } = param;
    _s1();
    const [parentHeight, setParentHeight] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(0);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
        className: className,
        style: {
            position: "relative",
            overflow: "hidden"
        },
        animate: {
            height: isCompleted ? 0 : parentHeight
        },
        transition: {
            type: "spring",
            duration: 0.4
        },
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$components$2f$AnimatePresence$2f$index$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["AnimatePresence"], {
            initial: false,
            mode: "sync",
            custom: direction,
            children: !isCompleted && /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(SlideTransition, {
                direction: direction,
                onHeightReady: (h)=>setParentHeight(h),
                children: children
            }, currentStep, false, {
                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                lineNumber: 224,
                columnNumber: 11
            }, this)
        }, void 0, false, {
            fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
            lineNumber: 222,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 216,
        columnNumber: 5
    }, this);
}
_s1(StepContentWrapper, "8nJUmvnv1Q4tl3zvDcDnUhXEVbk=");
_c1 = StepContentWrapper;
function SlideTransition(param) {
    let { children, direction, onHeightReady } = param;
    _s2();
    const containerRef = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useRef"])(null);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useLayoutEffect"])({
        "SlideTransition.useLayoutEffect": ()=>{
            if (containerRef.current) {
                onHeightReady(containerRef.current.offsetHeight);
            }
        }
    }["SlideTransition.useLayoutEffect"], [
        children,
        onHeightReady
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
        ref: containerRef,
        custom: direction,
        variants: stepVariants,
        initial: "enter",
        animate: "center",
        exit: "exit",
        transition: {
            duration: 0.4
        },
        style: {
            position: "absolute",
            left: 0,
            right: 0,
            top: 0
        },
        children: children
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 257,
        columnNumber: 5
    }, this);
}
_s2(SlideTransition, "JVErPvg7bZ6yLj50J4lCvDO7Tjk=");
_c2 = SlideTransition;
const stepVariants = {
    enter: (dir)=>({
            x: dir >= 0 ? "-100%" : "100%",
            opacity: 0
        }),
    center: {
        x: "0%",
        opacity: 1
    },
    exit: (dir)=>({
            x: dir >= 0 ? "50%" : "-50%",
            opacity: 0
        })
};
function Step(param) {
    let { children } = param;
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "step-default",
        children: children
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 292,
        columnNumber: 10
    }, this);
}
_c3 = Step;
function StepIndicator(param) {
    let { step, currentStep, onClickStep, disableStepIndicators, disabledNextButton } = param;
    const status = currentStep === step ? "active" : currentStep < step ? "inactive" : "complete";
    const handleClick = ()=>{
        if (step !== currentStep && !disableStepIndicators && !disabledNextButton) {
            onClickStep(step);
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
        onClick: handleClick,
        className: "step-indicator",
        animate: status,
        initial: false,
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
            variants: {
                inactive: {
                    scale: 1,
                    backgroundColor: "var(--primary)",
                    color: "var(--bg)"
                },
                active: {
                    scale: 1,
                    backgroundColor: "var(--primary)",
                    color: "var(--bg)"
                },
                complete: {
                    scale: 1,
                    backgroundColor: "var(--primary)",
                    color: "var(--bg)"
                }
            },
            transition: {
                duration: 0.3
            },
            className: "step-indicator-inner",
            children: status === "complete" ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(CheckIcon, {
                className: "check-icon"
            }, void 0, false, {
                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                lineNumber: 352,
                columnNumber: 11
            }, this) : status === "active" ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                className: "active-dot"
            }, void 0, false, {
                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                lineNumber: 354,
                columnNumber: 11
            }, this) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("span", {
                className: "step-number",
                children: step
            }, void 0, false, {
                fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
                lineNumber: 356,
                columnNumber: 11
            }, this)
        }, void 0, false, {
            fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
            lineNumber: 330,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 324,
        columnNumber: 5
    }, this);
}
_c4 = StepIndicator;
function StepConnector(param) {
    let { isComplete } = param;
    const lineVariants = {
        incomplete: {
            width: 0,
            backgroundColor: "transparent"
        },
        complete: {
            width: "100%",
            backgroundColor: "var(--light-gray)"
        }
    };
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
        className: "step-connector",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].div, {
            className: "step-connector-inner",
            variants: lineVariants,
            initial: false,
            animate: isComplete ? "complete" : "incomplete",
            transition: {
                duration: 0.4
            }
        }, void 0, false, {
            fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
            lineNumber: 375,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 374,
        columnNumber: 5
    }, this);
}
_c5 = StepConnector;
function CheckIcon(props) {
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("svg", {
        ...props,
        fill: "none",
        stroke: "white",
        strokeWidth: 2,
        viewBox: "0 0 24 24",
        children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$framer$2d$motion$2f$dist$2f$es$2f$render$2f$components$2f$motion$2f$proxy$2e$mjs__$5b$app$2d$client$5d$__$28$ecmascript$29$__["motion"].path, {
            initial: {
                pathLength: 0
            },
            animate: {
                pathLength: 1
            },
            transition: {
                delay: 0.1,
                type: "tween",
                ease: "easeOut",
                duration: 0.3
            },
            strokeLinecap: "round",
            strokeLinejoin: "round",
            d: "M5 13l4 4L19 7"
        }, void 0, false, {
            fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
            lineNumber: 395,
            columnNumber: 7
        }, this)
    }, void 0, false, {
        fileName: "[project]/src/src/shared/Stepper/Stepper.tsx",
        lineNumber: 388,
        columnNumber: 5
    }, this);
}
_c6 = CheckIcon;
var _c, _c1, _c2, _c3, _c4, _c5, _c6;
__turbopack_context__.k.register(_c, "Stepper");
__turbopack_context__.k.register(_c1, "StepContentWrapper");
__turbopack_context__.k.register(_c2, "SlideTransition");
__turbopack_context__.k.register(_c3, "Step");
__turbopack_context__.k.register(_c4, "StepIndicator");
__turbopack_context__.k.register(_c5, "StepConnector");
__turbopack_context__.k.register(_c6, "CheckIcon");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
"[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx [app-client] (ecmascript)": ((__turbopack_context__) => {
"use strict";

var { k: __turbopack_refresh__, m: module } = __turbopack_context__;
{
__turbopack_context__.s({
    "CreateForm": ()=>CreateForm
});
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/jsx-dev-runtime.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$useConstructorStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/store/useConstructorStore.ts [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/LoadingSpinner/LoadingSpinner.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/textArea/TextArea.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/node_modules/next/dist/compiled/react/index.js [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__ = __turbopack_context__.i("[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.module.scss.module.css [app-client] (css module)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/InputImage/InputImage.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/p/Paragraph.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/ui/buttonDeafault/Button.tsx [app-client] (ecmascript)");
var __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$shared$2f$Stepper$2f$Stepper$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__ = __turbopack_context__.i("[project]/src/src/shared/Stepper/Stepper.tsx [app-client] (ecmascript)");
;
var _s = __turbopack_context__.k.signature();
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
const CreateForm = ()=>{
    _s();
    const [step1Valid, setStep1Valid] = (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useState"])(false);
    const { subjects, getSubjects, setSubject, getTaskNumber, subject, loading, tasks, task, setTask, getVarinants, variants, variant, setVariant, answer, setAnswer, setImage, initialAnswerFiles, initialAnswerFilesAdd, initialAnswerFilesRemove, initialDescriptionFiles, initialDescriptionFilesAdd, initialDescriptionFilesRemove, updateInitialAnswerFile, updateInitialDescriptionFile } = (0, __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$useConstructorStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useConstructorStore"])();
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "CreateForm.useEffect": ()=>{
            getSubjects();
            getVarinants();
        }
    }["CreateForm.useEffect"], []);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "CreateForm.useEffect": ()=>{
            if (subject) {
                getTaskNumber(subject.ID);
            }
        }
    }["CreateForm.useEffect"], [
        subject
    ]);
    (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$index$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useEffect"])({
        "CreateForm.useEffect": ()=>{
            if (subject && task && variant) {
                setStep1Valid(true);
            }
        }
    }["CreateForm.useEffect"], [
        task,
        variant,
        subject
    ]);
    return /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("section", {
        children: loading && (!subjects || subjects.length === 0) && (!tasks || tasks.length === 0) ? /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$LoadingSpinner$2f$LoadingSpinner$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Spinner"], {}, void 0, false, {
            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
            lineNumber: 64,
            columnNumber: 9
        }, ("TURBOPACK compile-time value", void 0)) : /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$shared$2f$Stepper$2f$Stepper$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["default"], {
            linkEndButton: "/profile/create-task/constructor",
            endButtonChildren: "Перейти в конструктор",
            initialStep: 1,
            disabledNextButton: !step1Valid,
            children: [
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$shared$2f$Stepper$2f$Stepper$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Step"], {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("form", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].form,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select__container,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                        className: "pi pi-chevron-down ".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].icon)
                                    }, void 0, false, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 75,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                        value: (subject === null || subject === void 0 ? void 0 : subject.Name) || "",
                                        onChange: (e)=>{
                                            const selectedSubject = subjects === null || subjects === void 0 ? void 0 : subjects.find((s)=>s.Name === e.target.value);
                                            if (selectedSubject) setSubject(selectedSubject);
                                        },
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                value: "",
                                                children: "Выберите предмет"
                                            }, void 0, false, {
                                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                                lineNumber: 86,
                                                columnNumber: 19
                                            }, ("TURBOPACK compile-time value", void 0)),
                                            subjects === null || subjects === void 0 ? void 0 : subjects.map((subject)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                    value: subject.Name,
                                                    children: subject.Name
                                                }, subject.ID, false, {
                                                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                                    lineNumber: 88,
                                                    columnNumber: 21
                                                }, ("TURBOPACK compile-time value", void 0)))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 76,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 74,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select__container,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                        className: "pi pi-chevron-down ".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].icon)
                                    }, void 0, false, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 95,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                        value: (task === null || task === void 0 ? void 0 : task.TaskTitle) || "",
                                        onChange: (e)=>{
                                            const selectedTask = tasks === null || tasks === void 0 ? void 0 : tasks.find((t)=>t.TaskTitle === e.target.value);
                                            if (selectedTask) setTask(selectedTask);
                                        },
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                value: "",
                                                children: "Выберите категорию"
                                            }, void 0, false, {
                                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                                lineNumber: 106,
                                                columnNumber: 19
                                            }, ("TURBOPACK compile-time value", void 0)),
                                            tasks === null || tasks === void 0 ? void 0 : tasks.map((task)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                    value: task.TaskTitle,
                                                    children: task.TaskTitle
                                                }, task.TaskID, false, {
                                                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                                    lineNumber: 108,
                                                    columnNumber: 21
                                                }, ("TURBOPACK compile-time value", void 0)))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 96,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 94,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select__container,
                                children: [
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                        className: "pi pi-chevron-down ".concat(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].icon)
                                    }, void 0, false, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 115,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0)),
                                    /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("select", {
                                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].select,
                                        value: (variant === null || variant === void 0 ? void 0 : variant.VariantName) || "",
                                        onChange: (e)=>{
                                            const selectedVariant = variants === null || variants === void 0 ? void 0 : variants.find((v)=>v.VariantName === e.target.value);
                                            if (selectedVariant) setVariant(selectedVariant);
                                        },
                                        children: [
                                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                value: "",
                                                children: "Выберите вариант"
                                            }, void 0, false, {
                                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                                lineNumber: 126,
                                                columnNumber: 19
                                            }, ("TURBOPACK compile-time value", void 0)),
                                            variants === null || variants === void 0 ? void 0 : variants.map((variant)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("option", {
                                                    value: variant.VariantName,
                                                    children: variant.VariantName
                                                }, variant.VariantID, false, {
                                                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                                    lineNumber: 128,
                                                    columnNumber: 21
                                                }, ("TURBOPACK compile-time value", void 0)))
                                        ]
                                    }, void 0, true, {
                                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                        lineNumber: 116,
                                        columnNumber: 17
                                    }, ("TURBOPACK compile-time value", void 0))
                                ]
                            }, void 0, true, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 114,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$textArea$2f$TextArea$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["TextArea"], {
                                onChange: (e)=>setAnswer(e.target.value),
                                value: answer,
                                placeholder: "Введите ответ"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 134,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 73,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                    lineNumber: 72,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$shared$2f$Stepper$2f$Stepper$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Step"], {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Paragraph"], {
                                size: "small",
                                children: "Изображение с решением"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 143,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            initialAnswerFiles.map((file)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                            className: "pi pi-trash",
                                            onClick: ()=>initialAnswerFilesRemove(file.id)
                                        }, void 0, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 146,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["InputImage"], {
                                            file: file.file,
                                            onChange: (e)=>updateInitialAnswerFile(file.id, e)
                                        }, file.id, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 150,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, file.id, true, {
                                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                    lineNumber: 145,
                                    columnNumber: 17
                                }, ("TURBOPACK compile-time value", void 0))),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                onClick: ()=>initialAnswerFilesAdd(),
                                size: "small",
                                color: "white",
                                filled: true,
                                children: "Добавить изображение"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 157,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 142,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                    lineNumber: 141,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0)),
                /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$shared$2f$Stepper$2f$Stepper$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Step"], {
                    children: /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                        className: __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$Widgets$2f$Constructor$2f$CreateForm$2f$CreateForm$2e$module$2e$scss$2e$module$2e$css__$5b$app$2d$client$5d$__$28$css__module$29$__["default"].container,
                        children: [
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$p$2f$Paragraph$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Paragraph"], {
                                size: "small",
                                children: "Дополнительная информация к задаче"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 169,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0)),
                            initialDescriptionFiles.map((file)=>/*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("div", {
                                    children: [
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])("i", {
                                            className: "pi pi-trash",
                                            onClick: ()=>initialDescriptionFilesRemove(file.id)
                                        }, void 0, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 174,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0)),
                                        /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$InputImage$2f$InputImage$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["InputImage"], {
                                            file: file.file,
                                            onChange: (e)=>updateInitialDescriptionFile(file.id, e)
                                        }, file.id, false, {
                                            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                            lineNumber: 178,
                                            columnNumber: 19
                                        }, ("TURBOPACK compile-time value", void 0))
                                    ]
                                }, file.id, true, {
                                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                    lineNumber: 173,
                                    columnNumber: 17
                                }, ("TURBOPACK compile-time value", void 0))),
                            /*#__PURE__*/ (0, __TURBOPACK__imported__module__$5b$project$5d2f$node_modules$2f$next$2f$dist$2f$compiled$2f$react$2f$jsx$2d$dev$2d$runtime$2e$js__$5b$app$2d$client$5d$__$28$ecmascript$29$__["jsxDEV"])(__TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$ui$2f$buttonDeafault$2f$Button$2e$tsx__$5b$app$2d$client$5d$__$28$ecmascript$29$__["Button"], {
                                onClick: ()=>initialDescriptionFilesAdd(),
                                size: "small",
                                color: "white",
                                filled: true,
                                children: "Добавить файл"
                            }, void 0, false, {
                                fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                                lineNumber: 185,
                                columnNumber: 15
                            }, ("TURBOPACK compile-time value", void 0))
                        ]
                    }, void 0, true, {
                        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                        lineNumber: 168,
                        columnNumber: 13
                    }, ("TURBOPACK compile-time value", void 0))
                }, void 0, false, {
                    fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
                    lineNumber: 167,
                    columnNumber: 11
                }, ("TURBOPACK compile-time value", void 0))
            ]
        }, void 0, true, {
            fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
            lineNumber: 66,
            columnNumber: 9
        }, ("TURBOPACK compile-time value", void 0))
    }, void 0, false, {
        fileName: "[project]/src/src/Widgets/Constructor/CreateForm/CreateForm.tsx",
        lineNumber: 60,
        columnNumber: 5
    }, ("TURBOPACK compile-time value", void 0));
};
_s(CreateForm, "Zl5n1FI35lgRCnP1kBoOTJcrpgA=", false, function() {
    return [
        __TURBOPACK__imported__module__$5b$project$5d2f$src$2f$src$2f$store$2f$useConstructorStore$2e$ts__$5b$app$2d$client$5d$__$28$ecmascript$29$__["useConstructorStore"]
    ];
});
_c = CreateForm;
var _c;
__turbopack_context__.k.register(_c, "CreateForm");
if (typeof globalThis.$RefreshHelpers$ === 'object' && globalThis.$RefreshHelpers !== null) {
    __turbopack_context__.k.registerExports(module, globalThis.$RefreshHelpers$);
}
}}),
}]);

//# sourceMappingURL=_13273d24._.js.map