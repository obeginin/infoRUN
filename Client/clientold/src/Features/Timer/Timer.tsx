import { useEffect } from "react";
import { Paragraph } from "../../ui/p/Paragraph";
import { useTimerStore } from "./store/store";

export const Timer = ({ taskId }: { taskId: number }) => {
  const { hours, minutes, seconds, isRunning, tick, currentTaskId } =
    useTimerStore();

  useEffect(() => {
    if (!isRunning) return;

    const interval = setInterval(() => {
      tick();
    }, 1000);
    return () => clearInterval(interval);
  }, [isRunning, tick]);

  if (currentTaskId !== taskId || !isRunning) {
    return null;
  }
  const formatTime = (value: number) => {
    return value < 10 ? `0${value}` : value.toString();
  };
  return (
    <div>
      <Paragraph>
        {formatTime(hours)}:{formatTime(minutes)}:{formatTime(seconds)}
      </Paragraph>
    </div>
  );
};
