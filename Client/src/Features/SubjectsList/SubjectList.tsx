"use client";

import { Subject } from "@/src/interface/subject.interface";
import { useMyTaskStore } from "@/src/store/task/myTaskStore";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
import { Paragraph } from "@/src/ui/p/Paragraph";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import styles from "./SubjectList.module.scss";
import { useUserStore } from "@/src/store/user/userStore";

interface Props {
  to: string;
  onSubjectSelect?: (subject: Subject) => void;
  isTwoStep?: boolean;
}

export const SubjectList = ({ to, onSubjectSelect, isTwoStep }: Props) => {
  const { subjects, getSubjects, loading, getTask, task } = useMyTaskStore();
  const user = useUserStore((state) => state.user);
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null);

  useEffect(() => {
    getSubjects();
  }, []);

  useEffect(() => {
    getTask(user?.Login || "");
  }, []);

  const counts = useMemo(() => {
    const m = new Map<string, number>();
    for (const t of task) m.set(t.SubjectName, (m.get(t.SubjectName) ?? 0) + 1);
    return m;
  }, [task]);

  const subjectsSorted = useMemo(
    () =>
      [...subjects].sort(
        (a, b) => (counts.get(b.Name) ?? 0) - (counts.get(a.Name) ?? 0)
      ),
    [subjects, counts]
  );

  const handleClick = (item: Subject) => {
    if (isTwoStep) {
      setSelectedSubject(item);
      onSubjectSelect?.(item);
    }
  };

  return (
    <div className={styles.container}>
      {!loading && subjectsSorted.length > 0 ? (
        subjectsSorted.map((item: Subject) => (
          <div key={item.ID} className={styles.item}>
            {isTwoStep ? (
              <div
                className={`${styles.card} ${
                  selectedSubject?.ID === item.ID ? styles.selected : ""
                }`}
                onClick={() => handleClick(item)}
                style={{ cursor: "pointer" }}
              >
                <div>
                  <Paragraph>{item.Name}</Paragraph>
                  <Paragraph size="tiny" color="gray">
                    Кол-во: {counts.get(item.Name) ?? 0}
                  </Paragraph>
                </div>
                <div>
                  <i className="pi pi-chevron-right"></i>
                </div>
              </div>
            ) : (
              <Link href={`${to}/${item.EnglishName}`}>
                <div className={styles.card}>
                  <div>
                    <Paragraph>{item.Name}</Paragraph>
                    <Paragraph size="tiny" color="gray">
                      Кол-во: {counts.get(item.Name) ?? 0}
                    </Paragraph>
                  </div>
                  <div>
                    <i className="pi pi-chevron-right"></i>
                  </div>
                </div>
              </Link>
            )}
          </div>
        ))
      ) : (
        <Spinner />
      )}
    </div>
  );
};
