import styles from "./CircualProgress.module.scss";

interface CircualProgressProps {
  total: number;
  completed: number;
}

export const CircualProgress = ({ total, completed }: CircualProgressProps) => {
  const radius = 120;
  const stroke = 30;
  const normalizedRadius = radius - stroke / 2;
  const circumference = 2 * Math.PI * normalizedRadius;
  const percent = total > 0 ? Math.min(100, Math.round((completed / total) * 100)) : 0;
  const strokeDashoffset = circumference - (percent / 100) * circumference;

  return (
    <div className={styles.progressWrapper}>
      <svg height={radius * 2} width={radius * 2}>
        {/* Фоновый круг */}
        <circle
          stroke="#dbe6fd"
          fill="none"
          strokeWidth={stroke}
          cx={radius}
          cy={radius}
          r={normalizedRadius}
        />
        {/* Прогресс */}
        <circle
          stroke="#639aff"
          fill="none"
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          cx={radius}
          cy={radius}
          r={normalizedRadius}
          style={{ transition: "stroke-dashoffset 0.5s" }}
        />
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dy=".3em"
          fontSize="24px"
          fontFamily="Lato"
          fill="#639aff"
        >
          {percent}%
        </text>
      </svg>
    </div>
  );
};
