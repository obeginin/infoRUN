import { Paragraph } from "../p/Paragraph";

interface TextContainerProps {
  children: React.ReactNode;
  size?: "large" | "medium" | "base" | "small" | "tiny";
  f_weight?: "light" | "bold" | "extra_bold";
  radius?: string;
  filled?: boolean;
  color?: "text" | "primary" | "white" | "gray";
  borderColor?: "primary" | "secondary" | "bg" | "gray" | "purple" | "peach";
}

export const TextContainer = ({
  children,
  size = "base",
  f_weight = "light",
  radius = "32px",
  filled = false,
  color = "text",
  borderColor = "primary",
}: TextContainerProps) => {
  return (
    <div
      style={{
        width: "fit-content",
        padding: "10px 25px",
        borderRadius: radius,
        border: `1px solid var(--${borderColor})`,
        backgroundColor: filled ? "var(--primary)" : "transparent",
        color: color ? `var(--${color})` : filled ? "var(--bg)" : "var(--text)",
      }}
    >
      <Paragraph size={size} f_weight={f_weight}>
        {children}
      </Paragraph>
    </div>
  );
};
