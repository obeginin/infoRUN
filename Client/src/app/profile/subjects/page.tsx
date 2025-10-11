"use client";

import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Header } from "@/src/Widgets/Header/Header";
import { useEffect, useMemo } from "react";
import type { Subject } from "@/src/interface/subject.interface";
import styles from "./subjects.module.scss";
import { useMyTaskStore } from "@/src/store/task/myTaskStore";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { useUserStore } from "@/src/store/user/userStore";
import { Paragraph } from "@/src/ui/p/Paragraph";
import Link from "next/link";
export default function Subjects() {
  const { subjects, getSubjects, loading, getTask, task } = useMyTaskStore();
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Предметы", link: "/profile/subjects" },
  ];
  const user = useUserStore((state) => state.user);

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

  return (
    <div style={{ position: "relative", minHeight: "100vh" }}>
      <Header />
      <div className="app">
        <BreadCrumb items={items} />
        <section>
          <ProfileContentContainer>
            <div className={styles.container}>
              {!loading && subjectsSorted.length > 0 ? (
                subjectsSorted.map((item: Subject) => (
                  <div key={item.ID} className={styles.item}>
                    <Link href={`/profile/subjects/${item.EnglishName}`}>
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
                  </div>
                ))
              ) : (
                <Spinner />
              )}
            </div>
          </ProfileContentContainer>
        </section>
      </div>
      <Footer />
    </div>
  );
}
