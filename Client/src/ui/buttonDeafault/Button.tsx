// import styles from "./Button.module.scss";

// interface ButtonProps {
//   children: React.ReactNode;
//   disabled?: boolean;
//   onClick?: () => void;
//   radius?: string;
//   filled?: boolean;
//   outlined?: boolean;
//   border?: "primary" | "white";
//   color?: "primary" | "secondary" | "white" | "text";
//   style?: React.CSSProperties;
// }

// export const Button = ({
//   children,
//   disabled = false,
//   onClick,
//   radius = "32px",
//   filled = false,
//   border,
//   color = "text",
  
// }: ButtonProps) => {
//   return (
//     <>
//       <button
//         style={{
//           style ? style : {,

//           borderRadius: radius,
//           backgroundColor: filled ? "var(--primary)" : "transparent",
//           color: color ? `var(--${color})` : filled ? "var(--bg)" : "var(--text)",
//           border: border
//             ? `1px solid var(--${border})`
//             : "1px solid var(--primary)",
//         }}
//         className={`${styles.button} ${disabled ? styles.disabled : ""}`}
//         disabled={disabled}
//         onClick={onClick}
//       >
//         {children}
//       </button>
//     </>
//   );
// };


import styles from "./Button.module.scss";

interface ButtonProps {
  children: React.ReactNode;
  disabled?: boolean;
  onClick?: () => void;
  radius?: string;
  filled?: boolean;
  outlined?: boolean;
  border?: "primary" | "white";
  color?: "primary" | "secondary" | "white" | "text";
  style?: React.CSSProperties;
  type?: "button" | "submit" | "reset";
}

export const Button = ({
  children,
  disabled = false,
  onClick,
  radius = "32px",
  filled = false,
  border,
  outlined = false,
  color = "text",
  style,
  type
}: ButtonProps) => {
  const baseStyles = {
    borderRadius: radius,
    backgroundColor: filled ? "var(--primary)" : "transparent",
    color: color ? `var(--${color})` : filled ? "var(--bg)" : "var(--text)",
    border: border
      ? `1px solid var(--${border})`
      : outlined
      ? "1px solid var(--primary)"
      : "none",
  };

  const finalStyles = style ? style : baseStyles;

  return (
    <button
      type={type}
      style={finalStyles}
      className={`${styles.button} ${disabled ? styles.disabled : ""} ${
        outlined ? styles.outlined : ""
      }`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
};