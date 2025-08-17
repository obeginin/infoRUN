import { BreadCrumb } from "../../../Features/BreadCrumb/BreadCrumb";
import { Header } from "../../../Widgets/Header/Header";
import type { IProfileProgress } from "../../../Widgets/Profile/ProfileProgress/ProfileProgress.interface";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import styles from "./ProfileAllTasks.module.scss";
import { Footer } from "../../../Widgets/Footer/Footer";
import { useEffect, useState } from "react";
import TasksAPI from "../../../API/tasks";
import { useUserStore } from "../../../store/userStore";
import { useIntersectionObserver, useQuery } from "@siberiacancode/reactuse";
import { Task } from "../../../ui/taskContainer/Task";
import { Paragraph } from "../../../ui/p/Paragraph";
import { Spinner } from "../../../ui/LoadingSpinner/LoadingSpinner";
import { Input } from "../../../ui/input/Input";
import { Button } from "../../../ui/buttonDeafault/Button";

export const ProfileAllTasks = () => {
  const token = localStorage.getItem("token");
  const user = useUserStore((state) => state.user);
  const [data, setData] = useState<IProfileProgress[]>([]);
  const [isFetchingMore, setIsFetchingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState<number>(0);
  const [visibleImage, setVisibleImage] = useState<number | null>(null);
  const [answer, setAnswer] = useState<string>("");
  const [tabFilters, setTabFilters] = useState<string>("Все");
  const filters = ["Все", "Выполненные", "В процессе", "Не приступал"];
  const [allTasksCache, setAllTasksCache] = useState<IProfileProgress[] | null>(null);

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
      enabled: tabFilters === "Все", // грузим постранично только в режиме "Все"
      onSuccess: (fetchedData: IProfileProgress[]) => {
        setData((prevData) => [...prevData, ...fetchedData]);
        setHasMore(fetchedData.length === limit);
        setIsFetchingMore(false);
      },
      onError: () => {
        setIsFetchingMore(false);
      },
    }
  );

  // При смене вкладки на фильтр (не "Все") — один раз грузим все задачи, потом фильтруем из кэша
  useEffect(() => {
    if (tabFilters === "Все") return;
    setIsFetchingMore(false);
    setHasMore(false); // отключаем инфинити в режиме фильтра

    const applyFilter = (list: IProfileProgress[]) => {
      let filtered: IProfileProgress[] = list;
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
      .then((res: IProfileProgress[]) => {
        setAllTasksCache(res);
        applyFilter(res);
      })
      .catch((e) => console.log(e));
  }, [tabFilters, allTasksCache]);

  // При возврате на "Все" — сбрасываем список и смещение, перезапускаем инфинити
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
      if (tabFilters !== "Все") return; // инфинити только для "Все"
      if (entry.isIntersecting && hasMore && !isFetchingMore) setIsFetchingMore(true);
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
      <div className="app">
        <Header />
        <BreadCrumb currentPage="Мои задачи" prevPage="Личный кабинет" />

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
                              className={styles.image}
                              src={`${import.meta.env.VITE_BASE_URL}/${
                                item.ImagePath
                              }`}
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
};
