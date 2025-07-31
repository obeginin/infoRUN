import { BreadCrumb } from "../../../Features/BreadCrumb/BreadCrumb";
import { Header } from "../../../Widgets/Header/Header";
import type { IProfileProgress } from "../../../Widgets/Profile/ProfileProgress/ProfileProgress.interface";
// import { Paragraph } from "../../../ui/p/Paragraph";
import { ProfileContentContainer } from "../../../Features/ProfileContentContainer/ProfileContentContainer";
import styles from "./ProfileAllTasks.module.scss";
import { Footer } from "../../../Widgets/Footer/Footer";
// import { SelectOption } from "../../../ui/selectOption/selectOption";
import { useState } from "react";
import TasksAPI from "../../../API/tasks";
import { useUserStore } from "../../../store/userStore";
import { useIntersectionObserver, useQuery } from "@siberiacancode/reactuse";
import { Task } from "../../../ui/taskContainer/Task";
import { Paragraph } from "../../../ui/p/Paragraph";
import { Spinner } from "../../../ui/LoadingSpinner/LoadingSpinner";

// interface subjectItem {
//   ID: number;
//   Name: string;
//   Description: string;
// }
// const status = ["Решенные", "Не решенные", "В процессе"];
export const ProfileAllTasks = () => {
  // const [subjects, setSubjects] = useState([]);
  const token = localStorage.getItem("token");
  const user = useUserStore((state) => state.user);
  const [data, setData] = useState<IProfileProgress[]>([]);
  const [isFetchingMore, setIsFetchingMore] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState<number>(0);
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
      keys: [offset],
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

  const { ref } = useIntersectionObserver<HTMLDivElement>({
    threshold: 1,
    onChange: (entry) => {
      if (entry.isIntersecting && hasMore && !isFetchingMore)
        setIsFetchingMore(true);
      setOffset((prev) => prev + limit);
    },
  });

  return (
    <>
      <div className="app">
        <Header />
        <BreadCrumb currentPage="Мои задачи" prevPage="Личный кабинет" />

        <section>
          <ProfileContentContainer>
            <div className={styles.content}>
              {isSuccess &&
                data.map((item, index) => (
                  <Task key={index}>
                      <Paragraph>{item.SubTaskID}: {item.VariantName}</Paragraph>
                      <Paragraph>{item.Score}</Paragraph>
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
