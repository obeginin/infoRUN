"use client";

import FiltersAPI from "@/API/filters";
import { ProfileContentContainer } from "@/Features/ProfileContentContainer/ProfileContentContainer";
import { SubjectList } from "@/Features/SubjectsList/SubjectList";
import { Subject } from "@/interface/subject.interface";
import { ITaskNumber } from "@/interface/taskNumber.interface";
import { Footer } from "@/Widgets/Footer/Footer";
import { Header } from "@/Widgets/Header/Header";
import { useEffect, useState } from "react";
import styles from "./categories.module.scss";
import { Paragraph } from "@/ui/p/Paragraph";
import { Button } from "@/ui/buttonDeafault/Button";
import { BreadCrumb } from "@/ui/breadCrumb/BreadCrumb";
import Link from "next/link";

export default function Categories() {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Каталог заданий", link: "/profile/categories" },
  ];

  const [subjectSelect, setSubjectSelect] = useState<Subject | null>(null);
  const [taskNumberSelect, setTaskNumberSelect] = useState<ITaskNumber | null>(
    null
  );
  const [taskNumber, setTaskNumber] = useState<ITaskNumber[]>([]);
  const token = localStorage.getItem("token") || "";
  useEffect(() => {
    if (subjectSelect) {
      FiltersAPI.getTaskNumber(token, subjectSelect.ID)
        .then((res) => setTaskNumber(res.tasks))
        .catch((err) => console.log(err));
    }
  }, [subjectSelect]);
  return (
    <div style={{ position: "relative", height: "100vh" }}>
      <Header />

      <div className="app">
        <BreadCrumb items={items} />
        <section>
          <div className={styles.container}>
            <ProfileContentContainer>
              <SubjectList
                to="/profile/categories"
                isTwoStep
                onSubjectSelect={setSubjectSelect}
              />
            </ProfileContentContainer>
            <ProfileContentContainer>
              <div className={styles.content}>
                {taskNumber.length ? (
                  taskNumber.map((item) => (
                    <span
                      key={item.TaskTitle}
                      className={`${styles.item} + ${
                        taskNumberSelect?.TaskTitle === item.TaskTitle
                          ? styles.active
                          : ""
                      }`}
                      onClick={() => setTaskNumberSelect(item)}
                    >
                      {item.TaskTitle}
                    </span>
                  ))
                ) : (
                  <Paragraph>Выберите предмет</Paragraph>
                )}
              </div>
            </ProfileContentContainer>

            <Button
              color="white"
              filled
              disabled={!taskNumberSelect || !subjectSelect}
            >
              <Link
                href={`/profile/categories/selectedTask?subject=${subjectSelect?.ID}&task=${taskNumberSelect?.TaskID}`}
              >
                Перейти к заданиям
              </Link>
            </Button>
          </div>
        </section>
      </div>
      <Footer />
    </div>
  );
}
