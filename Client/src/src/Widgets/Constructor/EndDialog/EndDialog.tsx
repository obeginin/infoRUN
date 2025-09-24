"use client";

import { useConstructorStore } from "@/src/store/useConstructorStore";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { IDialog } from "@/src/ui/IDialog/IDialog";
import { Paragraph } from "@/src/ui/p/Paragraph";
import styles from "./EndDialog.module.scss";
import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export const EndDialog = () => {
  const { endDialog } = useConstructorStore();
  const [time, setTime] = useState(10);
  const router = useRouter();

  useEffect(() => {
    if (endDialog) {
      const interval = setInterval(() => {
        setTime((prev) => prev - 1);
      }, 1000);

      setTimeout(() => {
        router.push("/profile/my-tasks");
      }, 10000);
      return () => clearInterval(interval);
    }
  }, [endDialog]);
  return (
    <IDialog visible={endDialog} setVdisible={() => {}} closeIcon>
      <div className={styles.container}>
        <Paragraph size="medium">Задание успешно создано!</Paragraph>
        <i className="pi pi-check-circle"></i>
        <Paragraph>
          Вы будете перенаправлены на страницу задания через {time}
        </Paragraph>
        <div className={styles.buttons}>
          <Link href="/">
            <Button outlined>На главную</Button>
          </Link>
          <Link href="/profile/subjects">
            <Button filled color="white">
              Посмотреть задание
            </Button>
          </Link>
        </div>
      </div>
    </IDialog>
  );
};
