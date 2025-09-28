"use client";

import { useEffect, useState } from "react";
import styles from "./allTasks.module.scss";
import { useUserStore } from "@/src/store/userStore";
import type { ITask } from "@/src/interface/subtask.interface";
import TasksAPI from "@/src/API/tasks";
import { useIntersectionObserver, useQuery } from "@siberiacancode/reactuse";
import { Header } from "@/src/Widgets/Header/Header";
import { BreadCrumb } from "@/src/ui/breadCrumb/BreadCrumb";
import { ProfileContentContainer } from "@/src/Features/ProfileContentContainer/ProfileContentContainer";
import { Button } from "@/src/ui/buttonDeafault/Button";
import { Task } from "@/src/ui/taskContainer/Task";
import { Paragraph } from "@/src/ui/p/Paragraph";
import { Footer } from "@/src/Widgets/Footer/Footer";
import { Spinner } from "@/src/ui/LoadingSpinner/LoadingSpinner";
import { Input } from "@/src/ui/input/Input";

export default function AllTasks() {
  const items = [
    { id: 1, label: "Личный кабинет", link: "/profile" },
    { id: 2, label: "Все задачи", link: "/profile/all-tasks" },
  ]
  const token = localStorage.getItem("token");
  const user = useUserStore((state) => state.user);
  const [data, setData] = useState<ITask[]>([]);
  const [isFetchingMore, setIsFetchingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState<number>(0);
  const [visibleImage, setVisibleImage] = useState<number | null>(null);
  const [answer, setAnswer] = useState<string>("");
  const [tabFilters, setTabFilters] = useState<string>("Все");
  const filters = ["Все", "Выполненные", "В процессе", "Не приступал"];
  const [allTasksCache, setAllTasksCache] = useState<ITask[] | null>(null);

  const limit = 10;

  const { isError, isSuccess } = useQuery(
    () =>
      TasksAPI.getStudentTask(
        user?.ID as number,
        token as string,
        limit,
        offset
      ).then((res) => res),
    {
      keys: [offset, tabFilters],
      enabled: tabFilters === "Все",
      onSuccess: (fetchedData: ITask[]) => {
        setData((prevData) => [...prevData, ...fetchedData]);
        setHasMore(fetchedData.length === limit);
        setIsFetchingMore(false);
      },
      onError: () => {
        setIsFetchingMore(false);
      },
    }
  );

  useEffect(() => {
    if (tabFilters === "Все") return;
    setIsFetchingMore(false);
    setHasMore(false);

    const applyFilter = (list: ITask[]) => {
      let filtered: ITask[] = list;
      switch (tabFilters) {
        case "Выполненные":
          filtered = list.filter((t) => t.CompletionStatus === "Выполнено");
          break;
        case "В процессе":
          filtered = list.filter((t) => t.CompletionStatus === "В процессе");
          break;
        case "Не приступал":
          filtered = list.filter(
            (t) => t.CompletionStatus === "Не приступал" || !t.CompletionStatus
          );
          break;
        default:
          filtered = list;
      }
      setData(filtered);
    };

    if (allTasksCache && allTasksCache.length) {
      applyFilter(allTasksCache);
      return;
    }

    TasksAPI.getAllTasks(user?.ID as number, token as string)
      .then((res: ITask[]) => {
        setAllTasksCache(res);
        applyFilter(res);
      })
      .catch((e) => console.log(e));
  }, [tabFilters, allTasksCache, user?.ID, token]);

  useEffect(() => {
    if (tabFilters !== "Все") return;
    setData([]);
    setOffset(0);
    setHasMore(true);
    setIsFetchingMore(false);
  }, [tabFilters]);

  const { ref } = useIntersectionObserver<HTMLDivElement>({
    threshold: 1,
    onChange: (entry) => {
      if (tabFilters !== "Все") return;
      if (entry.isIntersecting && hasMore && !isFetchingMore)
        setIsFetchingMore(true);
      setOffset((prev) => prev + limit);
    },
  });

  const handleClick = (SubTaskID: number) => {
    if (!answer || !SubTaskID || !user) return;
    setAnswer("");
    TasksAPI.checkAnswer(SubTaskID, user.ID, answer)
      .then((res) => res)
      .catch((err) => console.log(err));
  };

  return (
    <>
        <Header />
      <div className="app">
        <BreadCrumb items={items} />

        <section>
          <ProfileContentContainer>
            <div className={styles.content}>
              <div className={styles.filter__buttons}>
                {filters.map((item) => (
                  <Button
                    key={item}
                    onClick={() => setTabFilters(item)}
                    filled={tabFilters === item}
                    outlined={tabFilters !== item}
                    color={tabFilters === item ? "white" : "text"}
                    radius="16px"
                  >
                    {item}
                  </Button>
                ))}
              </div>
              {isSuccess &&
                data.map((item, index) => (
                  <Task
                    key={index}
                    border={`${
                      item.CompletionStatus === "В процессе"
                        ? "warning"
                        : item.CompletionStatus === "Выполнено"
                        ? "success"
                        : "primary"
                    }`}
                  >
                    <Paragraph>
                      {item.SubTaskID}: {item.TaskTitle} {item.VariantName}
                    </Paragraph>
                    <Paragraph>{item.Score}</Paragraph>
                    <i
                      onClick={() =>
                        setVisibleImage(visibleImage === index ? null : index)
                      }
                      className={`pi pi-angle-down ${styles.arrow}`}
                    ></i>

                    <div
                      className={`${styles.collapsible} ${
                        visibleImage === index ? styles.open : ""
                      }`}
                    >
                      <div className={styles.collapsibleInner}>
                        <ProfileContentContainer>
                          <div className={styles.image}>
                            <img
                              loading="lazy"
                              className={styles.image}
                              src={`${process.env.NEXT_PUBLIC_BASE_URL}/${item.ImagePath}`}
                              alt={item.ImagePath ? item.ImagePath : ""}
                            />
                            <div className={styles.answer}>
                              <Input
                                label="Ответ"
                                value={answer}
                                onChange={(e) => setAnswer(e.target.value)}
                                radius="16px"
                              />
                              <Button
                                onClick={() => handleClick(item.SubTaskID)}
                                radius="16px"
                                color="white"
                                filled
                              >
                                Отправить
                              </Button>
                            </div>
                          </div>
                        </ProfileContentContainer>
                      </div>
                    </div>
                  </Task>
                ))}

              {isFetchingMore &&
                Array(limit)
                  .fill(0)
                  .map((_, i) => (
                    <Task key={i}>
                      <Spinner />
                    </Task>
                  ))}
              {isError && <Paragraph>Произошла ошибка</Paragraph>}
              <div ref={ref} style={{ height: "1px", visibility: "hidden" }} />
            </div>
          </ProfileContentContainer>
        </section>
      </div>
      <Footer />
    </>
  );
}
